"""
ONE COMMAND TO TEST EVERYTHING
Run this before your hackathon demo!
"""

import asyncio
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def print_banner(text):
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")


def test_ollama():
    """Test if Ollama is running"""
    print_banner("🤖 CHECKING OLLAMA")
    
    import subprocess
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print("✅ Ollama is running")
            print(f"\nAvailable models:")
            print(result.stdout)
            return True
        else:
            print("❌ Ollama not responding")
            print("\n💡 Fix: Run 'ollama serve' in another terminal")
            return False
    except Exception as e:
        print(f"❌ Ollama error: {e}")
        print("\n💡 Fix: Run 'ollama serve' in another terminal")
        return False


def test_database():
    """Test database connection"""
    print_banner("💾 CHECKING DATABASE")
    
    try:
        from app.db.session import SessionLocal
        from app.db.models import Opportunity
        
        db = SessionLocal()
        count = db.query(Opportunity).count()
        db.close()
        
        print(f"✅ Database connected")
        print(f"   Total opportunities: {count}")
        
        if count == 0:
            print("\n⚠️  Warning: No opportunities in database!")
            print("   Run: python index_scholarships_now.py")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False


def test_rag_index():
    """Test RAG index"""
    print_banner("🔍 CHECKING RAG INDEX")
    
    try:
        from app.knowledge.hybrid_rag import HybridRAG
        
        rag = HybridRAG()
        results = rag.semantic_search("engineering scholarship", limit=3)
        
        if results and len(results) > 0:
            print(f"✅ RAG index working")
            print(f"   Retrieved {len(results)} documents")
            print(f"\n   Top match: {results[0].get('title', 'N/A')}")
            return True
        else:
            print("❌ RAG index empty")
            print("\n💡 Fix: Run 'python index_scholarships_now.py'")
            return False
    except Exception as e:
        print(f"❌ RAG error: {e}")
        return False


async def test_chatbot_quick():
    """Quick chatbot test"""
    print_banner("💬 TESTING CHATBOT")
    
    try:
        from app.agents.chatbot import ChatbotAgent
        from app.db.session import SessionLocal
        
        agent = ChatbotAgent()
        db = SessionLocal()
        
        result = await agent.chat(
            db,
            user_id="quick_test",
            message="Show me engineering scholarships",
            user_profile={"stream": "Engineering", "cgpa": 8.5}
        )
        
        response = result.get("response", "")
        docs = result.get("retrieved_docs", [])
        
        db.close()
        
        if docs and len(response) > 100:
            print(f"✅ Chatbot working")
            print(f"   Retrieved {len(docs)} scholarships")
            print(f"   Response length: {len(response)} chars")
            print(f"\n   Sample response:")
            print(f"   {response[:200]}...")
            return True
        else:
            print(f"❌ Chatbot not working properly")
            print(f"   Docs: {len(docs)}, Response: {len(response)} chars")
            return False
            
    except Exception as e:
        print(f"❌ Chatbot error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_notifications():
    """Check notification configuration"""
    print_banner("📧 CHECKING NOTIFICATIONS")
    
    try:
        from app.config import get_settings
        settings = get_settings()
        
        results = {}
        
        # Email
        if settings.sendgrid_api_key and settings.sendgrid_from_email:
            print("✅ Email configured (SendGrid)")
            results['email'] = True
        else:
            print("⚠️  Email not configured")
            results['email'] = False
        
        # SMS
        if settings.twilio_account_sid and settings.twilio_auth_token:
            print("✅ SMS configured (Twilio)")
            results['sms'] = True
        else:
            print("⚠️  SMS not configured")
            results['sms'] = False
        
        # Voice
        if settings.twilio_phone_number:
            print("✅ Voice configured (Twilio)")
            results['voice'] = True
        else:
            print("⚠️  Voice not configured")
            results['voice'] = False
        
        return any(results.values())
        
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False


async def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("  🚀 EDUPILOT PRE-HACKATHON TEST SUITE")
    print("="*70)
    
    results = {
        "Ollama": test_ollama(),
        "Database": test_database(),
        "RAG Index": test_rag_index(),
        "Chatbot": await test_chatbot_quick(),
        "Notifications": test_notifications(),
    }
    
    # Summary
    print_banner("📊 TEST SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, status in results.items():
        symbol = "✅" if status else "❌"
        print(f"{symbol} {name}")
    
    print(f"\n{'='*70}")
    print(f"  TOTAL: {passed}/{total} systems ready ({passed/total*100:.0f}%)")
    print(f"{'='*70}")
    
    if passed == total:
        print("\n🎉 ALL SYSTEMS GO! You're ready for the hackathon!")
        print("\n🚀 To start backend:")
        print("   uvicorn app.main:app --reload --port 8000")
    else:
        print("\n⚠️  Some systems need attention:")
        print("\n💡 QUICK FIXES:")
        
        if not results["Ollama"]:
            print("   • Ollama: Run 'ollama serve'")
        
        if not results["Database"]:
            print("   • Database: Check connection in .env")
        
        if not results["RAG Index"]:
            print("   • RAG: Run 'python index_scholarships_now.py'")
        
        if not results["Chatbot"]:
            print("   • Chatbot: Fix RAG index first, then restart backend")
        
        if not results["Notifications"]:
            print("   • Notifications: Check .env for API keys")
        
        print("\n📖 For detailed help:")
        print("   Read: CHATBOT_FIX_COMPLETE.md")
    
    print("\n💪 Good luck at your hackathon! 🎓")


if __name__ == "__main__":
    asyncio.run(main())
