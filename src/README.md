# Serverless File Processing Pipeline on AWS

A serverless, event-driven file processing pipeline built on AWS using Lambda, S3, SQS, DynamoDB, and SNS — fully automated with CloudFormation (IaC) and GitHub Actions (CI/CD).

---

## How It Works

1. User uploads a file to **S3 bucket**
2. S3 triggers **Lambda #1** (trigger function)
3. Lambda #1 pushes a message to **SQS queue**
4. **Lambda #2** (processor) reads from SQS
5. Lambda #2 saves file metadata to **DynamoDB**
6. Lambda #2 sends an email alert via **SNS**

---

## AWS Services Used

| Service | Purpose |
|---|---|
| S3 | File upload storage with versioning |
| Lambda | Serverless compute (trigger + processor) |
| SQS | Message queue buffer between Lambdas |
| DynamoDB | Metadata storage with TTL auto-cleanup |
| SNS | Email notifications |
| CloudFormation | Infrastructure as Code (IaC) |
| IAM | Least-privilege roles for each Lambda |
| GitHub Actions | CI/CD auto-deployment pipeline |

---

## Project Structure

file-pipeline/
├── src/
│   ├── trigger_lambda.py      # S3 event → SQS
│   └── processor_lambda.py    # SQS → DynamoDB + SNS
├── images/                    # AWS Console screenshots
├── template.yaml              # CloudFormation IaC
├── .github/
│   └── workflows/
│       └── deploy.yml         # GitHub Actions CI/CD
└── README.md

---

## Setup & Deployment

### Prerequisites
- AWS CLI installed and configured
- GitHub account
- AWS account (Free Tier works)

### Step 1 — Clone the repo
```bash
git clone https://github.com/suryak-develop/file-pipeline.git
cd file-pipeline
```

### Step 2 — Deploy all AWS resources
```bash
aws cloudformation deploy \
  --stack-name file-pipeline \
  --template-file template.yaml \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides Email=your@email.com
```

### Step 3 — Upload Lambda code
```bash
powershell Compress-Archive -Path src\trigger_lambda.py -DestinationPath trigger.zip -Force
aws lambda update-function-code --function-name FilePipelineTrigger --zip-file fileb://trigger.zip

powershell Compress-Archive -Path src\processor_lambda.py -DestinationPath processor.zip -Force
aws lambda update-function-code --function-name FilePipelineProcessor --zip-file fileb://processor.zip
```

### Step 4 — Test the pipeline
```bash
aws s3 cp src/trigger_lambda.py s3://file-pipeline-YOUR_ACCOUNT_ID/
```

### Step 5 — Verify in DynamoDB
```bash
aws dynamodb scan --table-name FileMetadata
```

Check your email — you should receive an SNS notification.

---

## AWS Console Screenshots

### CloudFormation Stack
![CloudFormation](images/cloudFormation.png)

### S3 Bucket
![S3](images/s3.png)

### Lambda Functions
![Lambda](images/lambda.png)

### DynamoDB Table
![DynamoDB](images/DynamoDB.png)

### SQS Queue
![SQS](images/sqs.png)

### SNS Topic
![SNS](images/sns.png)

---

## CI/CD Pipeline

Every push to `main` automatically deploys both Lambda functions via GitHub Actions.

Add these secrets to your GitHub repo:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

---

## Resume Bullets

- Designed and deployed a serverless file processing pipeline using AWS Lambda, S3, SQS, SNS and DynamoDB
- Automated full infrastructure provisioning using CloudFormation (IaC), enabling one-command deployment
- Configured IAM roles with least-privilege policies for secure service-to-service communication
- Built a CI/CD pipeline using GitHub Actions to automatically deploy Lambda functions on every push to main
- Tested end-to-end pipeline by uploading files to S3 and verifying records in DynamoDB with SNS alerts