#!/bin/bash
# Deploys the IT Ops Console: packages Lambda code + CloudFormation, deploys the
# stack, writes frontend/config.js from the stack outputs, syncs the SPA + docs
# to S3, and invalidates CloudFront. Uses only the AWS CLI and macOS's built-in
# bash/zip/openssl — no CDK, SAM, Node, or Homebrew required.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_config.sh"

echo "Stack:   $STACK_NAME"
echo "Region:  $REGION"
echo "Account: $ACCOUNT_ID"
echo

echo "==> Ensuring artifact bucket exists ($ARTIFACT_BUCKET)"
if ! aws s3api head-bucket --bucket "$ARTIFACT_BUCKET" --region "$REGION" 2>/dev/null; then
  if [ "$REGION" = "us-east-1" ]; then
    aws s3api create-bucket --bucket "$ARTIFACT_BUCKET" --region "$REGION"
  else
    aws s3api create-bucket --bucket "$ARTIFACT_BUCKET" --region "$REGION" \
      --create-bucket-configuration LocationConstraint="$REGION"
  fi
fi

SHARED_SECRET="$(openssl rand -hex 20)"

echo "==> Packaging CloudFormation template (zips Lambda code, uploads to S3)"
aws cloudformation package \
  --template-file "$PROJECT_ROOT/infra/template.yaml" \
  --s3-bucket "$ARTIFACT_BUCKET" \
  --output-template-file "$PROJECT_ROOT/infra/.packaged-template.yaml" \
  --region "$REGION"

echo "==> Deploying CloudFormation stack (creates/updates real AWS resources)"
aws cloudformation deploy \
  --template-file "$PROJECT_ROOT/infra/.packaged-template.yaml" \
  --stack-name "$STACK_NAME" \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides SharedSecret="$SHARED_SECRET" \
  --region "$REGION"

echo "==> Reading stack outputs"
API_ENDPOINT="$(aws cloudformation describe-stacks --stack-name "$STACK_NAME" --region "$REGION" \
  --query "Stacks[0].Outputs[?OutputKey=='ApiEndpoint'].OutputValue" --output text)"
FRONTEND_BUCKET="$(aws cloudformation describe-stacks --stack-name "$STACK_NAME" --region "$REGION" \
  --query "Stacks[0].Outputs[?OutputKey=='FrontendBucketName'].OutputValue" --output text)"
FRONTEND_URL="$(aws cloudformation describe-stacks --stack-name "$STACK_NAME" --region "$REGION" \
  --query "Stacks[0].Outputs[?OutputKey=='FrontendUrl'].OutputValue" --output text)"
DISTRIBUTION_ID="$(aws cloudformation describe-stacks --stack-name "$STACK_NAME" --region "$REGION" \
  --query "Stacks[0].Outputs[?OutputKey=='DistributionId'].OutputValue" --output text)"

echo "==> Writing frontend/config.js"
cat > "$PROJECT_ROOT/frontend/config.js" <<EOF
window.OPS_CONSOLE_CONFIG = {
  apiBaseUrl: "${API_ENDPOINT}",
  apiKey: "${SHARED_SECRET}",
};
EOF

echo "==> Syncing frontend + docs to S3 ($FRONTEND_BUCKET)"
aws s3 sync "$PROJECT_ROOT/frontend" "s3://${FRONTEND_BUCKET}" \
  --region "$REGION" --delete --exclude "config.example.js"
aws s3 sync "$PROJECT_ROOT/docs" "s3://${FRONTEND_BUCKET}/docs" \
  --region "$REGION" --delete

echo "==> Invalidating CloudFront cache"
aws cloudfront create-invalidation --distribution-id "$DISTRIBUTION_ID" --paths "/*" >/dev/null

echo
echo "Deploy complete."
echo "App URL:      $FRONTEND_URL"
echo "API endpoint: $API_ENDPOINT"
echo
echo "Run scripts/seed.sh to load sample data, and scripts/destroy.sh when you're"
echo "done to tear everything down and stop any further charges."
