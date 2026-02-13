# Langfuse Integration Troubleshooting Guide

## ✅ Current Configuration

Your Langflow is now configured with:

```yaml
LANGFUSE_SECRET_KEY: sk-lf-87ae8f58-4ea7-47b3-9f38-9be6938b27bc
LANGFUSE_PUBLIC_KEY: pk-lf-4943ac35-1532-477d-968a-2dafcbac229a
LANGFUSE_HOST: http://host.docker.internal:3000
LANGFUSE_ENABLED: "true"
```

## 🔍 How to Verify Traces Are Working

### Step 1: Check Langfuse is Running

```bash
cd c:\Users\tamil\repo\tamilsmtp\dockers\langfuse
docker compose ps
```

Expected output: `langfuse` container should be **Up** and healthy.

### Step 2: Access Langfuse Dashboard

1. Open browser: **http://localhost:3000**
2. Login with your Langfuse account
3. Navigate to your project (the one with the API keys above)

### Step 3: Create a Test Workflow in Langflow

1. Open **http://localhost:7860**
2. Create a **simple workflow**:
   - Add a **"Chat Input"** component
   - Add a **"Chat Output"** component
   - Connect them: Chat Input → Chat Output
3. **Run the workflow**:
   - Enter some text in the input
   - Click "Run" or "Play"
   - Wait for completion

### Step 4: Check for Traces in Langfuse

1. Go back to **Langfuse** (http://localhost:3000)
2. Click on **"Traces"** in the left sidebar
3. **Refresh the page** (F5)
4. You should see a new trace appear!

## 🐛 If No Traces Appear

### Check 1: Verify Environment Variables

```bash
cd c:\Users\tamil\repo\tamilsmtp\dockers\langflow
docker compose exec langflow env | findstr LANGFUSE
```

Expected output:
```
LANGFUSE_SECRET_KEY=sk-lf-87ae8f58-4ea7-47b3-9f38-9be6938b27bc
LANGFUSE_PUBLIC_KEY=pk-lf-4943ac35-1532-477d-968a-2dafcbac229a
LANGFUSE_HOST=http://host.docker.internal:3000
LANGFUSE_ENABLED=true
```

### Check 2: View Langflow Logs

```bash
docker compose logs langflow --tail 100
```

Look for:
- ✅ **No errors** about Langfuse connection
- ✅ **No 403 errors** (authentication failures)
- ⚠️ **Any warnings** about tracing

### Check 3: Verify Network Connectivity

Test if Langflow can reach Langfuse:

```bash
docker compose exec langflow curl -v http://host.docker.internal:3000/api/public/health
```

Expected: Should return a 200 OK response.

### Check 4: Verify API Keys in Langfuse

1. Login to **Langfuse** (http://localhost:3000)
2. Go to **Settings** → **API Keys**
3. Verify the keys match:
   - Secret Key: `sk-lf-87ae8f58-4ea7-47b3-9f38-9be6938b27bc`
   - Public Key: `pk-lf-4943ac35-1532-477d-968a-2dafcbac229a`

### Check 5: Restart Both Services

Sometimes a full restart helps:

```bash
# Restart Langfuse
cd c:\Users\tamil\repo\tamilsmtp\dockers\langfuse
docker compose restart langfuse

# Wait 30 seconds

# Restart Langflow
cd c:\Users\tamil\repo\tamilsmtp\dockers\langflow
docker compose restart langflow

# Wait 60 seconds for full startup
```

## 📊 What Traces Look Like

When working correctly, you'll see in Langfuse:

```
Trace: Workflow Execution
├─ Name: Your workflow name
├─ Timestamp: 2026-02-12 09:00:00
├─ Duration: 1.2s
├─ Status: Success/Error
└─ Components:
   ├─ Chat Input
   │  └─ Input: "Hello world"
   └─ Chat Output
      └─ Output: "Hello world"
```

## 🔧 Advanced Troubleshooting

### Enable Debug Logging

Edit `docker-compose.yml` and change:

```yaml
LANGFLOW_LOG_LEVEL: DEBUG  # Changed from INFO
```

Then restart:
```bash
docker compose restart langflow
```

View detailed logs:
```bash
docker compose logs -f langflow
```

### Check Langfuse Logs

```bash
cd c:\Users\tamil\repo\tamilsmtp\dockers\langfuse
docker compose logs langfuse --tail 100
```

Look for incoming trace requests.

### Test with Simple Python Script

Create a test file `test_langfuse.py`:

```python
from langfuse import Langfuse

langfuse = Langfuse(
    secret_key="sk-lf-87ae8f58-4ea7-47b3-9f38-9be6938b27bc",
    public_key="pk-lf-4943ac35-1532-477d-968a-2dafcbac229a",
    host="http://localhost:3000"
)

# Create a test trace
trace = langfuse.trace(name="test-trace")
trace.generation(
    name="test-generation",
    input="Hello",
    output="World"
)

print("Trace created! Check Langfuse dashboard.")
```

Run it:
```bash
pip install langfuse
python test_langfuse.py
```

If this works, the issue is with Langflow configuration.

## 📝 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| **403 Forbidden** | API keys are incorrect or from wrong project |
| **Connection refused** | Langfuse not running or wrong host |
| **No traces** | Tracing not enabled or workflow not executed |
| **Delayed traces** | Wait 10-30 seconds, then refresh |
| **Wrong project** | Verify you're viewing the correct project in Langfuse |

## ✅ Success Checklist

- [ ] Langfuse is running (http://localhost:3000)
- [ ] Langflow is running (http://localhost:7860)
- [ ] API keys are correct in docker-compose.yml
- [ ] Environment variables are loaded (check with `docker compose exec`)
- [ ] No errors in Langflow logs
- [ ] Workflow executed successfully in Langflow
- [ ] Checked "Traces" section in Langfuse
- [ ] Refreshed Langfuse page

## 🎯 Quick Test Command

Run this to verify everything:

```bash
# 1. Check services
cd c:\Users\tamil\repo\tamilsmtp\dockers\langfuse && docker compose ps
cd c:\Users\tamil\repo\tamilsmtp\dockers\langflow && docker compose ps

# 2. Check env vars
docker compose exec langflow env | findstr LANGFUSE

# 3. Test connectivity
docker compose exec langflow curl http://host.docker.internal:3000/api/public/health

# 4. Check logs
docker compose logs langflow --tail 50
```

## 📞 Still Not Working?

If traces still don't appear:

1. **Check the exact Langflow version**:
   ```bash
   docker compose exec langflow langflow --version
   ```

2. **Verify Langfuse project settings**:
   - Make sure the project is not archived
   - Check if there are any project-level restrictions

3. **Try the Langfuse UI directly**:
   - Create a manual trace in Langfuse to verify it's working
   - Settings → API Keys → "Create Test Trace"

---

**Need more help?** Share the output of:
```bash
docker compose logs langflow --tail 100 > langflow.log
docker compose logs langfuse --tail 100 > langfuse.log
```
