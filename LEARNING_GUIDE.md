# 📚 Garments Store AI Agent - Learning Guide

A comprehensive guide to understanding and learning from this AI agent project.

## 🎯 Learning Objectives

By the end of this guide, you will understand:

1. **How AI Agents Work** - Core concepts and architecture
2. **LangChain Framework** - Tools, agents, and chains
3. **Tool Design** - Creating and integrating tools
4. **Prompt Engineering** - Writing effective prompts
5. **State Management** - Handling conversation context
6. **API Design** - Building REST interfaces
7. **Testing Strategies** - Validating agent behavior
8. **Real-world Applications** - Practical considerations

## 📖 Table of Contents

1. [Phase 1: Understanding the Basics](#phase-1-understanding-the-basics)
2. [Phase 2: Deep Dive into Code](#phase-2-deep-dive-into-code)
3. [Phase 3: Hands-on Practice](#phase-3-hands-on-practice)
4. [Phase 4: Advanced Concepts](#phase-4-advanced-concepts)
5. [Reference Guide](#reference-guide)

---

## Phase 1: Understanding the Basics

### What is an AI Agent?

An **AI Agent** is a software system that:
- **Perceives** the environment (user input)
- **Reasons** about actions using AI (LLM)
- **Decides** which tools to use
- **Acts** by calling tools
- **Responds** to the user

### Agent vs. Chatbot

| Feature | Chatbot | Agent |
|---------|---------|-------|
| **Decision Making** | Predefined rules | AI-powered reasoning |
| **Tools** | Single source | Multiple integrated tools |
| **Problem Solving** | Template-based | Adaptive and dynamic |
| **Complexity** | Simple | Complex |

### The Agent Loop

```
REPEAT:
  1. Accept user input
  2. Send to LLM with tools available
  3. LLM decides which tool(s) to use
  4. Execute the tool(s)
  5. Send results back to LLM
  6. LLM formulates response
  7. Return response to user
UNTIL user exits
```

### Key Components

#### 1. **Language Model (LLM)**
The "brain" of the agent. We use OpenAI's GPT models.

```python
from langchain.llms import OpenAI

llm = OpenAI(
    temperature=0.7,  # Creativity level (0=deterministic, 1=random)
    api_key=os.getenv("OPENAI_API_KEY")
)
```

**Understanding Temperature:**
- `0.0` - Deterministic, always same answer
- `0.5` - Balanced, some variation
- `1.0` - Creative, high variation

#### 2. **Tools**
Functions the agent can call to solve problems.

```python
Tool(
    name="search_products",
    func=search_products,  # Python function
    description="Search for products in the store"
)
```

#### 3. **Agent**
The orchestrator that decides which tools to use.

```python
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True  # Show agent's reasoning
)
```

#### 4. **Memory (Optional)**
Some agents remember conversation history (not in our basic version).

### ReAct Framework

Our agent uses **ReAct** (Reasoning + Acting):

```
┌────────────────────────────────────────┐
│ Thought: What do I need to do?        │
│ Action: Use this tool                 │
│ Action Input: With these parameters   │
├────────────────────────────────────────┤
│ [Tool executes and returns result]    │
├────────────────────────────────────────┤
│ Observation: Here's what happened    │
│ Thought: What's next?                 │
│ Final Answer: Here's the response     │
└────────────────────────────────────────┘
```

---

## Phase 2: Deep Dive into Code

### File 1: `store_database.py` - The Data Layer

This file manages:
- Product inventory
- Orders and order history
- Stock management

#### Key Classes:

**Product Class**
```python
@dataclass
class Product:
    id: str                    # Unique identifier
    name: str                  # Product name
    category: str              # Category
    price: float               # Price in dollars
    description: str           # Description
    sizes: List[str]           # Available sizes
    colors: List[str]          # Available colors
    stock: Dict[str, int]      # Stock per size
    image_url: str = ""
    rating: float = 0.0
```

**GarmentsStore Class**
```python
class GarmentsStore:
    def __init__(self):
        self.products = {}     # Product database
        self.orders = {}       # Order database
        self.order_counter = 1000
        self.initialize_inventory()  # Load products
```

#### Key Methods:

```python
# Search for products
def search_products(query: str) -> List[Product]

# Get specific product
def get_product_by_id(product_id: str) -> Optional[Product]

# Check if item is in stock
def check_stock(product_id: str, size: str, quantity: int) -> bool

# Create a new order
def create_order(customer_name: str, email: str, items: List[Dict], delivery_address: str) -> Order
```

**Understanding the Stock System:**
```python
# Stock is stored as: {"size": quantity}
product.stock = {
    "S": 10,   # 10 units in small
    "M": 15,   # 15 units in medium
    "L": 8,    # 8 units in large
    "XL": 5    # 5 units in extra large
}
```

### File 2: `agent.py` - The AI Brain

This is where the magic happens!

#### Step 1: Tool Definition

Each tool is a Python function:

```python
def search_products(query: str) -> str:
    """Search for products - the agent can call this"""
    results = store.search_products(query)  # Search
    # Format results for agent
    response = f"Found {len(results)} product(s)...\n"
    for product in results:
        response += f"{product.name} - ${product.price}\n"
    return response
```

**Key Point**: Tools return **strings** that the agent can understand!

#### Step 2: Tool Wrapping

Convert functions to LangChain Tools:

```python
Tool(
    name="search_products",              # Tool name
    func=search_products,                 # Python function
    description="Search for products..." # What it does
)
```

**Why descriptions matter**: The agent reads these to decide which tool to use!

#### Step 3: Agent Initialization

```python
agent = initialize_agent(
    tools=tools,                                    # List of tools
    llm=llm,                                       # The AI model
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # Agent type
    verbose=True,                                  # Show reasoning
    max_iterations=10,                             # Prevent infinite loops
    early_stopping_method="generate"              # How to stop
)
```

#### Step 4: Agent Execution

```python
response = agent.run("Show me blue jeans")
```

**What happens internally**:
1. Agent receives: "Show me blue jeans"
2. LLM analyzes available tools
3. LLM decides to use: `search_products("blue jeans")`
4. Tool executes and returns results
5. LLM formulates user-friendly response
6. Response returned to user

### File 3: `api.py` - The Web Interface

Exposes agent functionality as REST endpoints.

#### Basic Endpoints:

```python
@app.post("/chat")
async def chat(request: ChatMessage):
    """Chat with the agent"""
    response = run_agent(request.message)
    return ChatResponse(
        user_message=request.message,
        assistant_response=response
    )
```

#### Request/Response Models:

```python
class ChatMessage(BaseModel):
    message: str  # User input

class ChatResponse(BaseModel):
    user_message: str      # Echo of input
    assistant_response: str # Agent response
```

---

## Phase 3: Hands-on Practice

### Exercise 1: Run the Basic Agent

**Objective**: Get familiar with how the agent works.

1. Start the agent:
   ```bash
   python agent.py
   ```

2. Try these inputs:
   ```
   You: "Show me jeans"
   You: "What's in the Tops category?"
   You: "Tell me about product P002"
   You: "Is the White T-Shirt available in size M?"
   ```

3. Watch the verbose output - see how the agent "thinks"!

**Questions to ask yourself**:
- Which tool did the agent choose?
- Why did it choose that tool?
- What was the agent's reasoning?

### Exercise 2: Test Different Queries

**Objective**: Understand how the LLM interprets requests.

Try these variations:

```
# Explicit request
"Search for hoodies"

# Implicit request (agent must interpret)
"I'm looking for something warm to wear"

# Detailed request
"Show me all pants under $70 in size 32"

# Vague request
"What do you have?"

# Complex request
"I want to buy a black hoodie in medium, my name is John Doe"
```

**Learning Point**: The LLM is powerful but needs good instructions!

### Exercise 3: Modify a Tool

**Objective**: Learn how to customize tools.

Try this: Edit the `search_products` function to sort by price:

```python
def search_products(query: str) -> str:
    """Search for products (sorted by price)"""
    results = store.search_products(query)
    results.sort(key=lambda p: p.price)  # Sort by price
    
    response = f"Found {len(results)} product(s), sorted by price:\n\n"
    for product in results:
        response += f"{product.name} - ${product.price:.2f}\n"
    return response
```

Test it: `"Show me all tops, cheapest first"`

### Exercise 4: Add a New Tool

**Objective**: Learn tool creation from scratch.

Add a discount tool:

```python
def apply_discount(product_name: str, discount_percent: float) -> str:
    """Apply a discount to a product"""
    # Find product
    results = store.search_products(product_name)
    if not results:
        return f"Product '{product_name}' not found"
    
    product = results[0]
    original_price = product.price
    store.apply_discount(product.id, discount_percent)
    new_price = product.price
    
    savings = original_price - new_price
    return f"Discount applied! {product.name}: ${original_price:.2f} → ${new_price:.2f} (Save ${savings:.2f})"

# Add to tools list
tools.append(Tool(
    name="apply_discount",
    func=apply_discount,
    description="Apply a discount percentage to a product"
))
```

Test it: `"Give me a 20% discount on the Blue Denim Jeans"`

### Exercise 5: Improve the Prompt

**Objective**: Learn prompt engineering.

Edit the agent's system prompt in `agent.py`:

```python
agent.agent.llm_chain.prompt.template = """
You are Emma, a friendly and helpful fashion store assistant.

Your personality:
- Always be warm and welcoming
- Use friendly language
- Make product recommendations
- Help customers find exactly what they need

Available tools:
{tools}

Remember:
1. Always search for products when customers ask about items
2. Provide price information
3. Check availability before confirming orders
4. Be proactive with suggestions

Question: {input}

{agent_scratchpad}
"""
```

Test: Notice how the agent's responses become more personalized!

---

## Phase 4: Advanced Concepts

### 1. Agent Types

LangChain supports different agent architectures:

**ZERO_SHOT_REACT_DESCRIPTION** (What we use)
- Agent decides tool based on descriptions
- No memory between steps
- Simple and fast

```python
AgentType.ZERO_SHOT_REACT_DESCRIPTION
```

**Other types**:
```python
# Conversational - remembers context
AgentType.CONVERSATIONAL_REACT_DESCRIPTION

# Structured input tools
AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION
```

### 2. Understanding LLM Parameters

```python
llm = OpenAI(
    temperature=0.7,        # Creativity (0-1)
    max_tokens=500,         # Max response length
    top_p=0.9,              # Nucleus sampling
    frequency_penalty=0,    # Repeat penalty
    presence_penalty=0,     # New topic penalty
)
```

**When to use what**:
- **Product search**: Low temp (0.3) - be precise
- **Creative recommendations**: High temp (0.8) - be creative
- **Order confirmation**: Low temp (0.0) - be consistent

### 3. Error Handling

Tools should handle errors gracefully:

```python
def search_products(query: str) -> str:
    try:
        if not query or len(query.strip()) < 2:
            return "Please provide a search term of at least 2 characters"
        
        results = store.search_products(query)
        
        if not results:
            return f"No products found matching '{query}'"
        
        # Format results...
        
    except Exception as e:
        return f"Error during search: {str(e)}"
```

### 4. Tool Parameter Handling

Tools can have optional parameters:

```python
def filter_products(category: str = None, max_price: float = None) -> str:
    """Filter products by category and price"""
    # Implementation
    pass
```

### 5. Chaining Operations

Sometimes agents need to chain multiple tools:

```
User: "I want to buy a hoodie, size M, in black"

1. First tool: search_products("hoodie")
2. Second tool: get_product_details("P003")
3. Third tool: check_stock("P003", "M")
4. Fourth tool: place_order(...)
```

### 6. Integration Patterns

**Pattern 1: Sequential Tools**
```
Search → Details → Stock Check → Order
```

**Pattern 2: Parallel Tools**
```
Search Category A + Search Category B simultaneously
```

**Pattern 3: Conditional Tools**
```
IF product found THEN check stock
ELSE recommend alternatives
```

### 7. Performance Optimization

```python
# Cache frequently used results
cache = {}

def search_products_cached(query: str) -> str:
    if query in cache:
        return cache[query]
    
    result = search_products(query)
    cache[query] = result
    return result
```

---

## Reference Guide

### Common Agent Patterns

#### Pattern 1: Search and Recommend
```python
user_input = "Show me hoodies"
# Agent: searches → formats → returns
```

#### Pattern 2: Details Request
```python
user_input = "Tell me about P001"
# Agent: gets details → formats → returns
```

#### Pattern 3: Order Placement
```python
user_input = "I want to buy..."
# Agent: searches → confirms details → places order
```

#### Pattern 4: Status Check
```python
user_input = "Where's my order?"
# Agent: retrieves status → formats → returns
```

### Debugging Tips

**Enable verbose mode to see agent thinking**:
```python
agent = initialize_agent(
    tools=tools,
    llm=llm,
    verbose=True  # See all steps
)
```

**Check tool descriptions**:
- Clear descriptions help agent choose right tool
- Test descriptions by asking yourself: "Would I know what this does?"

**Test tools independently**:
```python
result = search_products("jeans")
print(result)  # Check output format
```

**Monitor token usage**:
```python
# Each API call costs tokens
# Complex prompts = more tokens
# Optimize by simplifying
```

### Best Practices

✅ **DO**:
- Keep tool descriptions clear and concise
- Return formatted strings from tools
- Handle errors in tools
- Test tools independently
- Use low temperature for deterministic tasks
- Cache frequently used results
- Log agent decisions for debugging

❌ **DON'T**:
- Make tools do too much
- Return raw data from tools
- Ignore edge cases
- Use high temperature for critical operations
- Make tools call other tools (agent should orchestrate)
- Hard-code prompts (make them configurable)
- Forget to handle exceptions

### Common Mistakes

**Mistake 1: Unclear Tool Descriptions**
```python
# BAD
Tool(name="tool1", func=search, description="Does stuff")

# GOOD
Tool(name="search_products", func=search, 
     description="Search inventory by product name or category")
```

**Mistake 2: Tools Returning Wrong Format**
```python
# BAD - Returns dict
def search_products(query):
    return {"products": [...]}  # Agent can't parse this well

# GOOD - Returns formatted string
def search_products(query):
    return "Found 3 products: 1. Item1 2. Item2 3. Item3"
```

**Mistake 3: Too Many Tools**
```python
# BAD - Agent gets confused
tools = [tool1, tool2, tool3, ..., tool20]

# GOOD - Keep it focused
tools = [search, details, stock, order, status]  # 5-7 tools
```

**Mistake 4: Not Handling Errors**
```python
# BAD
def search(query):
    return store.search(query)  # Crashes if store is empty

# GOOD
def search(query):
    try:
        results = store.search(query)
        return results if results else "No matches found"
    except Exception as e:
        return f"Search error: {e}"
```

---

## 🎓 Summary

### What You've Learned:

1. ✅ AI agents use LLMs to reason about which tools to use
2. ✅ Tools are functions that agents can call
3. ✅ LangChain orchestrates the agent
4. ✅ Clear tool descriptions are critical
5. ✅ Tools should return formatted strings
6. ✅ Error handling is essential
7. ✅ Agent behavior can be customized via prompts
8. ✅ REST APIs expose agent functionality

### Next Steps:

1. **Experiment** - Try modifying the tools and prompts
2. **Extend** - Add new features (wishlists, reviews, etc.)
3. **Integrate** - Connect to real databases
4. **Deploy** - Put your agent online
5. **Monitor** - Track agent performance
6. **Improve** - Use feedback to enhance

### Further Learning:

- LangChain Docs: https://python.langchain.com/
- OpenAI Models: https://platform.openai.com/docs/models/
- Agent Design: https://www.deeplearning.ai/short-courses/
- Prompt Engineering: https://platform.openai.com/docs/guides/prompt-engineering

---

## 📱 Quick Reference

### Running Different Modes

```bash
# Interactive mode
python agent.py

# Test scenarios
python test_agent.py

# API server
python api.py

# Curl example
curl -X POST http://localhost:8000/chat \\
  -H "Content-Type: application/json" \\
  -d '{"message": "Show me jeans"}'
```

### Common Queries to Try

```
"What categories do you have?"
"Show me tops under $50"
"Is the blue jeans available in size 32?"
"Tell me about product P005"
"I want to order a t-shirt"
"What's my order status?"
```

---

**Happy Learning! 🚀**

Start with Exercise 1 and progress through each phase. Good luck!
