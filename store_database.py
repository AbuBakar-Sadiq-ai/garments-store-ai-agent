"""
Store Database Module
Manages inventory, products, and orders for the garments store
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
import json


@dataclass
class Product:
    """Represents a product in the store"""
    id: str
    name: str
    category: str
    price: float
    description: str
    sizes: List[str]
    colors: List[str]
    stock: Dict[str, int]  # {"S": 10, "M": 5, ...}
    image_url: str = ""
    rating: float = 0.0


@dataclass
class OrderItem:
    """Represents a single item in an order"""
    product_id: str
    product_name: str
    size: str
    color: str
    price: float
    quantity: int


@dataclass
class Order:
    """Represents a complete order"""
    order_id: str
    customer_name: str
    email: str
    items: List[OrderItem]
    total_price: float
    status: str  # pending, confirmed, shipped, delivered
    created_at: datetime
    delivery_address: str = ""


class GarmentsStore:
    """Main store class managing inventory and operations"""

    def __init__(self):
        self.products: Dict[str, Product] = {}
        self.orders: Dict[str, Order] = {}
        self.order_counter = 1000
        self.initialize_inventory()

    def initialize_inventory(self):
        """Initialize the store with sample products"""
        sample_products = [
            Product(
                id="P001",
                name="Blue Denim Jeans",
                category="Bottoms",
                price=59.99,
                description="Classic blue denim jeans, comfortable fit",
                sizes=["28", "30", "32", "34", "36"],
                colors=["Blue"],
                stock={"28": 5, "30": 8, "32": 10, "34": 6, "36": 4},
                rating=4.5
            ),
            Product(
                id="P002",
                name="White T-Shirt",
                category="Tops",
                price=19.99,
                description="Plain white cotton t-shirt, soft and breathable",
                sizes=["XS", "S", "M", "L", "XL", "XXL"],
                colors=["White"],
                stock={"XS": 3, "S": 15, "M": 20, "L": 18, "XL": 10, "XXL": 5},
                rating=4.0
            ),
            Product(
                id="P003",
                name="Black Hoodie",
                category="Tops",
                price=49.99,
                description="Comfortable black hoodie, perfect for casual wear",
                sizes=["S", "M", "L", "XL"],
                colors=["Black"],
                stock={"S": 8, "M": 12, "L": 10, "XL": 6},
                rating=4.7
            ),
            Product(
                id="P004",
                name="Summer Dress",
                category="Dresses",
                price=79.99,
                description="Colorful summer dress, light and breezy",
                sizes=["XS", "S", "M", "L"],
                colors=["Red", "Blue", "Yellow"],
                stock={"XS": 4, "S": 9, "M": 12, "L": 7},
                rating=4.6
            ),
            Product(
                id="P005",
                name="Leather Jacket",
                category="Outerwear",
                price=199.99,
                description="Premium leather jacket, timeless style",
                sizes=["S", "M", "L", "XL"],
                colors=["Black", "Brown"],
                stock={"S": 3, "M": 5, "L": 4, "XL": 2},
                rating=4.8
            ),
            Product(
                id="P006",
                name="Cargo Shorts",
                category="Bottoms",
                price=44.99,
                description="Practical cargo shorts with multiple pockets",
                sizes=["28", "30", "32", "34"],
                colors=["Khaki", "Olive"],
                stock={"28": 6, "30": 10, "32": 8, "34": 5},
                rating=4.2
            ),
            Product(
                id="P007",
                name="Sports Tank Top",
                category="Activewear",
                price=29.99,
                description="Moisture-wicking tank top for sports and fitness",
                sizes=["XS", "S", "M", "L", "XL"],
                colors=["Black", "Gray", "Purple"],
                stock={"XS": 5, "S": 12, "M": 15, "L": 10, "XL": 8},
                rating=4.4
            ),
            Product(
                id="P008",
                name="Chinos Pants",
                category="Bottoms",
                price=69.99,
                description="Formal chinos for business casual look",
                sizes=["30", "32", "34", "36"],
                colors=["Navy", "Beige", "Gray"],
                stock={"30": 4, "32": 8, "34": 10, "36": 6},
                rating=4.3
            ),
        ]

        for product in sample_products:
            self.products[product.id] = product

    def search_products(self, query: str) -> List[Product]:
        """Search products by name, category, or description"""
        query_lower = query.lower()
        results = []
        
        for product in self.products.values():
            if (query_lower in product.name.lower() or
                query_lower in product.category.lower() or
                query_lower in product.description.lower()):
                results.append(product)
        
        return results

    def get_product_by_id(self, product_id: str) -> Optional[Product]:
        """Get a specific product by ID"""
        return self.products.get(product_id)

    def get_products_by_category(self, category: str) -> List[Product]:
        """Get all products in a category"""
        return [p for p in self.products.values() if p.category.lower() == category.lower()]

    def get_available_categories(self) -> List[str]:
        """Get all available product categories"""
        categories = set()
        for product in self.products.values():
            categories.add(product.category)
        return sorted(list(categories))

    def check_stock(self, product_id: str, size: str, quantity: int = 1) -> bool:
        """Check if a product is in stock in a specific size"""
        product = self.get_product_by_id(product_id)
        if not product:
            return False
        
        available = product.stock.get(size, 0)
        return available >= quantity

    def get_product_info(self, product_id: str) -> Optional[Dict]:
        """Get detailed information about a product"""
        product = self.get_product_by_id(product_id)
        if not product:
            return None
        
        return {
            "id": product.id,
            "name": product.name,
            "category": product.category,
            "price": f"${product.price:.2f}",
            "description": product.description,
            "available_sizes": product.sizes,
            "available_colors": product.colors,
            "stock": product.stock,
            "rating": product.rating
        }

    def create_order(self, customer_name: str, email: str, items: List[Dict], delivery_address: str) -> Optional[Order]:
        """Create a new order"""
        order_id = f"ORD{self.order_counter}"
        self.order_counter += 1
        
        order_items = []
        total_price = 0
        
        for item in items:
            product_id = item['product_id']
            size = item['size']
            color = item['color']
            quantity = item.get('quantity', 1)
            
            product = self.get_product_by_id(product_id)
            if not product:
                return None
            
            if not self.check_stock(product_id, size, quantity):
                return None
            
            # Deduct from stock
            product.stock[size] -= quantity
            
            order_item = OrderItem(
                product_id=product_id,
                product_name=product.name,
                size=size,
                color=color,
                price=product.price,
                quantity=quantity
            )
            order_items.append(order_item)
            total_price += product.price * quantity
        
        order = Order(
            order_id=order_id,
            customer_name=customer_name,
            email=email,
            items=order_items,
            total_price=total_price,
            status="confirmed",
            created_at=datetime.now(),
            delivery_address=delivery_address
        )
        
        self.orders[order_id] = order
        return order

    def get_order_status(self, order_id: str) -> Optional[Dict]:
        """Get the status of an order"""
        order = self.orders.get(order_id)
        if not order:
            return None
        
        return {
            "order_id": order.order_id,
            "customer_name": order.customer_name,
            "status": order.status,
            "total_price": f"${order.total_price:.2f}",
            "items_count": len(order.items),
            "created_at": order.created_at.isoformat()
        }

    def apply_discount(self, product_id: str, discount_percent: float) -> bool:
        """Apply a discount to a product"""
        product = self.get_product_by_id(product_id)
        if not product:
            return False
        
        discount_amount = product.price * (discount_percent / 100)
        product.price -= discount_amount
        return True

    def get_store_summary(self) -> Dict:
        """Get a summary of the store"""
        total_products = len(self.products)
        total_stock = sum(sum(p.stock.values()) for p in self.products.values())
        total_orders = len(self.orders)
        total_revenue = sum(o.total_price for o in self.orders.values())
        
        return {
            "total_products": total_products,
            "total_stock_items": total_stock,
            "total_orders": total_orders,
            "total_revenue": f"${total_revenue:.2f}",
            "categories": self.get_available_categories()
        }
