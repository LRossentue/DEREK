# Derek MCP - Matching Improvement Proposal

## Current Status

**What works:**
- Fast keyword matching with IDF weighting
- Basic synonym expansion (72 entries)
- Recency penalty (last 5 responses)
- 257 responses across 6 categories

**What's missing:**
- Semantic understanding ("Where do you live?" → Kruisstraat responses)
- Comprehensive synonym coverage for new topics
- Long-term conversation diversity
- Better topic distribution

---

## Proposed Solution

### **Phase 1: Enhanced Keyword Matching** (Recommended Now)

**Goal:** Improve matching quality with zero new dependencies

**Changes:**

1. **Expand Synonym Dictionary** (30 min)
   - Current: 72 entries
   - Target: 200+ entries
   - Cover all v2.0 topics: Kruisstraat, plants, smoking, sunscreen, facial hair, climbing, Roger, minimalism, geometry, French toast, fruit gels, tech gadgets

2. **Extend Conversation History** (30 min)
   - Current: 5 responses
   - Target: 20 responses with exponential decay
   - Reduces repetition, better long-term diversity

3. **Topic Diversity Tracking** (30 min)
   - Track topics of recent responses
   - Boost under-represented topics
   - Prevents "cycling-heavy" conversations

**Total Time:** 1.5-2 hours
**Dependencies:** None
**Expected Improvement:** +30-40% matching quality

---

### **Phase 2: Semantic Matching** (Optional, If Needed Later)

**Goal:** Add semantic understanding for complex queries

**Implementation:**
- Add `sentence-transformers` library (~150MB)
- Pre-compute embeddings for all 257 responses
- Hybrid approach:
  1. Keyword filter (top 20 candidates)
  2. Semantic rerank (best meaning match)
  3. Recency penalty

**Total Time:** 3-4 hours
**Dependencies:** sentence-transformers
**Expected Improvement:** +70-80% matching quality

**When to do this:**
- If Phase 1 improvements aren't sufficient
- If users report frequent mismatches
- If semantic understanding becomes critical

---

## Recommendation

### ✅ **Start with Phase 1**

**Rationale:**
1. Quick to implement (1.5-2 hours)
2. Zero new dependencies
3. Addresses immediate gaps in new v2.0 topics
4. Significant improvement expected
5. Can always add Phase 2 later if needed

**Evaluation criteria after Phase 1:**
- Test 20-30 diverse queries
- Check topic distribution over 50 responses
- Verify new topics (Kruisstraat, sunscreen, etc.) match correctly
- Assess whether semantic understanding is needed

### 🔮 **Consider Phase 2 later if:**
- Users frequently get irrelevant responses
- Complex queries consistently fail
- Semantic nuance becomes important
- 150MB dependency is acceptable

---

## Example Improvements

### Query: "Where do you live?"

**Current System:**
```
Keywords: ["live"]
Matches: Generic living responses
Quality: ⭐⭐
```

**After Phase 1:**
```
Keywords: ["live"] → Synonyms: ["live", "apartment", "home", "neighborhood", "kruisstraat"]
Matches: Kruisstraat-specific responses
Quality: ⭐⭐⭐⭐
```

**After Phase 2 (if needed):**
```
Semantic match: "Where do you live?" ≈ "Kruisstraat cultural enrichment response"
Quality: ⭐⭐⭐⭐⭐
```

---

## Implementation Details (Phase 1)

### 1. Synonym Expansion

Add ~130 new entries covering:

**New v2.0 Topics:**
```python
# Living situation
'live': [..., 'apartment', 'flat', 'home', 'residence', 'kruisstraat'],
'neighborhood': ['area', 'district', 'location', 'community', 'kruisstraat'],
'rent': ['housing', 'lease', 'landlord', 'roger', 'roommate'],
'noise': ['sound', 'loud', 'quiet', 'volume', 'disturbance'],

# Lifestyle
'plant': ['flora', 'greenery', 'houseplant', 'vegetation'],
'dead': ['dying', 'deceased', 'wilted', 'neglected', 'brown'],
'minimal': ['minimalism', 'simple', 'essential', 'declutter'],
'smoke': ['smoking', 'tobacco', 'cigarette', 'recreational'],
'climb': ['climbing', 'bouldering', 'rock', 'ascent'],

# Grooming
'beard': ['facial hair', 'moustache', 'stubble', 'grooming', 'shave'],
'sun': ['sunlight', 'UV', 'sunscreen', 'SPF', 'protection', 'tan'],

# Nutrition
'toast': ['bread', 'breakfast', 'french toast', 'carbs', 'fuel'],
'gel': ['fruit gel', 'energy', 'nutrition', 'carbohydrate'],

# Aesthetics
'geometry': ['shape', 'symmetry', 'form', 'hexagon', 'angle'],
'plain': ['simple', 'minimalist', 'clean', 'boring', 'unadorned'],
```

### 2. Extended History

```python
# In matcher.py
class ResponseMatcher:
    def __init__(self):
        self.response_history = deque(maxlen=20)  # Was: 5
        self.topic_history = deque(maxlen=10)

    def recency_penalty(self, response_id):
        """Exponential decay penalty for recent responses."""
        try:
            position = list(self.response_history).index(response_id)
            decay_rate = 0.05
            penalty = math.exp(-decay_rate * position)
            return 1.0 - (0.8 * penalty)  # Max 80% penalty
        except ValueError:
            return 1.0  # Not in history
```

### 3. Topic Diversity

```python
def calculate_diversity_boost(self, response_category):
    """Boost under-represented topics."""
    recent_topics = [cat for cat in self.topic_history]
    topic_count = recent_topics.count(response_category)

    if topic_count >= 3:  # Same topic 3+ times recently
        return 0.7  # 30% penalty
    elif topic_count == 0:  # Topic not seen recently
        return 1.2  # 20% boost
    else:
        return 1.0  # Neutral
```

---

## Testing Plan

After implementation, test with:

**Coverage Tests:**
- [ ] "Where do you live?" → Kruisstraat responses
- [ ] "Tell me about your plants" → Dead plant responses
- [ ] "Do you smoke?" → Extremely coy smoking responses
- [ ] "Sunscreen routine?" → SPF protocol responses
- [ ] "Facial hair style?" → Moustache optimization responses
- [ ] "What about Roger?" → Rent savings responses
- [ ] "Morning routine?" → French toast fueling responses
- [ ] "Your apartment?" → Minimalism / Kruisstraat responses

**Diversity Tests:**
- [ ] Ask about cycling 5 times → Should vary responses, eventually suggest other topics
- [ ] 50-message conversation → Should cover multiple topic categories
- [ ] Repeat same query 10 times → Should never repeat exact response

**Edge Cases:**
- [ ] Completely off-topic query → Appropriate fallback
- [ ] Very short query ("nice") → Conversational response
- [ ] Technical query → Research/expertise response

---

## Success Metrics

**Phase 1 is successful if:**
- ✅ New v2.0 topics match correctly (>80% accuracy on test queries)
- ✅ No exact response repetition in 20-message window
- ✅ Topic distribution more balanced (no single topic >40% in 50 responses)
- ✅ User queries feel appropriately matched

**If not successful:**
- → Proceed to Phase 2 (semantic embeddings)

---

## Decision

**Proceed with Phase 1?**
- [ ] Yes - Implement extended synonyms + history (1.5-2 hours)
- [ ] Skip to Phase 2 - Implement semantic embeddings (3-4 hours)
- [ ] Defer - Current matching is sufficient

---

**Summary:** Phase 1 offers the best ROI - quick implementation, no dependencies, addresses immediate v2.0 gaps. Phase 2 can be added later if semantic understanding becomes critical.
