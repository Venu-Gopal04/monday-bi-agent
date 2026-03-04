from groq import Groq
import json
import os
from dotenv import load_dotenv
from monday_client import get_board_summary

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def answer_question(user_question: str) -> dict:
    print(f"\n[AGENT] Question received: {user_question}")
    
    data = get_board_summary()
    
    deals_sample = data["deals"][:100]
    wo_sample = data["work_orders"][:100]

    prompt = f"""You are a Business Intelligence agent for Skylark Drones.
Answer founder-level questions using this live Monday.com data.

DEALS ({data['deal_count']} total):
{json.dumps(deals_sample, indent=2, default=str)[:4000]}

WORK ORDERS ({data['work_order_count']} total):
{json.dumps(wo_sample, indent=2, default=str)[:4000]}

Question: {user_question}

Give a direct answer with key data points."""

    print(f"[AGENT] Sending to Groq for analysis...")
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )

    print(f"[AGENT] Response received!")

    return {
        "answer": response.choices[0].message.content,
        "tool_calls": [
            {
                "action": "fetch_monday_boards",
                "boards": ["Deal Funnel", "Work Orders"],
                "records_fetched": {
                    "deals": data["deal_count"],
                    "work_orders": data["work_order_count"]
                }
            }
        ],
        "data_freshness": "Live - fetched at query time"
    }