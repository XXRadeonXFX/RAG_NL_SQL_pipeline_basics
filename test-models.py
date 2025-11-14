from anthropic import Anthropic
import os

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    ANTHROPIC_API_KEY = input("Enter your Claude API key: ")

client = Anthropic(api_key=ANTHROPIC_API_KEY)

print("Testing available Claude models...\n")

models_to_test = [
    "claude-3-5-sonnet-20241022",
    "claude-3-5-sonnet-20240620", 
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
    "claude-2.1",
    "claude-2.0",
]

for model in models_to_test:
    try:
        response = client.messages.create(
            model=model,
            max_tokens=10,
            messages=[{"role": "user", "content": "Hi"}]
        )
        print(f"✅ {model} - WORKS!")
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg or "not_found" in error_msg:
            print(f"❌ {model} - Not available")
        elif "401" in error_msg or "authentication" in error_msg.lower():
            print(f"❌ {model} - Authentication error (check API key)")
            break
        else:
            print(f"❌ {model} - Error: {error_msg}")