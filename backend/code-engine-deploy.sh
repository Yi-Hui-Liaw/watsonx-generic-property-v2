ibmcloud target -r us-south -g itz-wxo-689aa906629af945d7166d
ibmcloud ce project select --id 08916c27-3b8c-4337-8dbe-e9ba77ffb851
# ibmcloud ce registry create --name ibm-container-registry-property --server us.icr.io --username iamapikey --password USgRw8S3LQOAPNrdgPgTqaJzCOenwjSdRUkTURov7bH2
# ibmcloud ce secret create --name env --from-env-file property_agent/.env
ibmcloud ce build create --name test-build --registry-secret ibm-container-registry-property --build-type local --image us.icr.io/cr-itz-mudd99h1/property-backend --size xxlarge --timeout 1000000000m
ibmcloud ce buildrun submit --build test-build --name test-run --wait

ibmcloud ce application create --name property-demo --cpu 1 --memory 4G --min-scale 1 --max-scale 1 --port 8080 --registry-secret ibm-container-registry-property --image us.icr.io/cr-itz-mudd99h1/property-backend:latest --env-from-secret env


ibmcloud ce application create \
  --name property-demo \
  --cpu 1 \
  --memory 4G \
  --ephemeral-storage 4G \
  --min-scale 1 \
  --max-scale 1 \
  --port 8080 \
  --registry-secret ibm-container-registry-property \
  --image us.icr.io/cr-itz-qneqzwfh/property-backend \
  --env-from-secret env
