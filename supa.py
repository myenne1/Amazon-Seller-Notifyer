from csv import Error
from supabase import create_client, Client
from config import settings

SUPABASE_URL = settings.SUPABASE_URL
SUPABASE_SERVICE_ROLE_KEY = settings.SUPABASE_SERVICE_ROLE_KEY

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

def order_exists(order_id: str) -> bool:
    result = supabase.table("orders").select("order_id").eq("order_id", order_id).execute()
    return len(result.data) > 0

def insert_order(order_id: str, units_sold: int, amount: float, purchase_date: str, is_business: bool, status: str = "New"):
    supabase.table("orders").upsert(
        {
            "order_id": order_id,
            "units_sold": units_sold,
            "amount": amount,
            "purchase_date": purchase_date,
            "is_business": is_business,
            "status": status
        },
        on_conflict="order_id"
    ).execute()
    
def get_order_status(order_id: str) -> str | None:
    r = supabase.table("orders").select("status").eq("order_id", order_id).limit(1).execute()
    if r.data:
        return r.data[0].get("status")
    return None

def set_price(new_price):
    try:
        supabase.table("bot_settings").update({"price": new_price}).eq("id", 1).execute()
    except Exception as e:
        return Error("Unable to set price: ", e)
    
    
    
def get_price_setting() -> float | None:
    r = supabase.table("bot_settings").select("price").eq("id", 1).execute()
    return r.data[0].get('price')