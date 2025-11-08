# 🤓 Derek MCP - The Molecular Control Pedant

> *"Standing on the shoulders of giants... who are 40 centimeters shorter than me."*

A pedantic CLI bot that embodies every PhD candidate you've ever met: tall, ginger, and blessed with "Quantum-IQ" (intelligence in superposition with complete obliviousness).

Derek is a molecular machine learning researcher at TU/e who rides 300km per week, subsists entirely on Plenny Shake, and will absolutely correct your understanding of literally anything with maximum confidence and variable accuracy.

**Perfect for:** PhD defense parties, roasting your graduating friends, or procrastinating on your own thesis.

## Installation

```bash
# From the DEREK directory
pip install -e .
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

- 🎯 **220+ Responses** - From casual chat to nuclear-grade pedantry
- 🤖 **Typing Animation** - Watch Derek's confidence materialize character-by-character
- 🎨 **Smart Color Coding** - ACTUALLY in bright yellow, citations in blue, *robot actions* in magenta
- 📊 **Sass-o-Meter™** - Visual indicator of Derek's current pedantry level (0-10)
- 🧠 **Intelligent Matching** - Synonyms, stemming, and phrase detection for natural conversation
- 📚 **Real Research** - Actual citations from Derek van Tilborg's published work on activity cliffs
- 🎭 **Fake Citations** - I.M. Wright, Knowitall & Pedantic (2023), Obvious et al.
- 🍍 **SpongeBob Expertise** - 7 episodes analyzed with scientific rigor
- 🚴 **Lifestyle Accuracy** - 300km/week cycling, €300 Garmin, Plenny Shake dependency
- ⛰️ **The Giants Quote** - Immortalized thesis acknowledgment about short supervisors
- 💬 **Command Shortcuts** - `/sass`, `/history`, `/stats`, `/help`
- 🎭 **ASCII Faces** - 12 hand-crafted 60-char faces (neutral, sassy, talking, thinking)

## Project Structure

```
derek_mcp/
├── derek_mcp/
│   ├── __init__.py           # Package initialization
│   ├── cli.py                # CLI interface and main loop
│   ├── matcher.py            # Response matching logic
│   └── data/
│       └── responses.json    # Response database
├── setup.py                  # Package configuration
├── requirements.txt          # Dependencies
└── README.md                 # This file
```

## Customization

### Adding New Responses

You can easily add new responses by editing `derek_mcp/data/responses.json`. Each response should follow this schema:

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

- `molecules` - Chemistry, molecular structures, bonds
- `agentic_ai` - AI agents, LLMs, neural networks
- `mcp` - Model Context Protocol, servers, tools
- `thesis` - Dissertation, research, academia
- `quantum_iq` - Paradoxes, superposition of smart/dumb
- `robot` - Robot personality, existence questions
- `pedantry` - Pure corrections and nitpicking
- `general_science` - Catch-all scientific topics
- `meta` - Questions about Derek himself

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

- `colorama>=0.4.6` - Cross-platform colored terminal output

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
