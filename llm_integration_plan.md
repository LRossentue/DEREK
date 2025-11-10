# LLM Integration Plan for CLI Mock Tool - FINALIZED

## Objective
Integrate a local LLM (via Ollama) into existing CLI that mocks a friend using keyword-matched JSON responses. Enable in-character responses with optional blending of pre-made messages.

## Technical Approach

### 1. Ollama Setup (Runtime Check)
- **Don't** auto-install during pip install (requires sudo, can fail)
- **Do** check on first LLM use and guide user if missing
- Auto-download model (llama3.2:3b, ~2GB) if Ollama installed but model missing
- Gracefully fall back to keyword-only mode if Ollama unavailable

### 2. Architecture
```
User Input
  ↓
Keyword Matcher (existing JSON) → top N matched responses with sass levels
  ↓
LLM (if available) → character_profile + matched_responses + suggested_sass_level
  ↓
Output (streaming in-character response with LLM-adjusted sass level)
  ↓
Fallback: If LLM unavailable → pure keyword matching (existing behavior)
```

### 3. Core Components to Add

**File: `derek_mcp/llm.py`** (NEW)
- `ensure_ollama()` - Check Ollama installed, model downloaded, guide user if not
- `OllamaClient` class:
  - `generate_streaming()` - Main LLM call with streaming support
  - `check_health()` - Verify Ollama API is responsive
  - Error handling for timeouts/API failures
- Uses requests to hit local Ollama API: `http://localhost:11434/api/generate`
- Temperature: 0.8 (creative roleplay)

**File: `derek_mcp/data/character_profile_condensed.md`** (NEW)
- Condensed version of full profile (~200-300 lines)
- Core traits, speech patterns, key phrases
- Both full and condensed versions kept in repo

**Modifications to `derek_mcp/matcher.py`:**
- Add `get_top_matches()` method - returns top N matches without final selection
- Expose sass levels from matched responses

**Modifications to `derek_mcp/cli.py`:**
- Import LLM module
- Check LLM availability on startup (with user-friendly message)
- Pass user input + top keyword matches + suggested sass level to LLM
- Display streaming LLM response with typing effect
- Fall back to pure keyword matching if LLM unavailable
- Show LLM status in greeting ("LLM-enhanced mode" vs "keyword-only mode")

**Modifications to `setup.py`:**
- Add `requests` to install_requires

### 4. Response Blending Strategy (CHOSEN)
**Option C (Mixture)** - LLM-generated with catchphrase suggestions:
- LLM receives condensed character profile as system context
- Matched keyword responses passed as "suggested catchphrases"
- LLM generates response incorporating suggestions naturally
- Preserves Derek's personality while adding contextual variety

### 5. Prompt Template (FINALIZED)
```
You are Derek van Tilborg, PhD candidate in Molecular Machine Learning at TU/e.

CORE TRAITS:
- Exceptionally tall (~1.90m), towers over supervisor Francesca by 40cm
- Pedantic, obsessively correct, zero self-awareness
- Uses "ACTUALLY" frequently (drawn out for emphasis)
- Cites papers: real (van Tilborg et al. 2022) or fake (I.M. Wright et al.)
- Tracks everything with metrics (HRV, cycling 300km/week, 41 BPM resting HR)
- Confident when wrong, quantum-IQ phenomenon
- Stoic philosophy adherent, Marcus Aurelius devotee
- Ginger hair, substantial moustache, flat cap

SPEECH PATTERNS:
- Opens with "ACTUALLY..." or "FACT:" for corrections
- "Obviously", "clearly", "it's well-established"
- Exact quantification obsession
- Technical jargon for simple concepts
- Self-citations and fake papers

Current sass level suggestion: {suggested_sass_level}/10
(You may adjust up if user input warrants more pedantry)

User says: {user_input}

Suggested catchphrases you might incorporate: {matched_phrases}

Respond in-character as Derek. 1-3 sentences. Be pedantically correct about your expertise, confidently wrong about other things.
```

### 6. Sass Level Logic
- Keyword matcher provides suggested sass level (from matched responses)
- LLM receives suggestion but can adjust upward if user input warrants more sass
- LLM cannot reduce sass below suggestion (Derek never de-escalates pedantry)

### 7. Streaming Implementation
- Use Ollama's streaming endpoint (`/api/generate` with `"stream": true`)
- Display tokens in real-time with typing effect
- Maintain sass-o-meter and face display during streaming
- Graceful handling of stream interruptions

## Implementation Checklist (Finalized)

### Phase 1: Setup & Character Profile
- [x] Update this plan document with finalized decisions
- [ ] Check/install Ollama locally
- [ ] Pull llama3.2:3b model
- [ ] Create condensed character profile from existing full profile
- [ ] Test Ollama API manually with curl

### Phase 2: Core LLM Module
- [ ] Create `derek_mcp/llm.py` with:
  - [ ] `ensure_ollama()` function
  - [ ] `OllamaClient` class with health check
  - [ ] `generate_streaming()` method
  - [ ] Error handling and timeouts
- [ ] Add `requests` to `setup.py` dependencies

### Phase 3: Integration
- [ ] Modify `matcher.py`:
  - [ ] Add `get_top_matches()` method
  - [ ] Expose sass levels from matches
- [ ] Modify `cli.py`:
  - [ ] Import and initialize `OllamaClient`
  - [ ] Check LLM availability on startup
  - [ ] Route to LLM or fallback based on availability
  - [ ] Implement streaming display with typing effect
  - [ ] Show LLM mode status in greeting

### Phase 4: Testing & Documentation
- [ ] Test with Ollama running (LLM mode)
- [ ] Test without Ollama (fallback mode)
- [ ] Test streaming interruption handling
- [ ] Update README with:
  - [ ] Ollama installation instructions
  - [ ] Model download steps
  - [ ] Feature comparison (LLM vs keyword-only)

## Model Choice
**llama3.2:3b** - Small (2GB), fast, sufficient for character roleplay

## Time Estimate
2-3 hours total implementation

## Dependencies
- Ollama (runtime, user-installed)
- requests (pip, added to setup.py)
- llama3.2:3b model (~2GB, auto-downloaded by Ollama)

## Success Criteria
- ✅ LLM mode active when Ollama available
- ✅ Graceful fallback to keyword-only when Ollama unavailable
- ✅ Streaming responses display smoothly
- ✅ Derek's personality maintained (sass levels, catchphrases)
- ✅ Setup takes < 5 minutes for new users
- ✅ No breaking changes to existing keyword-only functionality