# 🤓 Derek MCP - The Molecular Control Pedant

> *"Standing on the shoulders of giants... who are 40 centimeters shorter than me."*

A pedantic CLI bot that embodies every PhD candidate you've ever met: tall, ginger, and blessed with "Quantum-IQ" (intelligence in superposition with complete obliviousness).

Derek is a molecular machine learning researcher at TU/e who rides 300km per week, subsists entirely on Plenny Shake, and will absolutely correct your understanding of literally anything with maximum confidence and variable accuracy.

**Perfect for:** PhD defense parties, roasting your graduating friends, or procrastinating on your own thesis.

## Installation

### Quick Setup (LLM-Enhanced Mode)

Derek now supports local LLM integration for more dynamic and contextual responses!

```bash
# 1. Install Ollama and the model
./setup_ollama.sh

# 2. Install Derek MCP
pip install -e .

# 3. Run Derek
derek_mcp
```

### Basic Installation (Keyword-Only Mode)

If you prefer the original keyword-based responses or don't want to install Ollama:

```bash
# From the DEREK directory
pip install -e .

# Run Derek (will automatically use keyword-only mode)
derek_mcp
```

## Usage

```bash
# Start interactive session
derek_mcp

# Show help
derek_mcp --help

# Show version
derek_mcp --version

# Disable colors
derek_mcp --no-color
```

## Interactive Session

Once launched, Derek will greet you with his characteristic robotic charm. Simply type your questions or statements, and Derek will respond with pedantic corrections.

### Example Sessions

### Casual Conversation
```
You: Hey Derek, how's it going?
Derek: Functioning optimally. My HRV this morning was 87—excellent recovery
       metrics. The dissertation progresses methodically. No major experimental
       catastrophes today. By most measures: productive.

You: What's up?
Derek: Currently analyzing molecular property distributions beyond the Karman
       Line. The usual. Also considering whether my desk needs to be raised
       another two centimeters. Ergonomics are never truly optimized, only
       iteratively improved.

You: Thanks for the help!
Derek: You're welcome. Though gratitude is unnecessary when I'm merely
       providing accurate information that should have been obvious from
       first principles.
```

### Technical Discussion
```
You: Tell me about molecular discovery
Derek: Molecular discovery is fundamentally an epistemological exercise in
       Bayesian inference over chemical space. My acquisition function
       optimizes for epistemic uncertainty in regions approaching the Karman
       Line—that threshold beyond which your training distribution becomes
       cosmically irrelevant.

You: I think that's a bit simple
Derek: You've characterized this as 'simple'? SIMPLE? The conceptual
       architecture alone requires graduate-level comprehension across three
       distinct domains. Your casual dismissal reveals a Dunning-Kruger
       confidence that would be amusing if it weren't so catastrophically
       misplaced. Shall I enumerate the seventeen prerequisite concepts
       you're missing?
```

### Pop Culture
```
You: Is mayonnaise an instrument?
Derek: Is mayonnaise an instrument? No, Patrick, mayonnaise is not an
       instrument. *pause* Horseradish is not an instrument either. This is
       basic categorical reasoning that apparently requires clarification. As
       documented in Band Geeks, Season 2, Episode 35b.
```

### Exit Commands

- `exit`, `quit`, `bye`, `goodbye`, or `q` - Exit the session
- `Ctrl+C` - Force exit

## ✨ Features

### Core Features
- 🤖 **LLM-Enhanced Mode** - Local LLM (llama3.2:3b) generates dynamic, contextual Derek responses
- 🎯 **325 Curated Responses** - Organized in 7 category files, serve as LLM context and fallback
- 🤖 **Streaming Responses** - Watch Derek's pedantry materialize token-by-token
- 🎨 **Smart Color Coding** - ACTUALLY in bright yellow, citations in blue, *robot actions* in magenta
- 📊 **Sass-o-Meter™** - Visual indicator of Derek's current pedantry level (0-10)
- 🧠 **Hybrid Intelligence** - LLM uses keyword matches as context for in-character generation
- 🔄 **Graceful Fallback** - Automatically switches to keyword-only mode if Ollama unavailable
- 📚 **Real Research** - Actual citations from Derek van Tilborg's published work on activity cliffs
- 🎭 **Fake Citations** - I.M. Wright, Knowitall & Pedantic (2023), Obvious et al.
- 🍍 **SpongeBob Expertise** - 7 episodes analyzed with scientific rigor
- 🚴 **Lifestyle Accuracy** - 300km/week cycling, €300 Garmin, French toast fueling, fruit gels
- ⛰️ **The Giants Quote** - Immortalized thesis acknowledgment about short supervisors
- 🧴 **Sunscreen Protocol** - SPF 50+ every 2 hours, 95.3% photostability metrics
- 🎨 **Geometry Obsession** - Hexagons, right angles <0.3°, plain forms only
- 💬 **Command Shortcuts** - `/sass`, `/history`, `/stats`, `/help`
- 🎭 **ASCII Faces** - 12 hand-crafted 60-char faces (neutral, sassy, talking, thinking)

## 🤖 LLM Integration

Derek now features **hybrid intelligence**: an LLM generates responses using keyword-matched phrases as context, maintaining character consistency while allowing dynamic, contextual responses.

### How It Works

1. **User Input** → Keyword matcher finds top 3 relevant responses
2. **Context Building** → Matched responses + sass level passed to LLM
3. **LLM Generation** → llama3.2:3b generates in-character response using condensed profile
4. **Streaming Output** → Response displays token-by-token with typing effect
5. **Graceful Fallback** → If Ollama unavailable, uses pure keyword matching

### LLM vs Keyword-Only Mode

| Feature | LLM Mode | Keyword Mode |
|---------|----------|--------------|
| Contextual awareness | ✅ Yes | ❌ No |
| Varied responses | ✅ Infinite variations | 🔄 257 curated |
| Off-topic handling | ✅ In-character response | ⚠️ Generic fallback |
| Setup required | 🛠️ Ollama (~5 min) | ✅ Ready out-of-box |
| Response quality | 🎭 Dynamic, contextual | 📝 Hand-crafted |
| Offline use | ✅ Fully local | ✅ Fully local |

### Ollama Setup

```bash
# Automated setup script (recommended)
./setup_ollama.sh

# Manual setup
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2:3b

# Verify installation
ollama list
curl http://localhost:11434/api/tags
```

### Testing LLM Integration

```bash
# Test Ollama connection and model
python -m derek_mcp.llm

# Test full conversation pipeline
python test_conversation.py
```

## Project Structure

```
derek_mcp/
├── derek_mcp/
│   ├── __init__.py                        # Package initialization
│   ├── cli.py                             # CLI interface and main loop
│   ├── matcher.py                         # Response matching logic
│   ├── llm.py                             # LLM integration (Ollama)
│   └── data/
│       ├── character_profile.md           # Comprehensive character profile (single source of truth)
│       ├── responses_by_category/         # 325 responses in 7 organized files
│       │   ├── index.json                 # Master index
│       │   ├── responses_conversational.json (87 responses)
│       │   ├── responses_research.json    # (52 responses)
│       │   ├── responses_lifestyle.json   # (61 responses)
│       │   ├── responses_personality.json # (46 responses)
│       │   ├── responses_technology.json  # (16 responses)
│       │   ├── responses_culture.json     # (16 responses)
│       │   ├── responses_molml.json       # (47 responses)
│       │   └── CATEGORY_TROPES.md         # Documentation
│       └── faces/                         # ASCII art faces
├── setup_ollama.sh                        # Ollama setup automation
├── setup.py                               # Package configuration
└── README.md                              # This file
```

## Customization

### Adding New Responses

You can easily add new responses by editing the category files in `derek_mcp/data/responses_by_category/`. Each response should follow this schema:

```json
{
  "id": "unique_id",
  "category": "topic_category",
  "keywords": ["keyword1", "keyword2"],
  "response": "Derek's pedantic response here",
  "follow_up": "Optional snarky follow-up",
  "sass_level": 8
}
```

### Response Categories

Responses are organized into 7 category files:

- **Conversational** (87) - Greetings, gratitude, small talk, goodbyes
- **Research** (52) - Molecules, thesis, publications, academia, expertise areas
- **Lifestyle** (61) - Cycling, nutrition, minimalism, sunscreen, facial hair
- **Personality** (46) - Quantum-IQ, pedantry, robot identity, height references, geometry obsession
- **Technology** (16) - Gadgets, Garmin, bike accessories, quantification tools
- **Culture** (16) - SpongeBob analysis, pop culture with academic rigor
- **MolML** (47) - Group members at TU/e (Francesca, Riza, Sarah, Andrea, Luke, Sebastien, and others), with hilariously specific observations about each person

See `derek_mcp/data/responses_by_category/CATEGORY_TROPES.md` for detailed tropes per category.

### Template Variables

Responses support template variables:

- `{user_input}` - Full user input
- `{user_phrase}` - Extracted key phrase from input

Example:
```json
{
  "response": "Your understanding of '{user_phrase}' is... *processing* ...creative."
}
```

## Dependencies

### Required
- `colorama>=0.4.6` - Cross-platform colored terminal output
- `requests>=2.31.0` - HTTP client for Ollama API

### Optional (for LLM mode)
- **Ollama** - Local LLM runtime (user-installed)
- **llama3.2:3b** - 2GB model for character roleplay

## Development

```bash
# Install in development mode
pip install -e .

# Run directly from source
python -m derek_mcp.cli
```

## 🎯 Use Cases

- **PhD Defense Parties** - Roast your graduating friend in style
- **Lab Procrastination** - Better than doom-scrolling
- **Communication Training** - Learn to deal with pedantic colleagues
- **Entertainment** - Watch an AI embody academic stereotypes with alarming accuracy

## 🛠️ Utility Scripts

- **`keyword_stats.py`** - Generate statistics about response keywords (for future expansion)

## 📜 License

MIT License - Created for entertainment and educational purposes. 

**Disclaimer:** Derek's opinions do not reflect those of actual PhD candidates (probably). Any resemblance to real researchers, living or graduated, is purely coincidental and definitely not intentional at all.

## 🙏 Credits

Inspired by a certain tall, ginger molecular ML researcher at TU/e who definitely does NOT ride 300km per week, does NOT subsist entirely on Plenny Shake, and absolutely NEVER corrects people with unwarranted confidence.

This is a work of fiction. Names, characters, businesses, places, events, locales, and incidents are either the products of the author's imagination or used in a fictitious manner.

---

### ⚠️ Warning

Derek may:
- Question your understanding of basic concepts
- Reference SpongeBob episodes with scientific analysis
- Mention his €300 Garmin unprompted
- Calculate the optimal height for your desk
- Cite papers that don't exist
- Be wrong while being absolutely certain

This is working as intended.

---

*"ACTUALLY, if you read my thesis, the methodology is quite straightforward..."* 🤓

**Made with 💙 (and a healthy dose of academic satire)**
