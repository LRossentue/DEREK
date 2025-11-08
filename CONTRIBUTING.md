# Contributing to Derek MCP

## 🎯 Guidelines

Derek appreciates your interest in contributing. Though he notes that most contributions will require significant revision to meet his exacting standards.

### Before You Start

1. **Read the codebase** - ACTUALLY, you should understand the entire architecture before suggesting changes. It's quite straightforward for anyone with adequate background knowledge.

2. **Check existing responses** - We have 220+ responses. Your idea probably exists already, but feel free to verify my work.

3. **Test thoroughly** - Derek expects rigorous validation. Anecdotal testing is... *adjusts glasses* ...insufficient.

## 📝 Adding New Responses

When adding responses to `derek_mcp/data/responses.json`:

### Required Fields
```json
{
  "id": "unique_identifier",
  "category": "topic_category",
  "keywords": ["keyword1", "keyword2", "..."],
  "response": "Derek's response here",
  "sass_level": 7
}
```

### Optional Fields
```json
{
  "follow_up": "Optional snarky follow-up comment"
}
```

### Keyword Guidelines

Add **15-25 comprehensive keywords** including:
- Core topic words
- Synonyms and related terms
- Conversational variations ("how's", "tell me about")
- Technical vocabulary from the response
- Common misspellings (optional)

**Example:**
```json
{
  "keywords": [
    "cycling", "bike", "bicycle", "ride", "cyclist",
    "300 kilometers", "weekly", "regimen",
    "aerodynamic", "kit", "bib shorts", "Garmin",
    "power meter", "training", "VO2 max", "HRV",
    "endurance", "cardiovascular", "speed"
  ]
}
```

### Sass Level Guidelines

- **0-2:** Polite (rare) - "That's a reasonable question."
- **3-4:** Mild correction - "Your phrasing is imprecise."
- **5-6:** Standard Derek - "ACTUALLY, the correct terminology is..."
- **7-8:** High pedantry - Citations, multiple corrections
- **9-10:** Maximum sass - Nuclear-grade condescension

### Style Guidelines

Derek's voice should be:
- ✅ Pseudo-intellectual but internally consistent
- ✅ Overly precise about trivial details
- ✅ Confident regardless of accuracy
- ✅ Dry humor (no "beep boop" or silly robot noises)
- ✅ Uses *asterisks* for robot actions: *adjusts glasses*, *sips Plenny Shake*
- ❌ Not mean-spirited (satirical, not cruel)
- ❌ Not random/nonsensical

### Derek-isms to Include

- "ACTUALLY" (will be highlighted in yellow)
- "FACT:" (will be highlighted in red)
- Citations: "Author et al. (year)"
- Technical acronyms: ML, ROC-AUC, PDF
- Height references (Derek is tall, PI is short)
- Plenny Shake, Garmin, cycling metrics
- Marcus Aurelius, stoic philosophy
- SpongeBob episode references (with accuracy)
- Minecraft redstone or Factorio optimization

## 🐛 Bug Reports

Please include:
1. **Steps to reproduce** - Be specific
2. **Expected behavior** - What should happen
3. **Actual behavior** - What actually happens
4. **Your setup** - OS, Python version, terminal

Derek will analyze your bug report with his characteristic thoroughness and possibly question your methodology.

## 🔧 Code Contributions

### Code Style
- Follow PEP 8 (Derek insists)
- Add docstrings (Google style)
- Type hints where appropriate
- Keep functions focused and testable

### Testing
- Test your changes locally
- Try various phrasings and edge cases
- Check color rendering in different terminals
- Verify keyboard shortcuts work

### Pull Request Process

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
4. **Test thoroughly** (Derek is watching)
5. **Commit with clear messages**
6. **Push to your fork**
7. **Open a Pull Request**

Derek will review your PR with maximum scrutiny and minimal mercy. This is a feature, not a bug.

## 💡 Ideas We'd Love

- New response categories (with 10+ responses each)
- Additional ASCII faces (60 chars wide, please)
- Better keyword matching algorithms
- More SpongeBob episode references
- Additional stoic philosophy quotes
- Cycling-related pedantry
- New fake citations (keep them funny)

## 🚫 What We Won't Accept

- Mean-spirited content
- Discrimination or harassment
- Breaking changes without discussion
- Removing Derek's personality quirks
- Making Derek less pedantic (that's the point)
- Suggesting he's wrong (he'll never admit it)

## 📚 Resources

- **Matcher Algorithm:** See `derek_mcp/matcher.py` for keyword matching logic
- **Response Database:** `derek_mcp/data/responses.json` (1600+ lines of pedantry)
- **CLI Interface:** `derek_mcp/cli.py` for display logic and animations
- **Stats Script:** `keyword_stats.py` to analyze response coverage

## 🤝 Code of Conduct

Be excellent to each other. Derek may be pedantic, but we're not.

---

*"Your contribution has been noted. Though I would have structured it differently."* - Derek

**Thank you for contributing! 🤓**
