#!/bin/bash
# Shared config sourced by deploy.sh / seed.sh / destroy.sh.
# Written for macOS's default bash 3.2 — no associative arrays, no bash-4-only syntax.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

STACK_NAME="${STACK_NAME:-it-ops-console}"
REGION="${AWS_REGION:-$(aws configure get region 2>/dev/null)}"
REGION="${REGION:-us-east-1}"

ACCOUNT_ID="$(aws sts get-caller-identity --query Account --output text --region "$REGION")"
ARTIFACT_BUCKET="${STACK_NAME}-artifacts-${ACCOUNT_ID}-${REGION}"
