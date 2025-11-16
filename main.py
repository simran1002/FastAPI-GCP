from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import httpx
import os
from google import genai
from google.genai.types import HttpOptions

app = FastAPI(
    title="Paci FinTech API",
    description="FastAPI application with Fake Store API wrapper and Gemini chat integration",
    version="1.0.0"
)

GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "")
GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

if GOOGLE_CLOUD_PROJECT:
    os.environ["GOOGLE_CLOUD_PROJECT"] = GOOGLE_CLOUD_PROJECT
    os.environ["GOOGLE_CLOUD_LOCATION"] = GOOGLE_CLOUD_LOCATION
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

GOOGLE_APPLICATION_CREDENTIALS_JSON = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON", "")
if GOOGLE_APPLICATION_CREDENTIALS_JSON:
    import json
    import tempfile
    creds_data = json.loads(GOOGLE_APPLICATION_CREDENTIALS_JSON)
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        json.dump(creds_data, f)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = f.name

FAKE_STORE_API_URL = "https://fakestoreapi.com"

gemini_client = None


def get_gemini_client():
    global gemini_client
    if gemini_client is None:
        try:
            gemini_client = genai.Client(http_options=HttpOptions(api_version="v1"))
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize Gemini client: {str(e)}. Make sure Vertex AI API is enabled and credentials are configured."
            )
    return gemini_client


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


class CartItem(BaseModel):
    productId: int
    quantity: int


class AddToCartRequest(BaseModel):
    userId: int
    products: List[CartItem]


@app.get("/")
def read_root():
    return {
        "message": "Welcome to Paci FinTech API",
        "endpoints": {
            "/hello": "Hello World endpoint",
            "/products": "List all products from Fake Store",
            "/carts": "List all carts",
            "/carts/add": "Add item to cart",
            "/chat": "Chat with Gemini AI"
        }
    }


@app.get("/hello")
def hello_world():
    return {"message": "Hello World"}


@app.get("/products")
async def get_all_products():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{FAKE_STORE_API_URL}/products")
            response.raise_for_status()
            products = response.json()
            return JSONResponse(content=products)
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching products from Fake Store API: {str(e)}"
        )


@app.get("/products/{product_id}")
async def get_product(product_id: int):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{FAKE_STORE_API_URL}/products/{product_id}")
            response.raise_for_status()
            product = response.json()
            return JSONResponse(content=product)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Product not found")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching product: {str(e)}"
        )
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching product: {str(e)}"
        )


@app.get("/carts")
async def get_all_carts():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{FAKE_STORE_API_URL}/carts")
            response.raise_for_status()
            carts = response.json()
            return JSONResponse(content=carts)
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching carts from Fake Store API: {str(e)}"
        )


@app.get("/carts/{cart_id}")
async def get_cart(cart_id: int):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{FAKE_STORE_API_URL}/carts/{cart_id}")
            response.raise_for_status()
            cart = response.json()
            return JSONResponse(content=cart)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Cart not found")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching cart: {str(e)}"
        )
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching cart: {str(e)}"
        )


@app.post("/carts/add")
async def add_to_cart(cart_request: AddToCartRequest):
    try:
        cart_data = {
            "userId": cart_request.userId,
            "products": [
                {
                    "productId": item.productId,
                    "quantity": item.quantity
                }
                for item in cart_request.products
            ]
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{FAKE_STORE_API_URL}/carts",
                json=cart_data
            )
            response.raise_for_status()
            cart = response.json()
            return JSONResponse(content=cart, status_code=201)
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error adding to cart: {str(e)}"
        )


@app.post("/chat", response_model=ChatResponse)
async def chat_with_gemini(chat_request: ChatRequest):
    try:
        client = get_gemini_client()
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=chat_request.message,
        )
        
        return ChatResponse(response=response.text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error communicating with Gemini API: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

