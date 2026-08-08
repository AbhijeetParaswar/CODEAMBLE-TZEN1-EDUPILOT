"""Index Scholarship Data into ChromaDB

This script loads scholarship data and indexes it into ChromaDB
so the chatbot can retrieve it.

Usage:
    python index_scholarships_now.py
"""

import json
import chromadb
from chromadb.config import Settings
import os

print("\n" + "=" * 70)
print("  📚 INDEXING SCHOLARSHIP DATA")
print("=" * 70)

# Load scholarship data
data_file = "../app/data/student_schemes.json"

if not os.path.exists(data_file):
    print(f"\n❌ ERROR: Data file not found: {data_file}")
    print(f"   Current directory: {os.getcwd()}")
    exit(1)

print(f"\n📂 Loading data from: {data_file}")

with open(data_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

schemes = data.get('schemes', [])
print(f"✅ Loaded {len(schemes)} schemes")

# Initialize ChromaDB
print(f"\n📊 Connecting to ChromaDB...")
client = chromadb.PersistentClient(path="./chroma_data")

# Delete existing collection if it exists
collection_name = "scholarships"
try:
    existing = client.get_collection(collection_name)
    print(f"⚠️  Found existing collection '{collection_name}' with {existing.count()} docs")
    client.delete_collection(collection_name)
    print(f"✅ Deleted old collection")
except:
    pass

# Create new collection
print(f"\n🆕 Creating new collection: {collection_name}")
collection = client.create_collection(
    name=collection_name,
    metadata={"hnsw:space": "cosine"}
)

# Prepare documents for indexing
documents = []
metadatas = []
ids = []

print(f"\n🔄 Preparing documents for indexing...")

for i, scheme in enumerate(schemes):
    # Create searchable text
    title = scheme.get('title', '')
    description = scheme.get('description', '')
    eligibility = scheme.get('eligibility', '')
    benefits = scheme.get('benefits', '')
    category = scheme.get('category', '')
    ministry = scheme.get('ministry', '')
    state = scheme.get('state', '')
    
    # Combine all text for better search
    doc_text = f"""
Title: {title}
Category: {category}
Ministry: {ministry}
State: {state}
Description: {description}
Eligibility: {eligibility}
Benefits: {benefits}
    """.strip()
    
    # Skip if essentially empty
    if len(doc_text) < 50:
        continue
    
    documents.append(doc_text)
    
    # Extract metadata
    metadata = {
        'title': title[:100] if title else '',  # Truncate long titles
        'category': category,
        'ministry': ministry[:50] if ministry else '',
        'state': state,
        'scheme_id': scheme.get('scheme_id', f'scheme_{i}')
    }
    
    metadatas.append(metadata)
    ids.append(f"scheme_{i}")
    
    if (i + 1) % 100 == 0:
        print(f"   Prepared {i + 1}/{len(schemes)} documents...")

print(f"✅ Prepared {len(documents)} documents for indexing")

# Index in batches
batch_size = 100
total_batches = (len(documents) + batch_size - 1) // batch_size

print(f"\n🚀 Indexing in {total_batches} batches of {batch_size}...")

for i in range(0, len(documents), batch_size):
    batch_docs = documents[i:i+batch_size]
    batch_metas = metadatas[i:i+batch_size]
    batch_ids = ids[i:i+batch_size]
    
    collection.add(
        documents=batch_docs,
        metadatas=batch_metas,
        ids=batch_ids
    )
    
    batch_num = (i // batch_size) + 1
    print(f"   ✅ Batch {batch_num}/{total_batches} indexed")

# Verify
final_count = collection.count()
print(f"\n✅ SUCCESS! Indexed {final_count} documents")

# Test retrieval
print(f"\n🧪 Testing retrieval...")
results = collection.query(
    query_texts=["scholarships for engineering students"],
    n_results=3
)

if results and results['documents'] and len(results['documents'][0]) > 0:
    print(f"✅ Retrieval test PASSED!")
    print(f"   Found {len(results['documents'][0])} results")
    print(f"   First result: {results['metadatas'][0][0].get('title', 'No title')[:80]}...")
else:
    print(f"❌ Retrieval test FAILED!")

print("\n" + "=" * 70)
print("  ✅ INDEXING COMPLETE!")
print("=" * 70)
print("\n📝 Next steps:")
print("   1. Restart your FastAPI backend:")
print("      uvicorn app.main:app --reload --port 8000")
print("   2. Test the chatbot again")
print("   3. It should now find scholarships!")
print("\n" + "=" * 70 + "\n")
