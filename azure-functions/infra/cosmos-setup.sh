az cosmosdb sql database create -n myCosmos -g myRg --db-name BillingDB
az cosmosdb sql container create \
  --account-name myCosmos \
  --db-name BillingDB \
  --name RecordsHot \
  --partition-key-path "/pk" \
  --throughput 400

az cosmosdb sql container create \
  --account-name myCosmos \
  --db-name BillingDB \
  --name RecordsCold \
  --partition-key-path "/pk" \
  --throughput 400

az storage account create -n mystorage -g myRg -l eastus --sku Standard_LRS
az storage container create --account-name mystorage --name coldblobs
