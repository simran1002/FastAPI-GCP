# Deployment Guide - Following Article Approach

## Prerequisites

1. Google Cloud SDK installed
2. Billing account activated (required for Cloud Run)
3. Project: `paci-fintech-23343`

## Deployment Steps (Following Article)

### Step 1: Initialize Google Cloud SDK
```bash
gcloud init
```
Choose your project: `paci-fintech-23343`

### Step 2: Build Container Image
```bash
gcloud builds submit --tag gcr.io/paci-fintech-23343/paci-fintech-api
```

### Step 3: Deploy to Cloud Run
```bash
gcloud run deploy paci-fintech-api \
  --image gcr.io/paci-fintech-23343/paci-fintech-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_CLOUD_PROJECT=paci-fintech-23343,GOOGLE_CLOUD_LOCATION=us-central1
```

### Or Use the Script
```bash
chmod +x deploy.sh
./deploy.sh
```

## After Deployment

You'll get:
- **API URL**: `https://paci-fintech-api-xxxxx.run.app`
- **Swagger UI**: `https://paci-fintech-api-xxxxx.run.app/docs`

## GitHub Repository Setup

1. Create repository: https://github.com/new
2. Push code:
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

## Note

Billing account must be OPEN before deployment. If you see billing errors:
1. Go to: https://console.cloud.google.com/billing
2. Open billing account
3. Make prepayment if required
4. Wait for activation (up to 24 hours)

