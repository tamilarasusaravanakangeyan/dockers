# 🚨 CRITICAL FIX NEEDED: APM Integration Configuration

## Problem
The elastic-agent's APM server is trying to connect to `localhost:9200` instead of `elasticsearch:9200`, causing it to fail to start. This means port 4317 is NOT actually listening, so the otel-collector cannot send data.

## Solution: Fix APM Integration in Kibana

### Step 1: Open Kibana
Go to: http://localhost:5601
Login: elastic / ElasticStrong123!

### Step 2: Navigate to Fleet
☰ Menu → Management → Fleet → Agent Policies

### Step 3: Edit the Policy
Click on **"fleet-server-policy"**

### Step 4: Find APM Integration
Look for an integration named **"apm-1"** or **"Elastic APM"**
Click on it to edit

### Step 5: Fix Elasticsearch Host
In the APM integration settings, find the field:
**"Elasticsearch host"** or **"Output"**

Change from:
```
http://localhost:9200
```

To:
```
http://elasticsearch:9200
```

### Step 6: Save Changes
Click **"Save integration"**

### Step 7: Wait for Agent to Update
The elastic-agent will automatically receive the new configuration within 30 seconds.

### Step 8: Verify
Run this command to check if APM server started successfully:

```bash
docker logs elastic-agent --tail 50 | findstr "APM Server listening"
```

You should see:
```
APM Server listening on: 0.0.0.0:8200
OTLP gRPC listening on: 0.0.0.0:4317
OTLP HTTP listening on: 0.0.0.0:4318
```

### Step 9: Test the Connection
Once APM is running, test your FastAPI app:

```bash
python main.py
```

Then in another terminal:
```bash
curl http://localhost:8081/hello
```

Check otel-collector logs - errors should stop:
```bash
docker logs otel-collector --tail 20
```

---

## Alternative: If APM Integration Doesn't Exist

If you don't see an APM integration, you need to add it:

1. In **fleet-server-policy**, click **"Add integration"**
2. Search for **"Elastic APM"**
3. Click **"Add Elastic APM"**
4. Configure:
   - **Name**: apm-1
   - **Host**: `0.0.0.0:8200`
   - **URL**: (leave default)
   - **Elasticsearch host**: `http://elasticsearch:9200`
   - **Enable OTLP**: ✅ YES
   - **OTLP gRPC port**: 4317
   - **OTLP HTTP port**: 4318
5. Click **"Save and continue"**
6. Click **"Save and deploy changes"**

---

## Why This Happens

When you add an APM integration via Kibana UI, it sometimes defaults to `localhost:9200` because Kibana assumes Elasticsearch is on the same host. In Docker, each container has its own `localhost`, so we must use the service name `elasticsearch` instead.
