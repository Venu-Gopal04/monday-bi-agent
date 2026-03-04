Skylark Drones — BI Agent
A conversational Business Intelligence agent built for Skylark Drones that lets founders ask natural-language questions about their deal pipeline and work orders — and get instant, data-backed answers.
Powered by Monday.com (live data) + Groq LLaMA 3.1 (AI reasoning) + FastAPI (backend).
🔗 Live Demo: huggingface.co/spaces/Venugopal04/monday-bi-agent

What it does
Instead of manually digging through Monday.com boards, you can just ask:

"How's our pipeline this quarter?"
"What's our total deal value?"
"Which work orders are not started?"
"Who is our top performing owner?"
"Show revenue by sector"

The agent fetches live data from Monday.com on every query, sends it to an LLM for analysis, and returns a clear, structured answer — along with a visible tool trace showing exactly what data was fetched.

Tech Stack:

   Layer         Technology                         Why

1) Data          Monday.com GraphQL API             Live data, no ETL, real-time
2) AI            Groq (LLaMA 3.1 8B Instant)        Free tier, fast, great at structured data
3) Backend       FastAPI + Python                   Lightweight, easy to deploy
4) Frontend      HTML / CSS / JS                    No build step, works everywhere
5) Hosting       Hugging Face Spaces (Docker)       Free, always-on, no card needed

Project Structure
monday-bi-agent/
├── agent.py              # AI orchestration — fetches data, builds prompt, calls Groq
├── main.py               # FastAPI server — handles /ask endpoint + serves frontend
├── monday_client.py      # Monday.com GraphQL client — fetches deals and work orders
├── frontend/
│   └── index.html        # Chat UI — single file, no framework
├── Dockerfile            # For Hugging Face Spaces deployment
├── requirements.txt
└── .env                  # API keys (not committed)

How It Works

User asks a question in the chat UI
Frontend sends a POST request to /ask
Backend calls Monday.com GraphQL API and fetches up to 500 records from both boards (Deal Funnel + Work Orders)
First 100 records from each board are passed as context to the LLM
Groq (LLaMA 3.1) analyzes the data and returns a structured answer
Frontend displays the answer + tool trace showing live data fetch details


Running Locally
1. Clone the repo
bashgit clone https://github.com/Venu-Gopal04/monday-bi-agent.git
cd monday-bi-agent
2. Create virtual environment
bashpython -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
3. Install dependencies
bashpip install -r requirements.txt
4. Set up environment variables
Create a .env file in the root directory:
MONDAY_API_KEY=your_monday_api_token
WORK_ORDER_BOARD_ID=your_work_order_board_id
DEAL_BOARD_ID=your_deal_funnel_board_id
GROQ_API_KEY=your_groq_api_key
5. Start the server
bashuvicorn main:app --reload
6. Open the app
Visit http://localhost:8000 in your browser.

Getting API Keys

Monday.com API Key: Go to your Monday.com account → Profile → Administration → Connections → API → Generate token
Groq API Key: Sign up free at console.groq.com → API Keys → Create key


Data Notes
The Monday.com boards used in this project contain anonymized data:

Company names are replaced with placeholder codes
Monetary values are masked but preserve relative proportions
Owner names appear as OWNER_001, OWNER_002, etc.

The agent handles this gracefully and makes clear when values are masked in its responses.

Deployment
The app is deployed on Hugging Face Spaces using Docker. The Dockerfile exposes port 7860 (required by HF Spaces) and serves both the FastAPI backend and the static frontend from a single container.
To deploy your own version:

Fork this repo
Create a new Hugging Face Space (Docker SDK)
Push this repo to the Space
Add your API keys as Secrets in the Space settings


Limitations

No conversation memory — each question is independent
Large boards (500+ items) are sampled to 100 records to stay within LLM context limits
Masked data limits the depth of financial analysis
Groq free tier has rate limits under heavy usage


Built for
Skylark Drones AI Engineer Technical Assignment — March 2026