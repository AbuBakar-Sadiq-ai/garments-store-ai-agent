"""
Test scenarios for the Garments Store AI Agent
Demonstrates various use cases and interactions
"""

from agent import run_agent


def print_section(title: str):
    """Print a formatted section header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def test_scenario(title: str, user_input: str):
    """Test a single scenario"""
    print(f"\n📌 Scenario: {title}")
    print(f"You: {user_input}")
    print("\nAssistant:")
    response = run_agent(user_input)
    print(response)
    print("-" * 70)


def main():
    """Run all test scenarios"""
    
    print_section("GARMENTS STORE AI AGENT - TEST SCENARIOS")
    print("This script demonstrates various interactions with the agent.\n")
    
    # Test 1: Product Search
    print_section("Test 1: Product Search")
    test_scenario(
        "Customer searching for jeans",
        "Show me jeans you have"
    )
    test_scenario(
        "Customer searching by color",
        "Do you have any blue items?"
    )
    test_scenario(
        "Customer searching by category",
        "What tops do you have?"
    )
    
    # Test 2: Product Details
    print_section("Test 2: Product Details")
    test_scenario(
        "Customer wants detailed info",
        "Tell me more about product P001"
    )
    test_scenario(
        "Customer checking specific product",
        "What are the details of the blue denim jeans?"
    )
    
    # Test 3: Stock Checking
    print_section("Test 3: Stock Availability")
    test_scenario(
        "Customer checking specific size",
        "Is the Blue Denim Jeans available in size 32?"
    )
    test_scenario(
        "Customer checking if item is in stock",
        "Do you have White T-Shirt in size M?"
    )
    
    # Test 4: Category Browsing
    print_section("Test 4: Browse by Category")
    test_scenario(
        "Customer browsing activewear",
        "Show me all activewear items"
    )
    test_scenario(
        "Customer browsing outerwear",
        "What outerwear do you have in stock?"
    )
    
    # Test 5: Store Information
    print_section("Test 5: Store Information")
    test_scenario(
        "Customer asking for store info",
        "Tell me about your store"
    )
    test_scenario(
        "Customer asking what categories are available",
        "What product categories do you have?"
    )
    
    # Test 6: Order Placement
    print_section("Test 6: Order Placement")
    test_scenario(
        "Customer placing an order",
        "I want to buy a Blue Denim Jeans in size 32. My name is John Smith, email is john@email.com, and I want it delivered to 123 Main St, New York, NY 10001"
    )
    test_scenario(
        "Customer ordering multiple items",
        "I'd like to order a White T-Shirt in size M and a Black Hoodie in size L. My name is Jane Doe, email jane@email.com, delivery to 456 Oak Ave, Boston, MA 02101"
    )
    
    # Test 7: Complex Queries
    print_section("Test 7: Complex Queries")
    test_scenario(
        "Customer asking for recommendations",
        "What would you recommend for summer? Something light and comfortable."
    )
    test_scenario(
        "Customer with budget constraints",
        "What items do you have under $50?"
    )
    test_scenario(
        "Customer looking for gift",
        "I need to buy a gift for my friend. What's popular?"
    )
    
    # Test 8: Size Information
    print_section("Test 8: Size and Color Options")
    test_scenario(
        "Customer asking about sizes",
        "What sizes does the Summer Dress come in?"
    )
    test_scenario(
        "Customer asking about colors",
        "Does the Summer Dress come in any other colors besides red and blue?"
    )
    
    # Test 9: Edge Cases
    print_section("Test 9: Edge Cases and Error Handling")
    test_scenario(
        "Customer searching for non-existent item",
        "Do you have any swimming suits?"
    )
    test_scenario(
        "Customer asking about out of stock item",
        "I need a leather jacket in size XXL. Do you have it?"
    )
    
    # Test 10: Pricing Inquiries
    print_section("Test 10: Pricing and Discounts")
    test_scenario(
        "Customer asking about price",
        "How much does the Leather Jacket cost?"
    )
    test_scenario(
        "Customer asking about discounts",
        "Do you have any sales or discounts?"
    )
    
    print_section("All Tests Complete!")
    print("\n✓ Test scenarios finished successfully!")
    print("\nYou can now run the interactive agent with: python agent.py")
    print("Or use the API with: python api.py\n")


if __name__ == "__main__":
    main()
