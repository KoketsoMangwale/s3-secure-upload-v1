
# 🔐 Secure Serverless Document Upload System

This project is a fully serverless, token-based file upload system built on AWS. It allows clients to **securely upload sensitive documents via a unique, anonymous link**, using **presigned S3 URLs**. Ideal for healthtech, fintech, legal tech, and other privacy-sensitive applications.

---

## ⚙️ Features

✅ Anonymous, secure document uploads  
✅ One-time tokens mapped to client IDs  
✅ Mobile-friendly — no login required  
✅ Files go **directly to S3** via presigned URLs  
✅ Upload metadata (file name, type, timestamp) is logged  
✅ GDPR-compliant: HTTPS-only, encrypted S3 storage, and no PII in URLs

---

## 🏗️ Built With

- [AWS Lambda](https://aws.amazon.com/lambda/) – Serverless compute
- [API Gateway](https://aws.amazon.com/api-gateway/) – REST endpoints
- [S3](https://aws.amazon.com/s3/) – Encrypted document storage
- [DynamoDB](https://aws.amazon.com/dynamodb/) – Token and upload log store
- [Python 3.11](https://www.python.org/)
- [Serverless Framework](https://www.serverless.com/)

---

## 📁 Project Structure

```

secure-upload/
├── handler/
│   ├── generate_token.py        # Generate upload tokens
│   ├── get_presigned_url.py     # Get signed S3 upload URLs
│   └── confirm_upload.py        # Log file metadata after upload
├── serverless.yml               # Serverless deployment config
├── requirements.txt             # Python dependencies
└── README.md

````

---

## 🚀 Getting Started

### Prerequisites

- Node.js & npm
- Python 3.11+
- AWS CLI configured (`aws configure`)
- Serverless Framework installed:
```bash
  npm install -g serverless
```

---
> __Please note that the name of S3 bucket must be unique, otherwise the deployment of the stack (template) will fail.__
---
### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/s3-secure-upload-v1.git
   cd s3-secure-upload-v1
   ```

2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Deploy with Serverless:

   ```bash
   sam build
   sam deploy --guided
   ```
* Stack Name: `sam-s3-secure-upload`
* AWS Region: e.g. `us-west-2`
* Confirm changes before deploy [y/N]: N
* Allow SAM CLI IAM role creation [Y/n]: Y
* Disable rollback [y/N]: N
* GenerateTokenFunction has no authentication. Is this okay? [y/N]: y
* PresignedURLFunction has no authentication. Is this okay? [y/N]: y
* ConfirmUploadFunction has no authentication. Is this okay? [y/N]: y
* Save arguments to configuration file [Y/n]: Y
* SAM configuration file [samconfig.toml]: samconfig.toml
* SAM configuration environment [default]: default
  
---

## 🧪 API Endpoints

### 1. Generate Upload Token

```
curl -X POST https://xxxxxxxxxx.execute-api.us-west-2.amazonaws.com/Prod/generate-token \
  -H "Content-Type: application/json" \
  -d '{"client_id": "ABC123"}'
```

```
Response:
{
"token": "224DB687",
"upload_url": "/upload-url/224DB687",
"expires_at": "2025-08-12T15:25:46.203808"
}
```
---

s3-secure-uploadPresignedURL Policy (executionRole)
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Statement1",
            "Effect": "Allow",
            "Action": [
                "dynamodb:GetItem",
                "dynamodb:PutItem",
                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:dynamodb:af-south-1:XXXXXXXXXXXX:table/SecureUploadTokens",
                "arn:aws:dynamodb:us-west-2:XXXXXXXXXXXX:table/SecureUploadLogs"
                "arn:aws:s3:::secure-upload-bucket-kbm/*"
            ]
        }
    ]
}
```

### 2. Get Presigned Upload URL
From the response in step 1. Replace the token in the endpoint below
```
curl https://mhiinugqqd.execute-api.us-west-2.amazonaws.com/Prod/upload-url/{token}
```
Response:

```
(
"upload_url": `Presigned URL`
"filename": "3cfa01a2bbab42249161187fd18a7047.bin", 
"key": "uploads/3cfa01a2bbab42249161187fd18a7047.bin", 
"content_type": "application/octet-stream"
}
```
---

### 3. Upload File (Client uses returned URL)
Using the `Presigned URL` from the response of the previous GET request, go to a browser, paste the URL 
```
curl -X PUT -H "Content-Type: application/octet-stream" -T myfile.txt `Presigned URL`

```

---

### 4. Confirm Upload

```
curl -X POST https://mhiinugqqd.execute-api.us-west-2.amazonaws.com/Prod/upload/confirm/224DB687 \
-H "Content-Type: application/json" \
-d '{"filename": "3cfa01a2bbab42249161187fd18a7047.bin", "content_type": "application/octet-stream"}'
```
Response:

`{"message": "Upload confirmed"}`

---

## 🔐 Security & Compliance

* ✅ AES256 encryption for all S3 uploads
* ✅ Tokens expire after 3 days
* ✅ HTTPS-only deployment
* ✅ IAM roles enforce least privilege
* ✅ No personal info in file paths or URLs

---

## 📌 To Do

* [ ] Optional email notification (SES)
* [ ] Expiring upload tokens (Dynamo TTL)
* [ ] Admin dashboard for reviewing uploads

---

## 🧑‍💻 Author

**Your Name**
[LinkedIn](https://www.linkedin.com/in/yourprofile) · [GitHub](https://github.com/your-username)

---

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).

```

---

