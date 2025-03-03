# Template

# Reusable
ibmcloud target -r us-south -g code-engine-6920005y08-0tklyx1k

ibmcloud ce project select --id 83db9261-78d2-496f-a96b-27256b5dde49
# ibmcloud ce registry create --name ibm-container-registry-3 --server us.icr.io --username iamapikey --password "$IBM_API_KEY"
# ibmcloud ce secret create --name env-6-u --from-env-file ../notebook/.env
ibmcloud ce application create --name watsonx-uem-v2 --build-source . --build-size xlarge --build-timeout 1200 --cpu 2 --memory 4G --min-scale 1 --max-sscale 1 --port 8080 --registry-secret ibm-container-registry-3 --image us.icr.io/cc-6920005y08-jpalca03-cr/watsonx-uem-v2:latest --env-from-secret env-u-6