# Insurance Claims Triage - DeepAgent Demo

> **A clean, focused demonstration of LangChain's `create_deep_agent`**

This demo showcases three powerful capabilities that make agents production-ready:

1. ✅ **Explicit Planning** - Uses `write_todos` for transparent workflow
2. 📁 **Filesystem Storage** - Handles large files efficiently
3. 🤖 **Subagent Delegation** - Parallel specialized processing

---

## 🚀 Quick Start

```bash
# Setup
cp .env.example .env              # Add your OPENAI_API_KEY
uv pip install -e .
python test_setup.py              # Validate installation

# Run - Choose your mode
python main.py                    # Automated demo
python main.py interactive        # Interactive mode
python ambient.py                 # Ambient mode (continuous processing)
```

**Expected output**: The agent will plan, store files, delegate to 3 subagents in parallel, and make a triage decision.

---

## 📚 Full Documentation

**👉 See [INDEX.md](INDEX.md) for complete navigation and learning path**

Quick links:
- **[QUICK_START.md](QUICK_START.md)** - Detailed setup and run instructions
- **[FEATURES.md](FEATURES.md)** - The three key capabilities explained
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design and code organization
- **[DEMO.md](DEMO.md)** - What to watch for when running

---

## 💡 What Makes This Special

### Planning-First Workflow
```
Agent creates visible plan:
☐ Retrieve claim information
☐ Store attachments
☐ Delegate to specialists
☐ Synthesize & decide
```

### Filesystem Storage
```bash
# Files stored on disk, not in messages:
claim_data/CLM-2024-001/
├── damage_front.jpg
├── police_report.pdf
└── repair_estimate.pdf
```

### Parallel Subagents
```
Main Agent (GPT-4)
├─→ damage-assessor  → Cost estimate
├─→ fraud-detector   → Risk score  
└─→ policy-verifier  → Coverage check
```

---

## 📖 Example: Processing a Claim

```python
# User request
"Process claim CLM-2024-001"

# Agent workflow
1. Plans with write_todos
2. Writes photos/docs to claim_data/
3. Spawns 3 subagents in parallel
4. Synthesizes → "AUTO-APPROVE"
```

**Try it**: `python main.py`

---

## 🎯 Why This Pattern?

Perfect for:
- Document processing with large attachments
- Multi-stage analysis requiring specialists
- Transparent AI needing visible reasoning
- Production systems handling real files

---

## 🏗️ Project Structure

```
insurance_claims_triage/
├── agent.py              # DeepAgent config (<100 lines!)
├── tools.py              # File I/O and claim tools
├── subagents/            # Specialized agents
│   ├── damage_assessor.py
│   ├── fraud_detector.py
│   └── policy_verifier.py
├── main.py               # Entry point
└── sample_claims/        # Test data (3 claims)
```

**Read the code**: Start with `agent.py` - it's surprisingly simple!

---

**Next**: See [INDEX.md](INDEX.md) for full documentation and learning path.
rt ambient processor (polls every 5s)
python ambient.py
```

The agent monitors `claims_queue/` and automatically processes any claims that appear. Perfect for production deployments!

See **[AMBIENT_MODE.md](AMBIENT_MODE.md)** for details.

---

**Next**: See [INDEX.md](INDEX.md) for full documentation and learning path.
