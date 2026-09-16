#!/bin/bash
# Loads realistic macOS-shop sample data into the 3 DynamoDB tables so the
# console isn't empty for a demo. Safe to re-run (adds more rows each time).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_config.sh"

ASSETS_TABLE="${STACK_NAME}-Assets"
TICKETS_TABLE="${STACK_NAME}-Tickets"
ONBOARDING_TABLE="${STACK_NAME}-Onboarding"

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

now_epoch() { date +%s; }

# Escapes backslashes and double quotes so values are safe to embed in
# hand-built JSON (several sample values contain a literal " for inches).
jesc() {
  local s="$1"
  s="${s//\\/\\\\}"
  s="${s//\"/\\\"}"
  printf '%s' "$s"
}

put_asset() {
  local asset_type serial assigned status purchased notes
  asset_type="$(jesc "$1")"; serial="$(jesc "$2")"; assigned="$(jesc "$3")"
  status="$(jesc "$4")"; purchased="$(jesc "$5")"; notes="$(jesc "$6")"
  local id ts
  id="$(uuidgen | tr 'A-Z' 'a-z')"
  ts="$(now_epoch)"
  cat > "$TMP_DIR/item.json" <<EOF
{
  "id": {"S": "$id"},
  "assetType": {"S": "$asset_type"},
  "serialNumber": {"S": "$serial"},
  "assignedTo": {"S": "$assigned"},
  "status": {"S": "$status"},
  "purchaseDate": {"S": "$purchased"},
  "notes": {"S": "$notes"},
  "createdAt": {"N": "$ts"},
  "updatedAt": {"N": "$ts"}
}
EOF
  aws dynamodb put-item --table-name "$ASSETS_TABLE" --item "file://$TMP_DIR/item.json" --region "$REGION"
}

put_ticket() {
  local subject description requester priority category status notes
  subject="$(jesc "$1")"; description="$(jesc "$2")"; requester="$(jesc "$3")"
  priority="$(jesc "$4")"; category="$(jesc "$5")"; status="$(jesc "$6")"; notes="$(jesc "$7")"
  local id ts
  id="$(uuidgen | tr 'A-Z' 'a-z')"
  ts="$(now_epoch)"
  cat > "$TMP_DIR/item.json" <<EOF
{
  "id": {"S": "$id"},
  "subject": {"S": "$subject"},
  "description": {"S": "$description"},
  "requester": {"S": "$requester"},
  "priority": {"S": "$priority"},
  "category": {"S": "$category"},
  "status": {"S": "$status"},
  "notes": {"S": "$notes"},
  "createdAt": {"N": "$ts"},
  "updatedAt": {"N": "$ts"}
}
EOF
  aws dynamodb put-item --table-name "$TICKETS_TABLE" --item "file://$TMP_DIR/item.json" --region "$REGION"
}

# steps_done is a space-separated list of 0/1 flags matching the step labels array order
put_onboarding() {
  local employee type target_date notes
  employee="$(jesc "$1")"; type="$(jesc "$2")"; target_date="$(jesc "$3")"; notes="$(jesc "$4")"
  shift 4
  local labels=("$@")
  local id ts
  id="$(uuidgen | tr 'A-Z' 'a-z')"
  ts="$(now_epoch)"

  {
    echo "{"
    echo "  \"id\": {\"S\": \"$id\"},"
    echo "  \"employeeName\": {\"S\": \"$employee\"},"
    echo "  \"type\": {\"S\": \"$type\"},"
    echo "  \"targetDate\": {\"S\": \"$target_date\"},"
    echo "  \"notes\": {\"S\": \"$notes\"},"
    echo "  \"createdAt\": {\"N\": \"$ts\"},"
    echo "  \"updatedAt\": {\"N\": \"$ts\"},"
    echo "  \"status\": {\"S\": \"In Progress\"},"
    echo "  \"steps\": {\"L\": ["
    local n=${#labels[@]}
    local i=0
    for entry in "${labels[@]}"; do
      i=$((i + 1))
      local label done_flag bool
      label="$(jesc "${entry%%|*}")"
      done_flag="${entry##*|}"
      bool="false"
      [ "$done_flag" = "1" ] && bool="true"
      printf '    {"M": {"label": {"S": "%s"}, "done": {"BOOL": %s}}}' "$label" "$bool"
      [ "$i" -lt "$n" ] && echo "," || echo ""
    done
    echo "  ]}"
    echo "}"
  } > "$TMP_DIR/item.json"

  aws dynamodb put-item --table-name "$ONBOARDING_TABLE" --item "file://$TMP_DIR/item.json" --region "$REGION"
}

echo "==> Seeding Assets"
put_asset 'MacBook Air 15" M3' "FVFXC2AB1234" "Priya Natarajan" "In Use" "2025-02-10" "AppleCare+ through 2028-02"
put_asset 'MacBook Pro 14" M3 Pro' "FVFXC2AB5678" "Jordan Michaels" "In Use" "2025-05-22" "Engineering build; 36GB RAM"
put_asset 'MacBook Air 13" M2' "FVFXC2AB9012" "" "In Stock" "2024-11-01" "Spare pool - ready to enroll in Mosyle"
put_asset 'MacBook Air 13" M2' "FVFXC2AB3456" "" "In Repair" "2024-08-15" "Battery swelling - sent to Apple Store for service"
put_asset 'MacBook Pro 16" M2 Max' "FVFXC2AB7890" "Sam Whitfield" "Retired" "2021-09-30" "End of 4-year refresh cycle; pending wipe and recycling"

echo "==> Seeding Tickets"
put_ticket "Can't connect to office Wi-Fi" "MacBook won't join the corp SSID since this morning, works fine on personal hotspot." "Priya Natarajan" "High" "Network" "In Progress" "Checked AP2 in Northeast HQ - flapping, escalated to facilities"
put_ticket "Need Confluence access to Marketing space" "New hire needs read/write on the Marketing space in Confluence." "Jordan Michaels" "Low" "Account/Access" "New" ""
put_ticket "Laptop fan running loud constantly" "Fan noise even at idle, temps seem high in Activity Monitor." "Sam Whitfield" "Medium" "Hardware" "Waiting" "Asked user to run Apple Diagnostics and share results"
put_ticket "1Password vault missing after reinstall" "Reinstalled 1Password after OS update, Engineering vault no longer showing." "Alex Chen" "Medium" "Software" "Resolved" "Re-added to Engineering vault from admin console; confirmed resolved"
put_ticket "Slack notifications not coming through on Mac" "No desktop notifications from Slack since latest macOS update." "Priya Natarajan" "Low" "Software" "New" ""

echo "==> Seeding Onboarding / Offboarding"
put_onboarding "Morgan Reyes" "Onboarding" "2026-09-22" "Joining as Support Engineer, hybrid, Minneapolis HQ" \
  "Mosyle enrollment complete|1" \
  "SSO / identity account created|1" \
  "Email / calendar provisioned|1" \
  "Slack account created and added to team channels|0" \
  "Jira / Confluence / Bitbucket access granted|0" \
  "1Password vault access granted|0" \
  "Laptop shipped or handed off|0" \
  "Day-1 IT check-in completed|0" \
  'Asset record updated to "In Use"|0'

put_onboarding "Taylor Brooks" "Offboarding" "2026-09-19" "Last day - voluntary departure, giving standard notice" \
  "SSO / identity account disabled|0" \
  "Slack account removed|0" \
  "Atlassian access revoked|0" \
  "1Password vault access revoked|0" \
  "Email suspended / forwarded per manager|0" \
  "Device remote-locked (if not same-day return)|0" \
  "Device returned and inspected|0" \
  "Device wiped via Mosyle and re-enrolled as spare|0" \
  'Asset record updated to "In Stock" or "Retired"|0'

echo
echo "Seed complete."
