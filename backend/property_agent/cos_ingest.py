#import os
import ibm_boto3
from ibm_botocore.client import Config, ClientError
import json

def main(params):
    
    COS_ENDPOINT="https://s3.us-south.cloud-object-storage.appdomain.cloud"
    COS_API_KEY_ID = "NsZSd9jC6BFC4zFp-WCmHLkPmL1-RK4qHU4fyxfPj3qZ" # eg "W00YixxxxxxxxxxMB-odB-2ySfTrFBIQQWanc--P3byk"
    COS_INSTANCE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/30ee78befc544b3d9602bf8953a14b87:e5a69161-aa1b-40fb-b190-04cc005f77c8:bucket:bucket-pkfzwrbptqqj9jr" # eg "crn:v1:bluemix:public:cloud-object-storage:global:a/3bf0d9003xxxxxxxxxx1c3e97696b71c:d6f04d83-6c4f-4a62-a165-696756d63903::"
    COS_BUCKET_NAME = "bucket-pkfzwrbptqqj9jr"
    
    # Create client connection
    cos_client = ibm_boto3.client("s3",
        ibm_api_key_id=COS_API_KEY_ID,
        ibm_service_instance_id=COS_INSTANCE_CRN,
        config=Config(signature_version="oauth"),
        endpoint_url=COS_ENDPOINT
    )
    
    name = params.get("name", "")
    email = params.get("email", "")
    contact = params.get("contact", "")
    description = params.get("description", "")

    # Create the data payload
    data = {
        "name": name,
        "email": email,
        "contact": contact,
        "description": description,
        "message": "Data saved to Cloud Object Storage"
    }

    # Generate a unique filename
    file_name = f"submission.json"

    try:
        # Upload to COS
        cos_client.put_object(
            Bucket=COS_BUCKET_NAME,
            Key=file_name,
            Body=json.dumps(data),
            ContentType='application/json'
        )
        result = {
            "message": "Data saved to Cloud Object Storage",
            "file": file_name
        }
        status_code = 200
    except Exception as e:
        result = {
            "message": "Failed to write to COS",
            "error": str(e)
        }
        status_code = 500

    return {
        "headers": {
            "Content-Type": "application/json"
        },
        "statusCode": status_code,
        "body": result
    }

if __name__ == "__main__":
    test_input = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "contact": "+1234567890",
        "description": "Testing COS upload"
    }

    result = main(test_input)
    print(json.dumps(result, indent=2))