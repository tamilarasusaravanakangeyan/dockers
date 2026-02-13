# 1. Install fleet_server package
curl -s -X POST "http://localhost:5601/api/fleet/epm/packages/fleet_server/8.19.2" \
  -H "kbn-xsrf: true" \
  -u elastic:ElasticStrong123!

# 2. Add Fleet Server integration to the policy
curl -s -X POST "http://localhost:5601/api/fleet/package_policies" \
  -H "Content-Type: application/json" \
  -H "kbn-xsrf: true" \
  -u elastic:ElasticStrong123! \
  -d '{
    "name": "fleet_server-1",
    "policy_id": "fleet-server-policy",
    "package": {
      "name": "fleet_server",
      "version": "8.19.2"
    },
    "inputs": {
      "fleet-server": {
        "enabled": true,
        "vars": {
          "host": "0.0.0.0",
          "port": 8220
        }
      }
    }
  }'
