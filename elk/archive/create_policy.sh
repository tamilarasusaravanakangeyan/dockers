curl -s -X POST "http://localhost:5601/api/fleet/agent_policies" \
  -H "Content-Type: application/json" \
  -H "kbn-xsrf: true" \
  -u elastic:ElasticStrong123! \
  -d '{
    "name": "Fleet Server Policy",
    "id": "fleet-server-policy",
    "namespace": "default",
    "monitoring_enabled": ["logs", "metrics"]
  }'
