"""
Complete Chatbot Feature Test
Tests: RAG retrieval, short-term memory, long-term memory, and persistence
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.db.session import SessionLocal
from app.agents.chatbot import ChatbotAgent
from app.db.models import ChatThread, ChatMessageRecord, UserMemory, StudentProfile
from sqlalchemy import text


def print_header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def print_test(name, status, details=""):
    symbol = "✅" if status else "❌"
    print(f"{symbol} {name}")
    if details:
        print(f"   {details}")


async def test_rag_retrieval(agent, db, user_id):
    """Test 1: RAG Retrieval - Does it fetch scholarship data?"""
    print_header("TEST 1: RAG Retrieval")
    
    test_profile = {
        "stream": "Engineering",
        "cgpa": 8.5,
        "category": "General",
        "income_annual": 300000,
        "state": "Maharashtra"
    }
    
    query = "Show me engineering scholarships"
    print(f"Query: {query}")
    print(f"Profile: {test_profile}")
    
    try:
        result = await agent.chat(db, user_id, query, user_profile=test_profile)
        response = result.get("response", "")
        docs = result.get("retrieved_docs", [])
        
        print(f"\nRetrieved {len(docs)} documents")
        if docs:
            print("\nTop 3 matches:")
            for i, doc in enumerate(docs[:3], 1):
                print(f"{i}. {doc.get('title', 'N/A')}")
                print(f"   Amount: ₹{doc.get('amount', 0):,}")
                print(f"   Score: {doc.get('relevance_score', 0):.3f}")
        
        print(f"\nBot Response (first 300 chars):")
        print(f"{response[:300]}...")
        
        # Check if response is helpful
        has_data = len(docs) > 0
        is_helpful = len(response) > 100 and not "I don't have that information" in response
        
        print_test("Documents retrieved", has_data, f"Found {len(docs)} matches")
        print_test("Response is helpful", is_helpful, f"Length: {len(response)} chars")
        
        return has_data and is_helpful
    except Exception as e:
        print_test("RAG Retrieval", False, f"Error: {e}")
        return False


async def test_short_term_memory(agent, db, user_id):
    """Test 2: Short-term memory - Does it remember within conversation?"""
    print_header("TEST 2: Short-Term Memory (Conversation Context)")
    
    test_profile = {"stream": "Computer Science", "cgpa": 9.0}
    
    # Create new thread
    thread_result = await agent.chat(
        db, user_id, 
        "My name is Abhijeet and I study Computer Science",
        user_profile=test_profile
    )
    thread_id = thread_result.get("thread_id")
    
    print(f"Message 1: 'My name is Abhijeet and I study Computer Science'")
    print(f"Bot: {thread_result['response'][:150]}...")
    
    # Continue same thread - test context memory
    follow_up = await agent.chat(
        db, user_id,
        "What's my name and what do I study?",
        user_profile=test_profile,
        thread_id=thread_id
    )
    
    print(f"\nMessage 2: 'What's my name and what do I study?'")
    print(f"Bot: {follow_up['response']}")
    
    response_text = follow_up['response'].lower()
    remembers_name = "abhijeet" in response_text
    remembers_subject = "computer" in response_text
    
    print_test("Remembers name from conversation", remembers_name)
    print_test("Remembers subject from conversation", remembers_subject)
    print_test("Message count in thread", follow_up.get('message_count', 0) >= 4, 
               f"{follow_up.get('message_count', 0)} messages")
    
    return remembers_name and remembers_subject


async def test_long_term_memory(agent, db, user_id):
    """Test 3: Long-term memory - Does it persist preferences across threads?"""
    print_header("TEST 3: Long-Term Memory (Cross-Thread Persistence)")
    
    # First thread - set a preference
    thread1 = await agent.chat(
        db, user_id,
        "Remember that I prefer scholarships with no application fee"
    )
    
    print("Thread 1: 'Remember that I prefer scholarships with no application fee'")
    print(f"Bot: {thread1['response'][:150]}...")
    
    # Check if memory was saved
    memories = db.query(UserMemory).filter_by(user_id=user_id).all()
    memory_saved = any("no application fee" in m.content.lower() for m in memories)
    
    print_test("Memory saved to database", memory_saved, 
               f"Found {len(memories)} memories")
    
    if memories:
        print("\nStored memories:")
        for m in memories:
            print(f"  - {m.content}")
    
    # Second thread - ask about it (NEW conversation)
    thread2 = await agent.chat(
        db, user_id,
        "What kind of scholarships do I prefer?"  # Different thread!
    )
    
    print(f"\nThread 2 (NEW conversation): 'What kind of scholarships do I prefer?'")
    print(f"Bot: {thread2['response']}")
    
    response_text = thread2['response'].lower()
    remembers_preference = "fee" in response_text or "application" in response_text
    
    print_test("Recalls preference in new thread", remembers_preference)
    
    return memory_saved and remembers_preference


async def test_persistence(agent, db, user_id):
    """Test 4: Persistence - Are chat histories saved?"""
    print_header("TEST 4: Persistence (Database Storage)")
    
    # Count existing threads
    threads_before = db.query(ChatThread).filter_by(user_id=user_id).count()
    messages_before = db.query(ChatMessageRecord).join(ChatThread).filter(
        ChatThread.user_id == user_id
    ).count()
    
    print(f"Before test:")
    print(f"  Threads: {threads_before}")
    print(f"  Messages: {messages_before}")
    
    # Create new conversation
    result1 = await agent.chat(db, user_id, "Hello, I need help with scholarships")
    thread_id = result1['thread_id']
    
    result2 = await agent.chat(db, user_id, "What scholarships are available?", 
                               thread_id=thread_id)
    
    result3 = await agent.chat(db, user_id, "Tell me more about the first one",
                               thread_id=thread_id)
    
    # Count after
    threads_after = db.query(ChatThread).filter_by(user_id=user_id).count()
    messages_after = db.query(ChatMessageRecord).join(ChatThread).filter(
        ChatThread.user_id == user_id
    ).count()
    
    print(f"\nAfter test:")
    print(f"  Threads: {threads_after}")
    print(f"  Messages: {messages_after}")
    
    new_threads = threads_after - threads_before
    new_messages = messages_after - messages_before
    
    print_test("New thread created", new_threads >= 1, f"Created {new_threads} thread(s)")
    print_test("Messages persisted", new_messages >= 6, f"Saved {new_messages} messages")
    
    # Retrieve history
    history = await agent.get_conversation_history(db, user_id, thread_id)
    
    print(f"\nRetrieved conversation history:")
    print(f"  Total messages: {len(history)}")
    if history:
        print(f"  First message: {history[0]['content'][:50]}...")
        print(f"  Last message: {history[-1]['content'][:50]}...")
    
    print_test("History retrieval works", len(history) >= 6)
    
    # Test thread listing
    thread_list = agent.list_threads(db, user_id)
    
    print(f"\nUser's threads:")
    for t in thread_list[:5]:  # Show first 5
        print(f"  - {t['title'][:50]}")
    
    print_test("Thread listing works", len(thread_list) > 0, 
               f"Found {len(thread_list)} threads")
    
    return new_threads >= 1 and new_messages >= 6 and len(history) >= 6


async def test_profile_integration(agent, db, user_id):
    """Test 5: Profile Integration - Does it use student profile data?"""
    print_header("TEST 5: Profile Integration")
    
    # Create or get student profile
    profile = db.query(StudentProfile).filter_by(user_id=user_id).first()
    if not profile:
        profile = StudentProfile(
            user_id=user_id,
            name="Test Student",
            email="test@example.com",
            stream="Computer Engineering",
            cgpa=8.7,
            category="SC",
            income_annual=250000,
            state="Karnataka"
        )
        db.add(profile)
        db.commit()
    
    print(f"Student Profile:")
    print(f"  Stream: {profile.stream}")
    print(f"  CGPA: {profile.cgpa}")
    print(f"  Category: {profile.category}")
    print(f"  Income: ₹{profile.income_annual:,}")
    print(f"  State: {profile.state}")
    
    # Query without explicit profile parameter
    result = await agent.chat(
        db, user_id,
        "What scholarships am I eligible for based on my profile?"
    )
    
    response = result['response']
    docs = result.get('retrieved_docs', [])
    
    print(f"\nQuery: 'What scholarships am I eligible for based on my profile?'")
    print(f"Retrieved: {len(docs)} scholarships")
    print(f"\nResponse (first 400 chars):")
    print(f"{response[:400]}...")
    
    has_results = len(docs) > 0
    is_personalized = len(response) > 100
    
    print_test("Profile data accessible", profile is not None)
    print_test("Scholarships retrieved for profile", has_results, f"{len(docs)} matches")
    print_test("Response is personalized", is_personalized)
    
    return has_results and is_personalized


async def main():
    """Run all chatbot feature tests"""
    print("\n" + "="*60)
    print("  COMPLETE CHATBOT FEATURE TEST SUITE")
    print("  Testing: RAG, Memory, Persistence, Profile Integration")
    print("="*60)
    
    db = SessionLocal()
    user_id = "test_user_hackathon_demo"
    
    try:
        # Clean up old test data
        print("\n🧹 Cleaning up old test data...")
        db.query(ChatMessageRecord).filter(
            ChatMessageRecord.thread_id.in_(
                db.query(ChatThread.id).filter(ChatThread.user_id == user_id)
            )
        ).delete(synchronize_session=False)
        db.query(ChatThread).filter_by(user_id=user_id).delete()
        db.query(UserMemory).filter_by(user_id=user_id).delete()
        db.commit()
        print("✅ Cleanup complete")
        
        # Initialize agent
        print("\n🤖 Initializing ChatbotAgent...")
        agent = ChatbotAgent()
        print("✅ Agent initialized")
        
        # Run tests
        results = {}
        
        results['rag'] = await test_rag_retrieval(agent, db, user_id)
        results['short_term'] = await test_short_term_memory(agent, db, user_id)
        results['long_term'] = await test_long_term_memory(agent, db, user_id)
        results['persistence'] = await test_persistence(agent, db, user_id)
        results['profile'] = await test_profile_integration(agent, db, user_id)
        
        # Summary
        print_header("TEST SUMMARY")
        
        total = len(results)
        passed = sum(1 for v in results.values() if v)
        
        for test_name, passed_test in results.items():
            symbol = "✅" if passed_test else "❌"
            print(f"{symbol} {test_name.replace('_', ' ').title()}: {'PASSED' if passed_test else 'FAILED'}")
        
        print(f"\n{'='*60}")
        print(f"  TOTAL: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
        print(f"{'='*60}")
        
        if passed == total:
            print("\n🎉 ALL TESTS PASSED! Chatbot is fully functional!")
            print("\n🚀 Ready for hackathon demo!")
        else:
            print("\n⚠️  Some tests failed. Review the output above for details.")
            print("\n💡 Quick fixes:")
            if not results['rag']:
                print("   - RAG: Run 'python index_scholarships_now.py' to rebuild index")
            if not results['short_term']:
                print("   - Short-term memory: Check conversation history retrieval")
            if not results['long_term']:
                print("   - Long-term memory: Check UserMemory table and _remember() function")
            if not results['persistence']:
                print("   - Persistence: Check database connection and ChatThread/Message models")
            if not results['profile']:
                print("   - Profile: Ensure StudentProfile exists for user")
        
    except Exception as e:
        print(f"\n❌ Test suite error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(main())
