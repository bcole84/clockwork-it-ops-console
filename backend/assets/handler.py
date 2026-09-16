import json
import os
import time
import uuid
from decimal import Decimal

import boto3

TABLE_NAME = os.environ["TABLE_NAME"]
SHARED_SECRET = os.environ["SHARED_SECRET"]

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

ALLOWED_STATUSES = {"In Stock", "In Use", "In Repair", "Retired"}


def _json_default(obj):
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def _response(status_code, body=None):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body, default=_json_default) if body is not None else "",
    }


def handler(event, context):
    method = event["requestContext"]["http"]["method"]
    if method == "OPTIONS":
        # HTTP API's automatic CORS handling doesn't intercept OPTIONS when a
        # route explicitly matches it (our routes use "ANY"), so it reaches
        # the Lambda. Let it through before the auth check so preflight succeeds.
        return _response(200, "")

    headers = {k.lower(): v for k, v in (event.get("headers") or {}).items()}
    if headers.get("x-ops-console-key") != SHARED_SECRET:
        return _response(401, {"error": "Unauthorized"})
    item_id = (event.get("pathParameters") or {}).get("id")

    try:
        if method == "GET" and not item_id:
            items = table.scan().get("Items", [])
            items.sort(key=lambda i: i.get("createdAt", 0), reverse=True)
            return _response(200, items)

        if method == "GET" and item_id:
            item = table.get_item(Key={"id": item_id}).get("Item")
            return _response(200, item) if item else _response(404, {"error": "Not found"})

        if method == "POST":
            body = json.loads(event.get("body") or "{}")
            now = int(time.time())
            item = {
                "id": str(uuid.uuid4()),
                "assetType": body.get("assetType", ""),
                "serialNumber": body.get("serialNumber", ""),
                "assignedTo": body.get("assignedTo", ""),
                "status": body.get("status") if body.get("status") in ALLOWED_STATUSES else "In Stock",
                "purchaseDate": body.get("purchaseDate", ""),
                "notes": body.get("notes", ""),
                "createdAt": now,
                "updatedAt": now,
            }
            table.put_item(Item=item)
            return _response(201, item)

        if method == "PUT" and item_id:
            existing = table.get_item(Key={"id": item_id}).get("Item")
            if not existing:
                return _response(404, {"error": "Not found"})
            body = json.loads(event.get("body") or "{}")
            for field in ("assetType", "serialNumber", "assignedTo", "purchaseDate", "notes"):
                if field in body:
                    existing[field] = body[field]
            if body.get("status") in ALLOWED_STATUSES:
                existing["status"] = body["status"]
            existing["updatedAt"] = int(time.time())
            table.put_item(Item=existing)
            return _response(200, existing)

        if method == "DELETE" and item_id:
            table.delete_item(Key={"id": item_id})
            return _response(204)

        return _response(405, {"error": "Method not allowed"})
    except Exception as exc:  # noqa: BLE001 - surfaced to the caller for a demo tool
        return _response(500, {"error": str(exc)})
