import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load the API Key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

print("------------------------------------------------")
if not api_key:
    print("❌ ERROR: No API Key found in .env file.")
else:
    print(f"✅ Key Found: {api_key[:5]}... (Length: {len(api_key)})")

    # 2. Configure the API
    genai.configure(api_key=api_key)

    # 3. List available models (This checks if your Key works)
    print("\n🔍 Checking available models for this Key...")
    try:
        found_flash = False
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"   - {m.name}")
                if "flash" in m.name:
                    found_flash = True
        
        if found_flash:
            print("\n✅ SUCCESS: Your API Key has access to Flash models.")
        else:
            print("\n⚠️ WARNING: Flash model not found in your list.")

        # 4. Try a simple generation
        print("\n🧪 Testing Generation with 'gemini-1.5-flash'...")
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Hello, are you working?")
        print(f"🤖 REPLY: {response.text}")

    except Exception as e:
        print(f"\n❌ API ERROR: {e}")
print("------------------------------------------------")