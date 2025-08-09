
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

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/secure-upload-v1.git
   cd secure-upload-v1
   ```

2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Deploy with Serverless:

   ```bash
   sam build
   sam deploy -guided
   ```

---

## 🧪 API Endpoints

### 1. Generate Upload Token

```
POST /generate-token
Body: { "client_id": "ABC123" }
Response: { "token": "RX8G73KL", "upload_url": "/upload-url/RX8G73KL" }
```

---

### 2. Get Presigned Upload URL

```
GET /upload-url/{token}?ext=pdf&contentType=application/pdf
Returns: { upload_url, filename, content_type }
```

---

### 3. Upload File (Client uses returned URL)

```js
await fetch(upload_url, {
  method: 'PUT',
  headers: { 'Content-Type': content_type },
  body: fileBlob
});
```

---

### 4. Confirm Upload

```
POST /upload/confirm/{token}
Body: { "filename": "abc123.pdf", "content_type": "application/pdf" }
```

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

