# Complete Langfuse Integration Setup Guide

## 🎯 Goal: Enable Observability for Langflow

This guide will help you get **valid Langfuse API keys** and enable full observability for your Langflow workflows.

## ✅ Current Status

- ✅ **Langfuse**: Running at http://localhost:3000
- ✅ **Langflow**: Running at http://localhost:7860
- ⚠️ **Integration**: Disabled (needs valid API keys)
- ✅ **Data Persistence**: Configured (data stored in `./data/postgres/`)

## 📋 Step-by-Step Setup

### Step 1: Access Langfuse

1. Open your browser and go to: **http://localhost:3000**
2. You should see the Langfuse welcome/login page

### Step 2: Create Your First Account

1. Click **"Sign Up"** or **"Create Account"**
2. Fill in:
   - **Email**: your-email@example.com
   - **Password**: Choose a strong password
   - **Name**: Your Name
3. Click **"Create Account"**
4. You'll be logged in automatically

### Step 3: Create a Project

1. After logging in, you'll see the dashboard
2. Click **"New Project"** or **"Create Project"**
3. Enter project details:
   - **Name**: `Langflow Observability` (or any name you prefer)
   - **Description**: `Tracing for Langflow workflows` (optional)
4. Click **"Create"**

### Step 4: Get Your API Keys

1. In your newly created project, look for **"Settings"** (usually in the sidebar or top menu)
2. Navigate to **"API Keys"** section
3. You'll see:
   - **Public Key** (starts with `pk-lf-...`)
   - **Secret Key** (starts with `sk-lf-...`)
4. **Copy both keys** - you'll need them in the next step

### Step 5: Update Langflow Configuration

Open the file: `c:\Users\tamil\repo\tamilsmtp\dockers\langflow\docker-compose.yml`

Find these lines (around line 34-37):
```yaml
# Langfuse integration (commented out - enable after creating project in Langfuse)
# LANGFUSE_SECRET_KEY: sk-lf-87ae8f58-4ea7-47b3-9f38-9be6938b27bc
# LANGFUSE_PUBLIC_KEY: pk-lf-4943ac35-1532-477d-968a-2dafcbac229a
# LANGFUSE_HOST: http://host.docker.internal:3000
```

**Uncomment and replace** with your actual keys:
```yaml
# Langfuse integration
LANGFUSE_SECRET_KEY: sk-lf-YOUR-ACTUAL-SECRET-KEY-HERE
LANGFUSE_PUBLIC_KEY: pk-lf-YOUR-ACTUAL-PUBLIC-KEY-HERE
LANGFUSE_HOST: http://host.docker.internal:3000
```

**Example** (with fake keys):
```yaml
# Langfuse integration
LANGFUSE_SECRET_KEY: sk-lf-a1b2c3d4-e5f6-7890-abcd-ef1234567890
LANGFUSE_PUBLIC_KEY: pk-lf-x9y8z7w6-v5u4-3210-zyxw-vu9876543210
LANGFUSE_HOST: http://host.docker.internal:3000
```

### Step 6: Restart Langflow

```bash
cd c:\Users\tamil\repo\tamilsmtp\dockers\langflow
docker compose restart langflow
```

Wait 30-60 seconds for Langflow to restart.

### Step 7: Verify Integration

1. **Open Langflow**: http://localhost:7860
2. **Create a simple workflow**:
   - Add a "Chat Input" component
   - Add an "OpenAI" or "Chat Output" component
   - Connect them
3. **Run the workflow**
4. **Check Langfuse**: http://localhost:3000
   - Go to your project
   - Click on **"Traces"** in the sidebar
   - You should see your workflow execution!

## 🎉 What You'll Get

Once integrated, you'll have:

### 📊 **Traces**
- See every workflow execution
- View input/output for each step
- Understand the flow of data

### ⏱️ **Performance Metrics**
- Execution time for each component
- Total workflow duration
- Identify bottlenecks

### 💰 **Cost Tracking**
- Token usage per execution
- API costs (if using OpenAI, Anthropic, etc.)
- Budget monitoring

### 🐛 **Debugging**
- See errors and exceptions
- Trace back to the exact step that failed
- View full context and variables

### 📈 **Analytics**
- Usage patterns over time
- Most used workflows
- Success/failure rates

## 🔍 Example: What a Trace Looks Like

When you run a workflow in Langflow, Langfuse will show:

```
Trace: Chat Workflow Execution
├─ Input: "What is the weather today?"
├─ OpenAI Call
│  ├─ Model: gpt-4
│  ├─ Tokens: 150
│  ├─ Cost: $0.003
│  └─ Duration: 1.2s
└─ Output: "I don't have access to real-time weather..."
```

## ⚠️ Troubleshooting

### Still getting 403 errors?

1. **Double-check the keys**:
   - Make sure you copied them correctly
   - No extra spaces or quotes
   - Keys should start with `sk-lf-` and `pk-lf-`

2. **Verify Langfuse is running**:
   ```bash
   cd c:\Users\tamil\repo\tamilsmtp\dockers\langfuse
   docker compose ps
   ```

3. **Check the project exists**:
   - Log in to Langfuse at http://localhost:3000
   - Verify the project is there
   - Verify the keys are from the correct project

4. **Restart both services**:
   ```bash
   # Restart Langfuse
   cd c:\Users\tamil\repo\tamilsmtp\dockers\langfuse
   docker compose restart langfuse
   
   # Restart Langflow
   cd c:\Users\tamil\repo\tamilsmtp\dockers\langflow
   docker compose restart langflow
   ```

### No traces appearing?

1. **Wait a few seconds** - traces may take 5-10 seconds to appear
2. **Refresh the Langfuse page**
3. **Check you're in the correct project**
4. **Verify the workflow actually ran** in Langflow

## 📝 Quick Commands Reference

```bash
# Check if Langfuse is running
cd c:\Users\tamil\repo\tamilsmtp\dockers\langfuse
docker compose ps

# Check if Langflow is running
cd c:\Users\tamil\repo\tamilsmtp\dockers\langflow
docker compose ps

# View Langflow logs
docker compose logs -f langflow

# Restart Langflow after config change
docker compose restart langflow
```

## 🎯 Next Steps After Setup

1. **Create workflows** in Langflow
2. **Run them** and see traces in Langfuse
3. **Analyze** performance and costs
4. **Optimize** based on insights
5. **Monitor** production usage

## 📚 Additional Resources

- **Langfuse Docs**: https://langfuse.com/docs
- **Langflow Docs**: https://docs.langflow.org
- **Tracing Guide**: https://langfuse.com/docs/tracing

---

**Ready to enable observability?** Follow the steps above and you'll have full visibility into your Langflow workflows! 🚀
