# Fashion Garments Store AI Agent

🤖 An intelligent AI-powered assistant for a garments store built with LangChain and OpenAI.

## 📋 Overview

This project demonstrates how to build a conversational AI agent that:
- Searches and recommends products
- Provides detailed product information
- Checks inventory and stock availability
- Processes customer orders
- Handles customer inquiries naturally

## 🎯 Features

✨ **Natural Language Processing** - Customers interact in plain English  
✨ **Product Search** - Find items by name, category, or keywords  
✨ **Stock Management** - Real-time inventory checking  
✨ **Order Processing** - Complete order workflow  
✨ **REST API** - Easy integration with web/mobile apps  
✨ **Interactive CLI** - Test the agent directly  
✨ **Test Suite** - 10 different test scenarios included  

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key
- pip (Python package manager)

### Installation

1. **Clone or download the project**
   ```bash
   git clone https://github.com/AbuBakar-Sadiq-ai/garments-store-ai-agent.git
   cd garments-store-ai-agent
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

### Running the Agent

**Interactive Mode (Chat with the Agent)**
```bash
python agent.py
```

**Run Test Scenarios**
```bash
python test_agent.py
```

**Start REST API Server**
```bash
python api.py
```
Then visit: http://localhost:8000/docs for API documentation

## 📁 Project Structure

### Core Files

| File | Purpose |
|------|----------|
| `agent.py` | Main AI agent with LangChain integration |
| `store_database.py` | Product inventory and order management |
| `api.py` | FastAPI REST endpoints |
| `test_agent.py` | Test scenarios and examples |
| `requirements.txt` | Python dependencies |
| `.env.example` | Environment configuration template |

### Documentation Files

| File | Purpose |
|------|----------|
| `README.md` | This file - project overview |
| `LEARNING_GUIDE.md` | Step-by-step learning guide with exercises |

## 🛍️ Store Inventory

The store comes pre-loaded with 8 products:

1. **Blue Denim Jeans** ($59.99) - Sizes 28-36
2. **White T-Shirt** ($19.99) - Sizes XS-XXL
3. **Black Hoodie** ($49.99) - Sizes S-XL
4. **Summer Dress** ($79.99) - Sizes XS-L, Multiple colors
5. **Leather Jacket** ($199.99) - Sizes S-XL, Multiple colors
6. **Cargo Shorts** ($44.99) - Sizes 28-34, Multiple colors
7. **Sports Tank Top** ($29.99) - Sizes XS-XL, Multiple colors
8. **Chinos Pants** ($69.99) - Sizes 30-36, Multiple colors

## 🔧 Agent Tools

The agent has access to 7 powerful tools:

### 1. **search_products**
Search for products by keyword, name, or category.
```
Example: "Show me blue jeans"
```

### 2. **get_product_details**
Get comprehensive information about a specific product.
```
Example: "Tell me about product P001"
```

### 3. **check_stock**
Verify availability of a product in a specific size.
```
Example: "Is Blue Denim Jeans available in size 32?"
```

### 4. **browse_category**
Browse all products in a specific category.
```
Example: "Show me all tops"
```

### 5. **place_order**
Process a new customer order.
```
Example: "I want to order a White T-Shirt in size M"
```

### 6. **get_order_status**
Check the status of an existing order.
```
Example: "What's the status of order ORD1000?"
```

### 7. **get_store_info**
Get general store information and statistics.
```
Example: "Tell me about your store"
```

## 💬 Example Conversations

### Conversation 1: Product Search & Purchase
```
Customer: "I'm looking for casual pants under $70"
Agent: [Searches and finds Cargo Shorts]

Customer: "Tell me more about the cargo shorts"
Agent: [Provides detailed information]

Customer: "Is it available in size 32?"
Agent: "Yes, we have it in stock!"

Customer: "I'll buy it in khaki. My name is John, email john@example.com, ship to 123 Main St"
Agent: "Order confirmed! Order ID: ORD1001"
```

### Conversation 2: Category Browsing
```
Customer: "What activewear do you have?"
Agent: [Displays all activewear items]

Customer: "Which one has the best rating?"
Agent: "The Sports Tank Top has 4.4/5 stars"

Customer: "Show me all colors available"
Agent: "Available in Black, Gray, and Purple"
```

## 🔌 REST API Endpoints

### Chat Endpoint
```bash
POST /chat
Body: {"message": "Show me jeans"}
```

### Product Search
```bash
GET /products/search?query=jeans
```

### Product Details
```bash
GET /products/P001
```

### Browse Category
```bash
GET /products/category/Tops
```

### Check Stock
```bash
GET /stock/P001/32
```

### Place Order
```bash
POST /orders
Body: {
  "product_id": "P001",
  "size": "32",
  "color": "Blue",
  "quantity": 1,
  "customer_name": "John Smith",
  "email": "john@example.com",
  "delivery_address": "123 Main St"
}
```

### Get Order Status
```bash
GET /orders/ORD1000
```

## 📚 Learning Path

1. **Start**: Read `LEARNING_GUIDE.md`
2. **Understand**: Review `store_database.py` (data structure)
3. **Learn**: Study `agent.py` (AI integration)
4. **Explore**: Review `api.py` (REST endpoints)
5. **Test**: Run `test_agent.py` (test scenarios)
6. **Practice**: Use `agent.py` interactively
7. **Extend**: Modify and add new features

## 🎓 What You'll Learn

- ✅ How AI agents work and make decisions
- ✅ LangChain framework and agent architecture
- ✅ Tool design and integration patterns
- ✅ Prompt engineering best practices
- ✅ Building REST APIs with FastAPI
- ✅ State management in conversational agents
- ✅ Error handling and edge cases
- ✅ Testing AI systems
- ✅ Real-world AI application design

## 🔄 Agent Decision Flow

```
┌─ User Input ───────────────────────────┐
│  "Show me blue jeans"                  │
└─────────────────────┬──────────────────┘
                      │
                      ▼
        ┌──────────────────────────────┐
        │  Agent Thinks               │
        │  (LLM)                       │
        └──────────────┬───────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
    search_        check_         get_product
    products       stock          details
        │              │              │
        └──────────────┼──────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │  Agent Plans                │
        │  Response                   │
        └──────────────┬───────────────┘
                       │
                       ▼
    ┌────────────────────────────────┐
    │  Return to Customer            │
    │  "Found 1 blue jeans"          │
    └────────────────────────────────┘
```

## 🛠️ Customization

### Add New Products
Edit `store_database.py` in the `initialize_inventory()` method:
```python
Product(
    id="P009",
    name="Your Product",
    category="Category",
    price=99.99,
    # ...
)
```

### Add New Tools
Add a function and Tool in `agent.py`:
```python
def my_tool(param: str) -> str:
    """Tool description"""
    return "result"

tools.append(Tool(
    name="my_tool",
    func=my_tool,
    description="What this tool does"
))
```

### Modify Agent Behavior
Edit the system prompt in `agent.py`:
```python
agent.agent.llm_chain.prompt.template = "Your custom prompt"
```

## 🐛 Troubleshooting

### "API key not found" error
- Make sure `.env` file exists
- Check that `OPENAI_API_KEY` is set correctly
- Don't use quotes around the key value

### "Module not found" error
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

### Agent not responding
- Check OpenAI API quota and billing
- Ensure internet connection is stable
- Check `.env` file for correct API key

### Order placement fails
- Verify product ID exists
- Check that size is available
- Ensure all required fields are provided

## 📖 Additional Resources

- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Agents Guide](https://python.langchain.com/docs/modules/agents/)
- [AI Agent Design Patterns](https://www.deeplearning.ai/short-courses/)

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add new features
- Fix bugs
- Improve documentation
- Add test cases
- Optimize performance

## 💡 Future Enhancements

- [ ] Database integration (instead of in-memory)
- [ ] User authentication and profiles
- [ ] Order history and recommendations
- [ ] Payment gateway integration
- [ ] Email notifications
- [ ] Multi-language support
- [ ] Machine learning for recommendations
- [ ] Analytics dashboard
- [ ] Review and rating system
- [ ] Inventory tracking dashboard

## ✨ Features Roadmap

**Version 1.0** ✅ 
- Basic product search and browsing
- Order placement
- REST API

**Version 1.1** (Upcoming)
- Advanced filtering and sorting
- Wishlist feature
- Customer reviews integration

**Version 2.0** (Future)
- Payment processing
- Email notifications
- Admin dashboard

## 📧 Support

For questions or issues:
1. Check the `LEARNING_GUIDE.md`
2. Review test scenarios in `test_agent.py`
3. Check troubleshooting section above
4. Review code comments for detailed explanations

---

**Happy Learning! 🚀**

Start with the interactive agent and explore how AI powers this store:
```bash
python agent.py
```
