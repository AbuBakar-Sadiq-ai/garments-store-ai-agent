"""
AI Agent for Garments Store
Uses LangChain and OpenAI to handle customer interactions
"""

import os
import json
from typing import Any
from dotenv import load_dotenv
from store_database import GarmentsStore, OrderItem
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.llms import OpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

load_dotenv()

# Initialize store
store = GarmentsStore()

# Initialize LLM
llm = OpenAI(
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY"),
    callbacks=[StreamingStdOutCallbackHandler()]
)


# ==================== TOOL DEFINITIONS ====================

def search_products(query: str) -> str:
    """
    Search for products in the store by name, category, or keywords.
    
    Args:
        query: Search term (e.g., "blue jeans", "shirts", "casual wear")
    
    Returns:
        A formatted string with search results
    """
    results = store.search_products(query)
    
    if not results:
        return f"No products found matching '{query}'. Try searching for categories like: {', '.join(store.get_available_categories())}"
    
    response = f"Found {len(results)} product(s) matching '{query}':\n\n"
    for i, product in enumerate(results, 1):
        response += f"{i}. {product.name}\n"
        response += f"   Price: ${product.price:.2f}\n"
        response += f"   Category: {product.category}\n"
        response += f"   Rating: {product.rating}/5.0\n"
        response += f"   Product ID: {product.id}\n\n"
    
    return response


def get_product_details(product_id: str) -> str:
    """
    Get detailed information about a specific product.
    
    Args:
        product_id: The ID of the product (e.g., "P001")
    
    Returns:
        Detailed product information
    """
    product_info = store.get_product_info(product_id)
    
    if not product_info:
        return f"Product with ID '{product_id}' not found."
    
    response = f"\n=== {product_info['name']} ===\n"
    response += f"Price: ${product_info['price']}\n"
    response += f"Category: {product_info['category']}\n"
    response += f"Description: {product_info['description']}\n"
    response += f"Rating: {product_info['rating']}/5.0\n"
    response += f"Available Sizes: {', '.join(product_info['available_sizes'])}\n"
    response += f"Available Colors: {', '.join(product_info['available_colors'])}\n"
    response += f"Stock by Size:\n"
    
    for size, qty in product_info['stock'].items():
        response += f"  - {size}: {qty} units\n"
    
    return response


def check_stock(product_id: str, size: str) -> str:
    """
    Check if a product is available in a specific size.
    
    Args:
        product_id: The product ID
        size: The size (e.g., "M", "32", "XL")
    
    Returns:
        Stock availability information
    """
    is_available = store.check_stock(product_id, size)
    product = store.get_product_by_id(product_id)
    
    if not product:
        return f"Product '{product_id}' not found."
    
    stock_count = product.stock.get(size, 0)
    
    if is_available:
        return f"✓ {product.name} in size {size} is IN STOCK ({stock_count} units available)."
    else:
        return f"✗ {product.name} in size {size} is OUT OF STOCK."


def browse_category(category: str) -> str:
    """
    Browse all products in a specific category.
    
    Args:
        category: The product category (e.g., "Tops", "Bottoms", "Outerwear")
    
    Returns:
        List of products in the category
    """
    products = store.get_products_by_category(category)
    
    if not products:
        available_cats = ", ".join(store.get_available_categories())
        return f"No products found in category '{category}'. Available categories: {available_cats}"
    
    response = f"\n=== Products in '{category}' Category ===\n"
    for i, product in enumerate(products, 1):
        response += f"{i}. {product.name} - ${product.price:.2f} (ID: {product.id})\n"
    
    return response


def place_order(product_id: str, size: str, color: str, quantity: int, customer_name: str, email: str, delivery_address: str) -> str:
    """
    Place an order for a product.
    
    Args:
        product_id: The product ID
        size: The size to order
        color: The color to order
        quantity: Number of items (default 1)
        customer_name: Full name of the customer
        email: Email address
        delivery_address: Shipping address
    
    Returns:
        Order confirmation details
    """
    if not customer_name or not email or not delivery_address:
        return "Error: Please provide customer name, email, and delivery address to place an order."
    
    items = [{
        'product_id': product_id,
        'size': size,
        'color': color,
        'quantity': quantity
    }]
    
    order = store.create_order(
        customer_name=customer_name,
        email=email,
        items=items,
        delivery_address=delivery_address
    )
    
    if not order:
        return f"Order failed. Please verify the product ID, size, and quantity are correct."
    
    response = f"\n✓ ORDER CONFIRMED!\n"
    response += f"Order ID: {order.order_id}\n"
    response += f"Customer: {order.customer_name}\n"
    response += f"Email: {order.email}\n"
    response += f"Delivery Address: {order.delivery_address}\n"
    response += f"Items: {len(order.items)} item(s)\n"
    response += f"Total: ${order.total_price:.2f}\n"
    response += f"Status: {order.status}\n"
    
    return response


def get_order_status(order_id: str) -> str:
    """
    Get the status of an existing order.
    
    Args:
        order_id: The order ID (e.g., "ORD1000")
    
    Returns:
        Order status information
    """
    order_info = store.get_order_status(order_id)
    
    if not order_info:
        return f"Order '{order_id}' not found."
    
    response = f"\n=== Order Status ===\n"
    response += f"Order ID: {order_info['order_id']}\n"
    response += f"Customer: {order_info['customer_name']}\n"
    response += f"Status: {order_info['status'].upper()}\n"
    response += f"Items: {order_info['items_count']}\n"
    response += f"Total: {order_info['total_price']}\n"
    response += f"Created: {order_info['created_at']}\n"
    
    return response


def get_store_info() -> str:
    """
    Get general information about the store.
    
    Returns:
        Store summary and available categories
    """
    summary = store.get_store_summary()
    
    response = f"\n=== Fashion Garments Store ===\n"
    response += f"Total Products: {summary['total_products']}\n"
    response += f"Total Stock Items: {summary['total_stock_items']}\n"
    response += f"Total Orders: {summary['total_orders']}\n"
    response += f"Total Revenue: {summary['total_revenue']}\n"
    response += f"Categories: {', '.join(summary['categories'])}\n"
    
    return response


# ==================== CREATE TOOLS ====================

tools = [
    Tool(
        name="search_products",
        func=search_products,
        description="Search for products in the store. Use this when customer wants to find specific items or browse by keyword."
    ),
    Tool(
        name="get_product_details",
        func=get_product_details,
        description="Get detailed information about a specific product including price, description, sizes, colors, and stock. Requires product ID."
    ),
    Tool(
        name="check_stock",
        func=check_stock,
        description="Check if a product is in stock in a specific size. Provide product ID and size."
    ),
    Tool(
        name="browse_category",
        func=browse_category,
        description="Browse all products in a category. Use categories like: Tops, Bottoms, Dresses, Outerwear, Activewear."
    ),
    Tool(
        name="place_order",
        func=place_order,
        description="Place an order. Requires: product_id, size, color, quantity, customer_name, email, and delivery_address."
    ),
    Tool(
        name="get_order_status",
        func=get_order_status,
        description="Get the status of an existing order using order ID."
    ),
    Tool(
        name="get_store_info",
        func=get_store_info,
        description="Get general store information including total products, stock, and categories."
    )
]


# ==================== INITIALIZE AGENT ====================

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    max_iterations=10,
    early_stopping_method="generate"
)

# System prompt for the agent
agent.agent.llm_chain.prompt.template = """
You are a helpful fashion store customer service assistant. You help customers find clothes, check availability, and place orders.

You have access to the following tools:
{tools}

Be friendly, professional, and helpful. Always:
1. Search for products when customers ask about specific items
2. Provide product details including price, sizes, and colors
3. Check stock availability before confirming orders
4. Help customers place orders by collecting necessary information
5. Follow up on order status requests

When placing orders, always confirm you have:
- Product ID and details
- Size and color selection
- Customer name, email, and delivery address

Make recommendations when appropriate.

Question: {input}

{agent_scratchpad}
"""


def run_agent(user_input: str) -> str:
    """
    Run the agent with user input and return the response.
    """
    try:
        response = agent.run(user_input)
        return response
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Welcome to Fashion Garments Store AI Assistant")
    print("="*60)
    print("\nI'm here to help you find and order the perfect garments!")
    print("Type 'quit' or 'exit' to end the conversation.\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit']:
            print("\nThank you for visiting our store! Goodbye!")
            break
        
        if not user_input:
            continue
        
        print("\nAssistant: ", end="")
        response = run_agent(user_input)
        print(f"\n{response}\n")
