# Langflow + Langfuse Integration Setup Guide

## Current Status

✅ Langflow is configured and ready to run  
⚠️ Langfuse integration is **disabled** (commented out in docker-compose.yml)

## Why is Langfuse Integration Disabled?

The Langfuse integration requires valid API keys from a **project** created in Langfuse. The keys you provided were causing 403 authentication errors, which means:

1. The Langfuse project hasn't been created yet, OR
2. The API keys are invalid or expired

## How to Enable Langfuse Integration

Follow these steps to properly integrate Langflow with Langfuse:

### Step 1: Access Langfuse

1. Open http://localhost:3000 in your browser
2. Create an account or login

### Step 2: Create a Project in Langfuse

1. Click on "**New Project**" or "**Create Project**"
2. Give it a name (e.g., "Langflow Tracing")
3. Click "**Create**"

### Step 3: Get Your API Keys

1. In your Langfuse project, go to "**Settings**"
2. Navigate to "**API Keys**" section
3. You'll see:
   - **Public Key** (starts with `pk-lf-...`)
   - **Secret Key** (starts with `sk-lf-...`)
4. Copy both keys

### Step 4: Update docker-compose.yml

Edit `c:\Users\tamil\repo\tamilsmtp\dockers\langflow\docker-compose.yml`:

Find these lines (around line 34-37):
```yaml
# Langfuse integration (commented out - enable after creating project in Langfuse)
# LANGFUSE_SECRET_KEY: sk-lf-87ae8f58-4ea7-47b3-9f38-9be6938b27bc
# LANGFUSE_PUBLIC_KEY: pk-lf-4943ac35-1532-477d-968a-2dafcbac229a
# LANGFUSE_HOST: http://host.docker.internal:3000
```

**Uncomment and update** with your actual keys:
```yaml
# Langfuse integration
LANGFUSE_SECRET_KEY: sk-lf-YOUR-ACTUAL-SECRET-KEY-HERE
LANGFUSE_PUBLIC_KEY: pk-lf-YOUR-ACTUAL-PUBLIC-KEY-HERE
LANGFUSE_HOST: http://host.docker.internal:3000
```

### Step 5: Restart Langflow

```bash
cd c:\Users\tamil\repo\tamilsmtp\dockers\langflow
docker compose restart langflow
```

### Step 6: Verify Integration

1. Open Langflow at http://localhost:7860
2. Create and run a workflow
3. Go to Langfuse at http://localhost:3000
4. Check the "**Traces**" section - you should see your workflow execution

## Running Langflow WITHOUT Langfuse

If you want to use Langflow without Langfuse tracing (current setup):

```bash
cd c:\Users\tamil\repo\tamilsmtp\dockers\langflow
docker compose up -d
```

Access Langflow at: http://localhost:7860  
Login: admin / admin123

Everything will work normally, just without automatic tracing to Langfuse.

## Troubleshooting

### Still getting 403 errors after updating keys?

1. **Verify keys are correct**:
   - Copy them again from Langfuse
   - Make sure there are no extra spaces

2. **Check Langfuse is running**:
   ```bash
   cd c:\Users\tamil\repo\tamilsmtp\dockers\langfuse
   docker compose ps
   ```

3. **Restart both services**:
   ```bash
   # Restart Langfuse
   cd c:\Users\tamil\repo\tamilsmtp\dockers\langfuse
   docker compose restart langfuse
   
   # Restart Langflow
   cd c:\Users\tamil\repo\tamilsmtp\dockers\langflow
   docker compose restart langflow
   ```

### Can't access Langfuse at localhost:3000?

Make sure Langfuse is running:
```bash
cd c:\Users\tamil\repo\tamilsmtp\dockers\langfuse
docker compose up -d
```

## Benefits of Langfuse Integration

Once properly configured, you'll get:

- 📊 **Automatic Tracing** - Every workflow execution is logged
- 💰 **Cost Tracking** - Monitor LLM API costs
- ⚡ **Performance Metrics** - Latency, token usage, etc.
- 🐛 **Debugging** - See exactly what happened in each run
- 📈 **Analytics** - Visualize usage patterns over time

## Summary

**Current Setup**: Langflow runs standalone (no Langfuse integration)  
**To Enable**: Follow steps above to get valid API keys from Langfuse  
**Access**: http://localhost:7860 (Langflow) | http://localhost:3000 (Langfuse)
