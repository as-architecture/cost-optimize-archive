# Azure Cost Optimization for Billing Records

This repo contains a serverless strategy for archiving billing records from Azure Cosmos DB to reduce costs without impacting APIs or introducing downtime.

## Features
- Serverless archival via Azure Functions
- Blob storage in Parquet format
- Synapse SQL for querying cold data
- Unified API logic to maintain transparency

## Components
- `archive-old-records`: Azure Function for data migration
- `api-layer`: Unified logic to query from Cosmos or Blob
- `infra`: Setup scripts
- `diagrams`: Architecture diagram
```

---
