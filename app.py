import os
import warnings
warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL")
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool, Tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub

def calculator(expression: str) -> str:
    """
    Evaluates mathematical expressions and returns the result as a string.
    
    Args:
        expression: A mathematical expression as a string (e.g., "25 * 4 + 10")
    
    Returns:
        The result of the expression as a string
    """
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"

def get_current_time(input_str: str) -> str:
    """
    Returns the current date and time in a formatted string.
    
    Args:
        input_str: Input parameter (required by Tool interface, not used)
    
    Returns:
        The current date and time as a formatted string (YYYY-MM-DD HH:MM:SS)
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def reverse_string(input_string: str) -> str:
    """
    Reverses a string and returns the reversed version.
    
    Args:
        input_string: The string to reverse
    
    Returns:
        The reversed string
    """
    return input_string[::-1]

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
    print("✅ GITHUB_TOKEN found!")
    
    # Create tools list
    tools = [
        Tool(
            name="Calculator",
            func=calculator,
            description="Use this tool when you need to evaluate mathematical expressions. "
                       "Provide the expression as a string (e.g., '25 * 4 + 10'). "
                       "This tool is perfect for arithmetic operations, solving equations, "
                       "and verifying mathematical calculations."
        ),
        Tool(
            name="get_current_time",
            func=get_current_time,
            description="Use this tool to get the current date and time. "
                       "Returns the current time in YYYY-MM-DD HH:MM:SS format. "
                       "Use this when you need to know what time it is right now."
        ),
        Tool(
            name="reverse_string",
            func=reverse_string,
            description="Reverses a string. Input should be a single string."
        )
    ]
    print("✅ Tools configured!")
    
    # Create an agent with tools
    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=client, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    print("✅ Agent created!")
    
    # Test queries
    queries = [
        "What time is it right now?",
        "What is 25 * 4 + 10?",
        "Reverse the string 'Hello World'"
    ]
    
    print("\n" + "="*60)
    print("Running example queries:")
    print("="*60)
    
    for query in queries:
        print(f"\n📝 Query: {query}")
        print("-" * 60)
        
        # Invoke agent with error handling
        try:
            result = agent_executor.invoke({"input": query})
            print(f"✅ Agent Result: {result['output']}")
        except Exception as e:
            print(f"❌ Error executing agent: {str(e)}")

if __name__ == "__main__":
    main()