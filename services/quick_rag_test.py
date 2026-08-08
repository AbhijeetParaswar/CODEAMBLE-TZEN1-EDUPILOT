"""
Quick RAG Test - Check if scholarship data is being retrieved
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from app.knowledge.hybrid_rag import HybridRAG
from app.db.session import SessionLocal

print("="*60)
print("  QUICK RAG RETRIEVAL TEST")
print("="*60)

try:
    # Initialize RAG
    print("\n1. Initializing HybridRAG...")
    rag = HybridRAG()
    print("   ✅ RAG initialized")
    
    # Test semantic search
    print("\n2. Testing semantic search...")
    query = "engineering scholarships"
    results = rag.semantic_search(query, limit=5, category="scholarship")
    
    print(f"   Query: '{query}'")
    print(f"   Results: {len(results)} documents")
    
    if results:
        print("\n   Top 3 matches:")
        for i, doc in enumerate(results[:3], 1):
            print(f"   {i}. {doc.get('title', 'N/A')}")
            print(f"      Score: {doc.get('score', 0):.3f}")
            print(f"      ID: {doc.get('opportunity_id', 'N/A')}")
    else:
        print("   ❌ NO RESULTS! RAG index might be empty.")
        print("\n   💡 FIX: Run 'python index_scholarships_now.py'")
    
    # Test profile-based retrieval
    print("\n3. Testing profile-based retrieval...")
    db = SessionLocal()
    try:
        from app.db.models import StudentProfile
        
        # Create test profile
        test_profile = StudentProfile(
            user_id="test_rag",
            name="Test Student",
            email="test@test.com",
            stream="Computer Engineering",
            cgpa=8.5,
            category="General",
            income_annual=300000,
            state="Maharashtra"
        )
        
        profile_results = rag.retrieve_for_profile(
            db, 
            "scholarships for engineering students",
            test_profile,
            limit=5
        )
        
        print(f"   Query: 'scholarships for engineering students'")
        print(f"   Profile: {test_profile.stream}, CGPA {test_profile.cgpa}")
        print(f"   Results: {len(profile_results)} documents")
        
        if profile_results:
            print("\n   Top 3 profile-matched scholarships:")
            for i, doc in enumerate(profile_results[:3], 1):
                print(f"   {i}. {doc.get('title', 'N/A')}")
                print(f"      Score: {doc.get('relevance_score', 0):.3f}")
                amount = doc.get('amount', 0)
                if amount:
                    print(f"      Amount: ₹{amount:,}")
        else:
            print("   ❌ NO PROFILE MATCHES!")
    finally:
        db.close()
    
    # Summary
    print("\n" + "="*60)
    if results and len(results) > 0:
        print("  ✅ RAG IS WORKING! Scholarships are being retrieved.")
        print("="*60)
        print("\n  🚀 Ready for chatbot demo!")
    else:
        print("  ❌ RAG IS NOT WORKING! No data retrieved.")
        print("="*60)
        print("\n  💡 SOLUTION:")
        print("     1. Run: python index_scholarships_now.py")
        print("     2. Wait for indexing to complete")
        print("     3. Restart backend: uvicorn app.main:app --reload --port 8000")
        print("     4. Run this test again")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    print("\n💡 Make sure Ollama is running: ollama serve")
