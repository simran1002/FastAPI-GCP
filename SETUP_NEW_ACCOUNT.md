# Setup Guide for New GCP Account

## Current Status

- ✅ New account: `simran100yadav@gmail.com`
- ✅ Project created: `paci-fintech-64122`
- ⚠️ Billing account needed

## Next Steps

### 1. Set Up Billing (Required)

New Google Cloud accounts get **$300 free credits**!

**Option A: Link Existing Billing Account**
```bash
gcloud billing accounts list
gcloud billing projects link paci-fintech-64122 --billing-account=BILLING_ACCOUNT_ID
```

**Option B: Create New Billing Account**
1. Go to: https://console.cloud.google.com/billing
2. Click "Create Account"
3. Add payment method
4. Link to project: `paci-fintech-64122`

### 2. Enable APIs

Once billing is set up:
```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable aiplatform.googleapis.com
```

### 3. Deploy

```bash
gcloud builds submit --tag gcr.io/paci-fintech-64122/paci-fintech-api
gcloud run deploy paci-fintech-api \
  --image gcr.io/paci-fintech-64122/paci-fintech-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_CLOUD_PROJECT=paci-fintech-64122,GOOGLE_CLOUD_LOCATION=us-central1
```

## Project Information

- **Project ID**: `paci-fintech-64122`
- **Account**: `simran100yadav@gmail.com`
- **Region**: `us-central1`

## Free Credits

Your new account is eligible for:
- ✅ $300 USD free credits
- ✅ 90 days to use credits
- ✅ No charges unless you exceed credits

