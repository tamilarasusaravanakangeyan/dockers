# Langflow + Langfuse Docker Setup - Quick Reference

## 🚀 Quick Start Commands

### Start Langflow
```bash
cd c:\Users\tamil\repo\tamilsmtp\dockers\langflow
docker compose up -d
```

### Check Status
```bash
docker compose ps
docker compose logs -f langflow
```

### Stop Langflow
```bash
docker compose down
```

## 🔗 Access URLs

| Service | URL | Credentials |
|---------|-----|-------------|
| **Langflow** | http://localhost:7860 | admin / admin123 |
| **Langfuse** | http://localhost:3000 | (from langfuse setup) |
| **PostgreSQL** | localhost:5434 | langflow / langflow |

## 🔑 Langfuse Integration Keys

These keys are already configured in the docker-compose.yml:

```
LANGFUSE_SECRET_KEY = "sk-lf-87ae8f58-4ea7-47b3-9f38-9be6938b27bc"
LANGFUSE_PUBLIC_KEY = "pk-lf-4943ac35-1532-477d-968a-2dafcbac229a"
LANGFUSE_HOST = "http://host.docker.internal:3000"
```

## 📊 How Tracing Works

1. **Create a flow in Langflow** at http://localhost:7860
2. **Run the flow** - executions are automatically traced
3. **View traces in Langfuse** at http://localhost:3000
4. **Analyze** performance, costs, and errors

## 🛠️ Troubleshooting

### Langflow won't start
```bash
# Check logs
docker compose logs langflow

# Restart
docker compose restart langflow
```

### Can't connect to Langfuse
```bash
# Verify Langfuse is running
cd c:\Users\tamil\repo\tamilsmtp\dockers\langfuse
docker compose ps

# Check if accessible
curl http://localhost:3000
```

### Database issues
```bash
# Reset database
docker compose down -v
docker compose up -d
```

## 📁 File Structure

```
langflow/
├── docker-compose.yml    # Main configuration
├── README.MD            # Full documentation
├── .env.example         # Environment variables template
└── QUICKSTART.md        # This file
```

## 🔄 Update Langflow

```bash
# Pull latest image
docker compose pull

# Restart with new image
docker compose down
docker compose up -d
```

## 📝 Next Steps

1. ✅ Start Langflow: `docker compose up -d`
2. ✅ Open http://localhost:7860
3. ✅ Login with admin/admin123
4. ✅ Create your first AI workflow
5. ✅ Check traces in Langfuse at http://localhost:3000

## 🎯 Common Use Cases

### Building a Chatbot
1. Open Langflow UI
2. Use the "Basic Prompting" template
3. Configure your LLM (OpenAI, Anthropic, etc.)
4. Test and deploy

### RAG (Retrieval Augmented Generation)
1. Use the "RAG" template
2. Upload your documents
3. Configure embeddings and vector store
4. Test queries

### Agent Workflows
1. Use the "Agent" template
2. Add tools and capabilities
3. Configure decision logic
4. Monitor in Langfuse

## 🔐 Security Notes

**⚠️ For Production:**
- Change default passwords
- Use environment variables for secrets
- Enable SSL/TLS
- Restrict network access
- Regular backups

## 📚 Resources

- **Langflow Docs**: https://docs.langflow.org
- **Langfuse Docs**: https://langfuse.com/docs
- **GitHub Issues**: Report problems in respective repos
