#!/bin/bash
# Tears down everything deploy.sh created: empties + the CloudFormation stack's
# S3 bucket (required before CFN can delete it), deletes the stack, then
# removes the packaging artifact bucket. Run this when you're done demoing to
# make sure nothing keeps billing.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_config.sh"

echo "This will permanently delete the '$STACK_NAME' stack and its data in region $REGION."
read -p "Type the stack name to confirm ($STACK_NAME): " CONFIRM
if [ "$CONFIRM" != "$STACK_NAME" ]; then
  echo "Confirmation did not match. Aborting."
  exit 1
fi

FRONTEND_BUCKET="$(aws cloudformation describe-stacks --stack-name "$STACK_NAME" --region "$REGION" \
  --query "Stacks[0].Outputs[?OutputKey=='FrontendBucketName'].OutputValue" --output text 2>/dev/null || true)"

if [ -n "${FRONTEND_BUCKET:-}" ] && [ "$FRONTEND_BUCKET" != "None" ]; then
  echo "==> Emptying frontend bucket ($FRONTEND_BUCKET)"
  aws s3 rm "s3://${FRONTEND_BUCKET}" --recursive --region "$REGION" || true
fi

echo "==> Deleting CloudFormation stack ($STACK_NAME)"
aws cloudformation delete-stack --stack-name "$STACK_NAME" --region "$REGION"
echo "    Waiting for deletion to finish..."
aws cloudformation wait stack-delete-complete --stack-name "$STACK_NAME" --region "$REGION"

if aws s3api head-bucket --bucket "$ARTIFACT_BUCKET" --region "$REGION" 2>/dev/null; then
  echo "==> Emptying and deleting artifact bucket ($ARTIFACT_BUCKET)"
  aws s3 rm "s3://${ARTIFACT_BUCKET}" --recursive --region "$REGION" || true
  aws s3api delete-bucket --bucket "$ARTIFACT_BUCKET" --region "$REGION"
fi

echo
echo "Teardown complete. No IT Ops Console resources should remain in $REGION."
