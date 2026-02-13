#!/bin/bash

# This script fixes the APM integration Elasticsearch host configuration

echo "Fixing APM integration Elasticsearch host..."

# Get the package policy ID for APM
POLICY_RESPONSE=$(curl -s -u elastic:ElasticStrong123! -X GET "http://localhost:5601/api/fleet/package_policies" -H "kbn-xsrf: true")

APM_POLICY_ID=$(echo $POLICY_RESPONSE | grep -o '"id":"[^"]*","name":"apm-[0-9]*"' | head -1 | grep -o 'id":"[^"]*"' | cut -d'"' -f3)

if [ -z "$APM_POLICY_ID" ]; then
  echo "ERROR: No APM integration found!"
  echo "Please add the Elastic APM integration via Kibana UI first."
  exit 1
fi

echo "Found APM integration with ID: $APM_POLICY_ID"

# Get the full policy
FULL_POLICY=$(curl -s -u elastic:ElasticStrong123! -X GET "http://localhost:5601/api/fleet/package_policies/$APM_POLICY_ID" -H "kbn-xsrf: true")

# Update the Elasticsearch host
UPDATED_POLICY=$(echo $FULL_POLICY | sed 's/"localhost:9200"/"elasticsearch:9200"/g')

# Save the updated policy
curl -u elastic:ElasticStrong123! -X PUT "http://localhost:5601/api/fleet/package_policies/$APM_POLICY_ID" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d "$UPDATED_POLICY"

echo ""
echo "APM integration updated! Restart elastic-agent:"
echo "docker compose restart elastic-agent"
