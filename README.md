# Paci FinTech FastAPI Application

FastAPI application with Fake Store API wrapper and Google Vertex AI Gemini chat integration.

## Features

- `/hello` - Hello World endpoint
- `/products` - List all products from Fake Store
- `/carts` - List all carts
- `/carts/add` - Add items to cart
- `/chat` - Chat with Gemini AI

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export GOOGLE_CLOUD_PROJECT=your-project-id
export GOOGLE_CLOUD_LOCATION=us-central1
```

3. Run locally:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

Access Swagger UI at: http://localhost:8080/docs

## Deployment

### Google Cloud Run

```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/paci-fintech-api
gcloud run deploy paci-fintech-api \
  --image gcr.io/YOUR_PROJECT_ID/paci-fintech-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID,GOOGLE_CLOUD_LOCATION=us-central1
```

## API Endpoints

- `GET /hello` - Returns "Hello World"
- `GET /products` - Lists all products
- `GET /products/{id}` - Get single product
- `GET /carts` - Lists all carts
- `GET /carts/{id}` - Get single cart
- `POST /carts/add` - Add items to cart
- `POST /chat` - Chat with Gemini AI

## License

MIT License
