#!/bin/bash

# Wait for Kibana to be ready
until curl -s -u elastic:ElasticStrong123! http://localhost:5601/api/status | grep -q "available"; do
  echo "Waiting for Kibana..."
  sleep 5
done

echo "Kibana is ready. Checking APM integration..."

# Get the policy ID
POLICY_ID="fleet-server-policy"

# Get current policy
POLICY=$(curl -s -u elastic:ElasticStrong123! -X GET "http://localhost:5601/api/fleet/agent_policies/${POLICY_ID}/full")

# Check if APM integration exists
APM_PACKAGE_POLICY_ID=$(echo $POLICY | grep -o '"id":"[^"]*","name":"apm-[0-9]*"' | head -1 | grep -o 'id":"[^"]*"' | cut -d'"' -f3)

if [ -z "$APM_PACKAGE_POLICY_ID" ]; then
  echo "APM integration not found. Please add it via Kibana UI:"
  echo "1. Go to Fleet > Agent Policies > fleet-server-policy"
  echo "2. Click 'Add integration'"
  echo "3. Search for 'Elastic APM' and add it"
  echo "4. Make sure to set the Elasticsearch host to 'http://elasticsearch:9200'"
else
  echo "APM integration found with ID: $APM_PACKAGE_POLICY_ID"
  echo "Checking configuration..."
fi
