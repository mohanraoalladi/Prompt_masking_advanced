🔐 Privacy‑Preserving LLM Pipeline
Secure Prompt → PII Masking → LLM → Unmasking → Response
Built with Presidio, custom recognizers, Google Gemini, and a Streamlit UI

This project implements a fully privacy‑preserving LLM orchestration pipeline. It ensures that no raw PII ever reaches the LLM, thanks to a masking layer powered by Microsoft Presidio and custom dictionary recognizers.
A Streamlit UI provides a transparent, interactive chat experience with visibility into every stage of the pipeline.

📁 Project Structure
Code
.
├── agents/                 # Orchestration logic (mask → LLM → unmask)
├── config/                 # YAML config (API keys, model, PII toggles)
│   └── config.yaml
├── recognizers/            # Custom Presidio recognizers
├── ui/                     # Streamlit UI components
├── README.md
├── requirements.txt
└── sample_prompts.json
This structure cleanly separates concerns:

agents handles the pipeline logic

config centralizes runtime settings

recognizers extends PII detection

ui provides the interactive interface

⚙️ Configuration (config/config.yaml)
Your configuration file controls the entire system — model selection, API keys, and which PII categories are masked.

yaml
GEMINI_API_KEY: "YOUR_KEY_HERE123"
MODEL_NAME: "gemini-1.5-pro"

# Toggle LLM usage (useful for debugging without burning tokens)
USE_LLM: false

# Enable/disable PII categories for masking
PII_CATEGORIES_ENABLED:
  PERSON: true
  EMAIL_ADDRESS: true
  PHONE_NUMBER: true
  CREDIT_CARD: true
  IP_ADDRESS: true
  LOCATION: true
  CLIENT_ID: true
  ACCOUNT_REFERENCE: true
  ORGANIZATION: true
  DATE_TIME: false
  DOMAIN_NAME: false
Why this config works well
Centralized, human‑readable settings

Easy to extend with new PII categories

Supports turning the LLM off for local debugging

Safe to commit (as long as API keys are injected via env vars in production)

🚀 Features
🔒 Privacy‑Preserving LLM Flow
Presidio‑based PII detection

Custom dictionary recognizers for domain‑specific entities

Automatic masking before sending text to Gemini

LLM inference on masked text only

Deterministic unmasking of the final response

🖥️ Streamlit UI
Chat interface with history

Masked vs. unmasked prompt views

LLM response view

Final unmasked output

Toggle switches for PII categories (mirroring config.yaml)

🧱 Architecture Overview
Code
User Prompt
    ↓
Presidio Analyzer (built‑in + custom recognizers)
    ↓
Masking Layer (tokenized placeholders)
    ↓
Google Gemini LLM (masked text only)
    ↓
Unmasking Layer (restores original PII)
    ↓
Final Response
This ensures compliant, privacy‑preserving AI interactions.

📦 Installation
1. Clone the repository
bash
git clone <your-repo-url>
cd <your-project-folder>
2. Create a virtual environment
bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
3. Install dependencies
bash
pip install -r requirements.txt
4. Configure environment variables
Create a .env file:

Code
GEMINI_API_KEY=your_key_here
The YAML config will read this automatically if your loader supports env overrides.

▶️ Running the App
bash
streamlit run ui/app.py
The UI will open at:

Code
http://localhost:8501
🧩 Custom Recognizers
Place your custom Presidio recognizers in:

Code
recognizers/
These may include:

Dictionary‑based recognizers

Regex‑based recognizers

Domain‑specific entity detectors

They are automatically loaded into the analyzer at startup.

🔍 Example Workflow
Input:

“Email John Doe at john.doe@company.com about the contract.”

Masked:

“Email PERSON_1 at EMAIL_1 about the contract.”

LLM Output (masked):

“Sure, I’ll draft an email to PERSON_1.”

Final Unmasked Output:

“Sure, I’ll draft an email to John Doe.”

🧪 Testing
Run tests with:

bash
pytest
Tests cover:

PII detection

Masking/unmasking consistency

Recognizer accuracy

LLM pipeline integration

🗺️ Roadmap
Add support for multiple LLM providers

Add audit logging for compliance

Add batch document processing

Add UI‑based config editing

🤝 Contributing
Contributions are welcome.
If you add new recognizers or pipeline components, please include tests and documentation.

📜 License
MIT License (or your preferred license)
