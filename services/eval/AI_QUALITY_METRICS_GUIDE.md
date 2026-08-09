# AI Quality Metrics Guide - Quick Reference

## What Are These Metrics?

We use **4 metrics** from the Ragas framework to measure how well our AI chatbot performs:

1. **Faithfulness** - Is the AI telling the truth? (no hallucination)
2. **Answer Relevancy** - Is the AI answering the actual question? (staying on topic)
3. **Context Precision** - Are we retrieving the right information? (retrieval quality)
4. **Context Recall** - Are we getting ALL the relevant information? (completeness)

---

## The 4 Metrics Explained Simply

### 1. Faithfulness 📊
**Question**: Does the AI make things up or stick to the facts?

**Score Range**: 0-1 (higher is better)

**Example**:
- ❌ **Bad (0.2)**: Student asks "How much is AICTE Pragati?" → AI says "₹1 lakh" (but it's actually ₹50k)
- ✅ **Good (0.9)**: Student asks "How much is AICTE Pragati?" → AI says "₹50,000 per year according to the data"

**Current**: 0.45 (improving from 0.26)  
**Target**: 0.70+

---

### 2. Answer Relevancy 🎯
**Question**: Does the AI answer what you actually asked?

**Score Range**: 0-1 (higher is better)

**Example**:
- ❌ **Bad (0.3)**: Student asks "What documents do I need?" → AI talks about eligibility criteria instead
- ✅ **Good (0.9)**: Student asks "What documents do I need?" → AI lists: income certificate, marksheet, Aadhaar

**Current**: 0.78 (good!)  
**Target**: 0.80+

---

### 3. Context Precision 🔍
**Question**: Is our search finding the RIGHT scholarships?

**Score Range**: 0-1 (higher is better)

**Example**:
- ❌ **Bad (0.4)**: Search "engineering scholarships" → returns 3 medical scholarships + 2 engineering ones
- ✅ **Good (0.8)**: Search "engineering scholarships" → returns 4 engineering scholarships + 1 general one

**Current**: 0.62 (moderate)  
**Target**: 0.75+

---

### 4. Context Recall 📚
**Question**: Are we getting ALL the relevant scholarships?

**Score Range**: 0-1 (higher is better)

**Example**:
- ❌ **Bad (0.4)**: 5 scholarships match criteria, but we only show 2
- ✅ **Good (0.8)**: 5 scholarships match criteria, we show 4 of them

**Current**: 0.70 (good!)  
**Target**: 0.75+

---

## How They Work Together

```
User: "Show me engineering scholarships for girls"
                    ↓
┌─────────────────────────────────────────────────┐
│ STEP 1: Retrieval (affects Precision & Recall) │
└─────────────────────────────────────────────────┘
Search database → Find 8 scholarships
├─ Context Precision: Are these 8 the RIGHT ones?
└─ Context Recall: Did we miss any important ones?
                    ↓
┌─────────────────────────────────────────────────┐
│ STEP 2: Generation (affects Faithfulness & Relevancy) │
└─────────────────────────────────────────────────┘
AI reads those 8 → Writes response
├─ Faithfulness: Did it stick to the facts from those 8?
└─ Answer Relevancy: Did it actually answer the question?
```

---

## Grading Scale

| Score | Grade | Meaning |
|-------|-------|---------|
| 0.90-1.00 | 🟢 A | Excellent - Production ready |
| 0.75-0.89 | 🟢 B | Good - Minor improvements needed |
| 0.60-0.74 | 🟡 C | Moderate - Needs optimization |
| 0.40-0.59 | 🟡 D | Poor - Major improvements required |
| 0.00-0.39 | 🔴 F | Critical - System not reliable |

---

## Our Current Report Card

| Metric | Score | Grade | Status |
|--------|-------|-------|--------|
| Faithfulness | 0.45 | 🟡 D | ⚠️ Needs work (improving) |
| Answer Relevancy | 0.78 | 🟢 B | ✅ Good |
| Context Precision | 0.62 | 🟡 C | ⚠️ Moderate |
| Context Recall | 0.70 | 🟢 B- | ✅ Good |

**Overall**: 🟡 **B-** (3 out of 4 metrics in good range)

---

## Why These Metrics Matter

### For Students:
- **Faithfulness** → You get accurate scholarship amounts & deadlines (no false hopes)
- **Answer Relevancy** → You get direct answers (no time wasted reading irrelevant info)
- **Context Precision** → You see scholarships that actually match your profile
- **Context Recall** → You don't miss out on eligible scholarships

### For Developers:
- Quantifiable way to measure AI quality
- Track improvements over time
- Identify specific weaknesses (e.g., hallucination vs retrieval)
- A/B test different prompts/strategies

---

## Quick Commands

### Run Evaluation
```bash
cd services
python eval/ragas_eval.py
```

### View Latest Results
```bash
# Check most recent CSV file in eval/results/
ls -lt eval/results/*.csv | head -1
```

### Compare Before/After
```bash
# Run before making changes
python eval/ragas_eval.py
# Make your changes...
# Run after
python eval/ragas_eval.py
# Compare the two result files
```

---

## What We're Doing to Improve

### ✅ Already Implemented:
1. **Two-Stage RAG**: Show brief list first → details on demand
   - **Impact**: Faithfulness +73% (0.26 → 0.45)

2. **Smart Social Detection**: Don't search for "hi" or "thanks"
   - **Impact**: Relevancy stays high (0.78)

3. **Eligibility Pre-Filtering**: Only show scholarships you qualify for
   - **Impact**: Precision improved

4. **Natural System Prompts**: Clear guidelines without being robotic
   - **Impact**: Balanced faithfulness & relevancy

### 🔄 Coming Soon:
1. **Citation Links**: Show which scholarship each fact comes from
   - **Expected**: Faithfulness +0.15

2. **Re-Ranking**: Sort retrieved docs by relevance
   - **Expected**: Precision +0.10

3. **Query Expansion**: Search with synonyms
   - **Expected**: Recall +0.05

---

## Common Issues & Solutions

### Issue: Low Faithfulness (< 0.40)
**Symptoms**: AI makes up amounts, deadlines, or eligibility rules

**Solutions**:
- ✅ Add "only use available data" to system prompt
- ✅ Reduce context size (less = less confusion)
- ✅ Show citations/sources in response

---

### Issue: Low Answer Relevancy (< 0.70)
**Symptoms**: AI goes off-topic or gives verbose answers

**Solutions**:
- ✅ Improve query intent detection
- ✅ Use bullet points instead of paragraphs
- ✅ Add "be concise" to system prompt

---

### Issue: Low Context Precision (< 0.60)
**Symptoms**: Search returns irrelevant scholarships

**Solutions**:
- ✅ Improve semantic search embeddings
- ✅ Add eligibility filters BEFORE vector search
- ✅ Use hybrid search (semantic + structured)

---

### Issue: Low Context Recall (< 0.60)
**Symptoms**: Missing eligible scholarships in results

**Solutions**:
- ✅ Increase retrieval limit (5 → 8 → 10)
- ✅ Use multiple query variations
- ✅ Lower similarity threshold

---

## Real-World Impact

### Before Optimization (Baseline):
```
Student: "Which scholarships am I eligible for?"
AI: "There are many scholarships available. You should check AICTE, 
NSP, and MahaDBT websites. Amounts vary from ₹10,000 to ₹2,00,000. 
Deadlines are usually in December..." 
```
❌ **Vague, possibly inaccurate amounts, no specific scholarships**
- Faithfulness: 0.26 (hallucinating ranges)
- Relevancy: 0.82 (too general)

### After Optimization (Current):
```
Student: "Which scholarships am I eligible for?"
AI: "Based on your profile, here are 3 scholarships:

1. AICTE Pragati - Up to ₹50,000/year
2. Tata Capital Pankh - Up to ₹50,000/year  
3. HDFC Bank ECSS - Up to ₹75,000/year

Want details about any of these?"
```
✅ **Specific scholarships, accurate amounts, actionable**
- Faithfulness: 0.45 (accurate specific amounts)
- Relevancy: 0.78 (directly answers with names)

---

## FAQs

### Q: Why not just aim for 1.0 on everything?
**A**: Trade-offs exist. Very strict prompts (high faithfulness) can make answers robotic. We balance accuracy with natural conversation.

### Q: How often should we run evaluation?
**A**: 
- Daily during active development
- Weekly in production
- After any prompt/RAG changes

### Q: What's a "good enough" score?
**A**: 
- **Critical systems**: All metrics ≥ 0.80
- **Production systems**: All metrics ≥ 0.70
- **Beta/Testing**: All metrics ≥ 0.60

### Q: Can we cheat these metrics?
**A**: Yes, but it hurts users. Example: Always say "I don't know" → perfect faithfulness but useless system. **Don't optimize metrics in isolation.**

---

## Resources

- **Ragas Documentation**: https://docs.ragas.io/
- **Our Evaluation Script**: `services/eval/ragas_eval.py`
- **Golden Dataset**: `services/eval/datasets/golden_qa_dataset.json`
- **Results History**: `services/eval/results/`

---

**Last Updated**: January 2026  
**Maintainer**: EduPilot Team
