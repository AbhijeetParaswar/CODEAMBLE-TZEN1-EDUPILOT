"""Test script to verify Groq configuration is loaded correctly"""
import os
from pathlib import Path

# Load .env manually
env_path = Path(__file__).parent / '.env'
print(f"Loading .env from: {env_path}\n")

env_vars = {}
with open(env_path, 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            # Remove inline comments
            if '#' in value:
                value = value.split('#')[0].strip()
            env_vars[key] = value

# Check Groq config
groq_api_key = env_vars.get('GROQ_API_KEY', '')
groq_model = env_vars.get('GROQ_MODEL', '')

print("=" * 60)
print("GROQ CONFIGURATION CHECK")
print("=" * 60)

if groq_api_key:
    # Check for spaces (common error)
    if groq_api_key.startswith(' ') or groq_api_key.endswith(' '):
        print("❌ ERROR: GROQ_API_KEY has leading/trailing spaces!")
        print(f"   Key: '{groq_api_key}'")
        print("   Fix: Remove spaces in .env file")
    else:
        print(f"✅ GROQ_API_KEY: {groq_api_key[:20]}...{groq_api_key[-10:]}")
        print(f"   Length: {len(groq_api_key)} characters")
else:
    print("❌ ERROR: GROQ_API_KEY not found in .env")

if groq_model:
    print(f"✅ GROQ_MODEL: {groq_model}")
else:
    print("❌ ERROR: GROQ_MODEL not found in .env")

print("\n" + "=" * 60)
print("OTHER RELEVANT SETTINGS")
print("=" * 60)

# Check other important settings
important_keys = ['DATABASE_URL', 'CHROMA_PATH', 'REDIS_URL', 'JUDGE_MODEL']
for key in important_keys:
    value = env_vars.get(key, 'NOT SET')
    status = "✅" if value != 'NOT SET' else "❌"
    print(f"{status} {key}: {value}")

print("\n" + "=" * 60)
print("VALIDATION RESULT")
print("=" * 60)

if groq_api_key and groq_model and not groq_api_key.startswith(' '):
    print("✅ Configuration is VALID - Ready to use Groq!")
    print("\nTo start the server:")
    print("  cd services")
    print("  venv\\Scripts\\activate  # (if using venv)")
    print("  python -m app.main")
else:
    print("❌ Configuration has ERRORS - Please fix .env file")
    print("\nCommon fixes:")
    print("  1. Remove spaces: GROQ_API_KEY=your_key (no spaces)")
    print("  2. Remove inline comments from same line")
    print("  3. Save file and restart server")
