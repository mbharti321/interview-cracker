# Azure Deployment Guide for Toy Insights

## Overview
This guide explains how to deploy the Toy Insights RAG service to Azure.

## Option 1: Azure Container Apps (Recommended)

### Prerequisites
- Azure subscription
- Azure CLI (`az` command)
- Docker (for building images)

### Steps

#### 1. Set Up Azure Resources

```bash
# Login to Azure
az login

# Create resource group
az group create \
  --name toy-insights-rg \
  --location eastus

# Create Azure Container Registry
az acr create \
  --resource-group toy-insights-rg \
  --name toyinsightsacr \
  --sku Basic

# Create Azure Database for PostgreSQL (flexible server)
az postgres flexible-server create \
  --resource-group toy-insights-rg \
  --name toy-insights-db \
  --location eastus \
  --admin-user dbadmin \
  --admin-password '<secure-password>' \
  --database-name toy_insights_db

# Create Azure Cache for Redis
az redis create \
  --resource-group toy-insights-rg \
  --name toy-insights-redis \
  --location eastus \
  --sku Basic \
  --vm-size c0
```

#### 2. Build and Push Docker Image

```bash
# Build Docker image
docker build -f infra/docker/Dockerfile -t toyinsightsacr.azurecr.io/toy-insights:latest .

# Login to ACR
az acr login --name toyinsightsacr

# Push image
docker push toyinsightsacr.azurecr.io/toy-insights:latest
```

#### 3. Deploy to Azure Container Apps

```bash
# Get connection strings
DB_CONNECTION=$(az postgres flexible-server show-connection-string \
  --server-name toy-insights-db \
  --admin-user dbadmin)

REDIS_CONNECTION=$(az redis list-keys \
  --resource-group toy-insights-rg \
  --name toy-insights-redis \
  --query primaryKey -o tsv)

# Create Container Apps environment
az containerapp env create \
  --resource-group toy-insights-rg \
  --name toy-insights-env \
  --location eastus

# Deploy container app
az containerapp create \
  --resource-group toy-insights-rg \
  --name toy-insights-api \
  --environment toy-insights-env \
  --image toyinsightsacr.azurecr.io/toy-insights:latest \
  --target-port 8000 \
  --ingress 'external' \
  --registry-server toyinsightsacr.azurecr.io \
  --registry-identity system \
  --env-vars \
    DATABASE_URL="$DB_CONNECTION" \
    REDIS_HOST="$(az redis show -g toy-insights-rg -n toy-insights-redis --query hostName -o tsv)" \
    REDIS_PORT="6379"
```

## Option 2: Azure App Service

### Alternative for simpler deployments

```bash
# Create App Service Plan
az appservice plan create \
  --name toy-insights-plan \
  --resource-group toy-insights-rg \
  --sku B1 \
  --is-linux

# Create Web App
az webapp create \
  --resource-group toy-insights-rg \
  --plan toy-insights-plan \
  --name toy-insights-app \
  --runtime "PYTHON|3.11"

# Configure deployment
az webapp deployment source config-zip \
  --resource-group toy-insights-rg \
  --name toy-insights-app \
  --src deployment.zip
```

## Secrets Management: Azure Key Vault

### Store Sensitive Configuration

```bash
# Create Key Vault
az keyvault create \
  --resource-group toy-insights-rg \
  --name toy-insights-vault

# Store secrets
az keyvault secret set \
  --vault-name toy-insights-vault \
  --name DATABASE-URL \
  --value "postgresql://..."

az keyvault secret set \
  --vault-name toy-insights-vault \
  --name REDIS-PASSWORD \
  --value "your-redis-password"

# Grant Container App access to Key Vault
az keyvault set-policy \
  --vault-name toy-insights-vault \
  --object-id <container-app-identity-id> \
  --secret-permissions get list
```

### Update Application Code to Use Key Vault

```python
# In src/api/main.py or env loading:
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
vault_url = "https://toy-insights-vault.vault.azure.net/"
client = SecretClient(vault_url=vault_url, credential=credential)

database_url = client.get_secret("DATABASE-URL").value
redis_password = client.get_secret("REDIS-PASSWORD").value
```

## Advanced: Using Azure AI Search Instead of FAISS

### Replace local vector store with Azure AI Search

1. **Create Azure AI Search Service:**
```bash
az search service create \
  --resource-group toy-insights-rg \
  --name toy-insights-search \
  --sku basic \
  --location eastus
```

2. **Update vectorstore.py:**

```python
# Replace FAISS with Azure AI Search client
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient

class AzureVectorStore:
    def __init__(self, service_name: str, index_name: str, api_key: str):
        self.endpoint = f"https://{service_name}.search.windows.net"
        self.client = SearchClient(
            endpoint=self.endpoint,
            index_name=index_name,
            credential=api_key
        )
    
    def add(self, embeddings, metadata):
        # Index embeddings with Azure AI Search
        pass
    
    def search(self, query_embedding, k: int = 5):
        # Use Azure AI Search vector search
        pass
```

## Monitoring & Logging

### Enable Application Insights

```bash
# Create Application Insights
az monitor app-insights component create \
  --resource-group toy-insights-rg \
  --app toy-insights-insights \
  --location eastus

# Link to Container App
az containerapp update \
  --resource-group toy-insights-rg \
  --name toy-insights-api \
  --instrumentation-key <instrumentation-key>
```

### View Logs

```bash
# Stream logs
az containerapp logs show \
  --resource-group toy-insights-rg \
  --name toy-insights-api \
  --follow

# Query Application Insights
az monitor app-insights metrics show \
  --resource-group toy-insights-rg \
  --app toy-insights-insights \
  --metric "requests/count"
```

## Scaling

```bash
# Scale Container App
az containerapp update \
  --resource-group toy-insights-rg \
  --name toy-insights-api \
  --min-replicas 2 \
  --max-replicas 10
```

## Cost Optimization

- Use **Azure Container Registry** for private image storage
- Use **Azure Database for PostgreSQL Flexible Server** for managed database
- Use **Azure Cache for Redis** for distributed caching
- Consider **Reserved Instances** for long-running services

## Troubleshooting

### Container won't start
```bash
az containerapp logs show \
  --resource-group toy-insights-rg \
  --name toy-insights-api
```

### Database connection issues
```bash
# Verify firewall rules
az postgres flexible-server firewall-rule list \
  --resource-group toy-insights-rg \
  --name toy-insights-db
```

### Redis connectivity
```bash
# Test Redis connection
redis-cli -h <redis-hostname> -p 6379
```

## Summary

| Component | Azure Service |
|-----------|---|
| Container Orchestration | Azure Container Apps |
| Database | Azure Database for PostgreSQL |
| Cache | Azure Cache for Redis |
| Image Registry | Azure Container Registry |
| Secrets | Azure Key Vault |
| Monitoring | Application Insights |
| Vector Search | Azure AI Search (optional) |

For more details, refer to:
- [Azure Container Apps Documentation](https://learn.microsoft.com/azure/container-apps/)
- [Azure PostgreSQL Flexible Server](https://learn.microsoft.com/azure/postgresql/flexible-server/)
- [Azure Cache for Redis](https://learn.microsoft.com/azure/azure-cache-for-redis/)
- [Azure AI Search](https://learn.microsoft.com/azure/search/)
