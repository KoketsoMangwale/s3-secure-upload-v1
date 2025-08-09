## 🚀 Secure Serverless Document Upload System

This project is a fully serverless, token-based file upload system built on AWS. It allows clients to securely upload sensitive documents via a unique, anonymous link using presigned S3 URLs. This system is ideal for privacy-sensitive applications in healthtech, fintech, and legal tech.

### Key Features ⚙️

* **Anonymous and Secure:** The system supports anonymous, secure document uploads with no login required.
* **One-time Tokens:** It uses one-time tokens mapped to client IDs to manage uploads.
* **Direct-to-S3 Uploads:** Files are uploaded directly to S3 via presigned URLs.
* **Metadata Logging:** Upload metadata, such as file name, type, and timestamp, is logged.
* **GDPR Compliant:** The system is GDPR-compliant, using HTTPS-only communication, encrypted S3 storage, and no PII in URLs.

### How It Works 🛠️

The system is built using the following AWS services and technologies:
* **AWS Lambda**: For serverless compute.
* **API Gateway**: To provide REST endpoints.
* **S3**: For encrypted document storage.
* **DynamoDB**: To store tokens and upload logs.
* **Python 3.11**: The programming language used.
* **Serverless Framework**: For deployment.

The workflow involves four main API endpoints:
1.  **Generate Upload Token:** A token and upload URL are generated for a `client_id`.
2.  **Get Presigned Upload URL:** The client uses the token to get a presigned S3 URL.
3.  **Upload File:** The client uses the presigned URL to directly upload the file to S3.
4.  **Confirm Upload:** The client confirms the upload, logging the file metadata.

### Getting Started 🚀

To get started, you'll need Node.js, npm, Python 3.11+, and the AWS CLI configured.
1.  Install the Serverless Framework: `npm install -g serverless`.
2.  Clone the repository: `git clone https://github.com/your-username/s3-secure-upload-v1.git`.
3.  Install dependencies: `pip install -r requirements.txt`.
4.  Deploy using the Serverless Framework: `sam build` followed by `sam deploy --guided`.


---

### Future Enhancements:
- Optional Email Notification: The system could be enhanced to send optional email notifications, possibly using Amazon SES
- Expiring Upload Tokens: The tokens could be configured to expire automatically using DynamoDB's Time to Live (TTL) feature
- 
