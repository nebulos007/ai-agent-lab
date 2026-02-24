import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

def main():
    print("🚀 Welcome to the app!")
    
    # Load environment variables
    load_dotenv()
    
    # Check if GITHUB_TOKEN exists
    github_token = os.getenv("GITHUB_TOKEN")
    
    if not github_token:
        print("❌ Error: GITHUB_TOKEN not found!")
        print("\n📋 To fix this:")
        print("   1. Create a .env file in the project root")
        print("   2. Add your GitHub token: GITHUB_TOKEN=your_token_here")
        print("   3. Get a token from: https://github.com/settings/tokens")
        return
    
    
    # Create ChatOpenAI instance
    client = ChatOpenAI(
        model="openai/gpt-4o",
        temperature=0,
        base_url="https://models.github.ai/inference",
        api_key=github_token
    )
    print("✅ ChatOpenAI client initialized!")
    
    # Test query
    query = "What is 25 * 4 + 10?"
    print(f"\n❓ Query: {query}")
    
    # Call invoke with the query (AI will answer without tools)
    message = HumanMessage(content=query)
    response = client.invoke([message])
    
    # Print the response
    print(f"🤖 Response: {response.content}")
    print("✅ GITHUB_TOKEN found!")

if __name__ == "__main__":
    main()