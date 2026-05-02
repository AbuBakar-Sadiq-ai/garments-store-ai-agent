"""
REST API for the Garments Store AI Agent
Exposes the agent functionality through HTTP endpoints
"""

import os
from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from agent import run_agent
from store_database import GarmentsStore

load_dotenv()

app = FastAPI(
    title="Fashion Garments Store API",
    description="AI-powered REST API for the garments store",
    version="1.0.0"
)

store = GarmentsStore()


# ==================== REQUEST/RESPONSE MODELS ====================

class ChatMessage(BaseModel):
    """Model for chat messages"""
    message: str


class ChatResponse(BaseModel):
    """Response model for chat"""
    user_message: str
    assistant_response: str


class ProductSearchRequest(BaseModel):
    """Request model for product search"""
    query: str


class ProductInfo(BaseModel):
    """Product information response"""
    id: str
    name: str
    category: str
    price: str
    description: str
    available_sizes: List[str]
    available_colors: List[str]
    rating: float


class OrderRequest(BaseModel):
    """Request model for placing an order"""
    product_id: str
    size: str
    color: str
    quantity: int = 1
    customer_name: str
    email: str
    delivery_address: str


class OrderResponse(BaseModel):
    """Response model for order confirmation"""
    order_id: str
    customer_name: str
    total_price: float
    status: str
    items_count: int


class StoreInfoResponse(BaseModel):
    """Store information response"""
    total_products: int
    total_stock_items: int
    categories: List[str]


# ==================== ENDPOINTS ====================

@app.get("/")
async def root():
    """Root endpoint with welcome message"""
    return {
        "message": "Welcome to Fashion Garments Store API",
        "version": "1.0.0",
        "documentation": "/docs"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/chat")
async def chat(request: ChatMessage) -> ChatResponse:
    """
    Chat with the AI agent about products and orders.
    
    Example: "Show me blue jeans" or "I want to order a white t-shirt"
    """
    if not request.message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    response = run_agent(request.message)
    
    return ChatResponse(
        user_message=request.message,
        assistant_response=response
    )


@app.get("/products/search")
async def search_products(query: str):
    """
    Search for products by name, category, or keywords.
    
    Query params:
    - query: Search term (e.g., "jeans", "shirts", "blue")
    """
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter required")
    
    results = store.search_products(query)
    
    return {
        "query": query,
        "total_results": len(results),
        "products": [
            {
                "id": p.id,
                "name": p.name,
                "category": p.category,
                "price": p.price,
                "description": p.description,
                "rating": p.rating
            }
            for p in results
        ]
    }


@app.get("/products/{product_id}")
async def get_product(product_id: str):
    """
    Get detailed information about a specific product.
    
    Path params:
    - product_id: The product ID (e.g., "P001")
    """
    product_info = store.get_product_info(product_id)
    
    if not product_info:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    
    return product_info


@app.get("/products/category/{category}")
async def get_category_products(category: str):
    """
    Get all products in a specific category.
    
    Path params:
    - category: Product category (e.g., "Tops", "Bottoms")
    """
    products = store.get_products_by_category(category)
    
    if not products:
        raise HTTPException(status_code=404, detail=f"No products in category {category}")
    
    return {
        "category": category,
        "total_products": len(products),
        "products": [
            {
                "id": p.id,
                "name": p.name,
                "price": p.price,
                "description": p.description
            }
            for p in products
        ]
    }


@app.get("/stock/{product_id}/{size}")
async def check_stock(product_id: str, size: str):
    """
    Check stock availability for a product in a specific size.
    
    Path params:
    - product_id: The product ID
    - size: The size (e.g., "M", "32", "XL")
    """
    is_available = store.check_stock(product_id, size)
    product = store.get_product_by_id(product_id)
    
    if not product:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    
    stock_count = product.stock.get(size, 0)
    
    return {
        "product_id": product_id,
        "product_name": product.name,
        "size": size,
        "in_stock": is_available,
        "stock_count": stock_count
    }


@app.get("/categories")
async def get_categories():
    """
    Get all available product categories.
    """
    categories = store.get_available_categories()
    
    return {
        "total_categories": len(categories),
        "categories": categories
    }


@app.post("/orders")
async def create_order(request: OrderRequest) -> OrderResponse:
    """
    Create a new order.
    
    Request body:
    - product_id: Product ID to order
    - size: Size selection
    - color: Color selection
    - quantity: Number of items (default: 1)
    - customer_name: Full name
    - email: Email address
    - delivery_address: Shipping address
    """
    items = [{
        'product_id': request.product_id,
        'size': request.size,
        'color': request.color,
        'quantity': request.quantity
    }]
    
    order = store.create_order(
        customer_name=request.customer_name,
        email=request.email,
        items=items,
        delivery_address=request.delivery_address
    )
    
    if not order:
        raise HTTPException(status_code=400, detail="Failed to create order. Check product ID, size, and stock.")
    
    return OrderResponse(
        order_id=order.order_id,
        customer_name=order.customer_name,
        total_price=order.total_price,
        status=order.status,
        items_count=len(order.items)
    )


@app.get("/orders/{order_id}")
async def get_order(order_id: str):
    """
    Get the status of an order.
    
    Path params:
    - order_id: The order ID (e.g., "ORD1000")
    """
    order_info = store.get_order_status(order_id)
    
    if not order_info:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    
    return order_info


@app.get("/store/info")
async def get_store_info():
    """
    Get general store information.
    """
    summary = store.get_store_summary()
    return summary


# ==================== ERROR HANDLERS ====================

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    return {
        "error": "An unexpected error occurred",
        "detail": str(exc)
    }


if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("Starting Fashion Garments Store API")
    print("="*60)
    print("\nAPI Documentation: http://localhost:8000/docs")
    print("Swagger UI: http://localhost:8000/docs")
    print("ReDoc: http://localhost:8000/redoc\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
