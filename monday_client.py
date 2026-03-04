import requests
import os
from dotenv import load_dotenv

load_dotenv()

MONDAY_API_KEY = os.getenv("MONDAY_API_KEY")
WORK_ORDER_BOARD_ID = os.getenv("WORK_ORDER_BOARD_ID")
DEAL_BOARD_ID = os.getenv("DEAL_BOARD_ID")

HEADERS = {
    "Authorization": MONDAY_API_KEY,
    "Content-Type": "application/json",
    "API-Version": "2024-01"
}

def query_monday(graphql_query):
    response = requests.post(
        "https://api.monday.com/v2",
        json={"query": graphql_query},
        headers=HEADERS
    )
    return response.json()

def get_all_deals():
    query = f"""
    {{
        boards(ids: [{DEAL_BOARD_ID}]) {{
            items_page(limit: 500) {{
                items {{
                    name
                    column_values {{
                        id
                        text
                    }}
                }}
            }}
        }}
    }}
    """
    result = query_monday(query)
    try:
        return result["data"]["boards"][0]["items_page"]["items"]
    except:
        return []

def get_all_work_orders():
    query = f"""
    {{
        boards(ids: [{WORK_ORDER_BOARD_ID}]) {{
            items_page(limit: 500) {{
                items {{
                    name
                    column_values {{
                        id
                        text
                    }}
                }}
            }}
        }}
    }}
    """
    result = query_monday(query)
    try:
        return result["data"]["boards"][0]["items_page"]["items"]
    except:
        return []

def get_board_summary():
    print("[TOOL CALL] Fetching deals from Monday.com...")
    deals = get_all_deals()
    print(f"[TOOL CALL] Fetched {len(deals)} deals")
    
    print("[TOOL CALL] Fetching work orders from Monday.com...")
    work_orders = get_all_work_orders()
    print(f"[TOOL CALL] Fetched {len(work_orders)} work orders")

    def parse_item(item):
        d = {"name": item["name"]}
        for col in item["column_values"]:
            if col["text"]:
                d[col["id"]] = col["text"]
        return d

    deals_clean = [parse_item(i) for i in deals]
    work_orders_clean = [parse_item(i) for i in work_orders]

    return {
        "deals": deals_clean,
        "work_orders": work_orders_clean,
        "deal_count": len(deals_clean),
        "work_order_count": len(work_orders_clean)
    }