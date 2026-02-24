import os
from dotenv import load_dotenv

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
    
    print("✅ GITHUB_TOKEN found!")

if __name__ == "__main__":
    main()