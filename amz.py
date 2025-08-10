from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any
from config import settings

from sp_api.api import Orders
from sp_api.base import SellingApiException
from config import settings
from supa import order_exists, insert_order, get_order_status
from messager import send_telegram_message

POLL_WINDOW_MINUTES = settings.POLL_WINDOW_MINUTES

def _orders_client() -> Orders:
    # Prefer STS if present; else fall back to IAM user. Role ARN is optional.
    aws_access_key = settings.STS_ACCESS_KEY_ID or settings.IAM_USER_ACCESS_KEY_ID
    aws_secret_key = settings.STS_SECRET_ACCESS_KEY or settings.IAM_USER_SECRET
    aws_session_token = settings.STS_SESSION_TOKEN  # may be None

    credentials = {
        "lwa_app_id": settings.LWA_ID,
        "lwa_client_secret": settings.LWA_SECRET,
        "refresh_token": settings.REFRESH_TOKEN,
        "aws_access_key": aws_access_key,
        "aws_secret_key": aws_secret_key,
        "aws_session_token": aws_session_token,
        "role_arn": settings.IAM_ROLE_ARN,
    }

    # marketplace_id is enough; region/host are optional
    client = Orders(credentials=credentials)
    return client

def fetch_recent_orders(minutes: int = POLL_WINDOW_MINUTES) -> List[Dict[str, Any]]:
    client = _orders_client()
    created_after_dt = datetime.now(timezone.utc) - timedelta(minutes=minutes)
    created_after = created_after_dt.replace(microsecond=0).isoformat().replace("+00:00", "Z")

    try:
        resp = client.get_orders(
            MarketplaceIds=[settings.MARKETPLACE_ID],
            CreatedAfter=created_after,
        )
    except SellingApiException as e:
        print(f"SP-API get_orders error: {e}")
        return []

    orders = resp.payload.get("Orders", []) or []
    results: List[Dict[str, Any]] = []
    print(f"Num fetched orders: {len(orders)}")
    
    for o in orders:
        
        # Order Id
        order_id = o.get("AmazonOrderId")
        
        # Order total
        amount = None
        order_total = o.get("OrderTotal") or {}
        
        if order_total.get("Amount") is not None:
            try:
                amount = float(order_total["Amount"])
            except:
                amount = None
        
        units_sold = int(o.get("NumberOfItemsUnshipped", 0) or 0)
        
        is_business = bool(o.get("IsBusinessOrder") or False)
        
        purchase_date = str(o.get("PurchaseDate") or "")
        
        canceled = (o.get("OrderStatus") == "Canceled")

        results.append({
            "order_id": order_id,
            "units": units_sold,
            "amount": float(amount or 0.0),
            "purchase_date": purchase_date,
            "isBusiness": is_business,
            "canceled": canceled,
        })

    return results

def process_order(order_id, units_sold, amount, purchase_date, is_business, cancelled):
    if cancelled:
        prev = get_order_status(order_id)
        if prev != "Canceled":
            send_telegram_message(f"Order was canceled\nOrder ID: {order_id}")
            insert_order(order_id, units_sold, amount, purchase_date, is_business, status="Canceled")
            return
        
    if order_exists(order_id):
        print(f"Skipping duplicate order: {order_id}")
        return
    insert_order(order_id, units_sold, amount, purchase_date, is_business)
    
    if is_business:
        send_telegram_message(f"[💸 Cha-Ching!]\n{units_sold} unit(s) sold\nBusiness Order!")
    else:
        send_telegram_message(f"[💸 Cha-Ching!]\n{units_sold} unit(s) sold")
        
    print(f"New order logged + notified: {order_id}")

def poll_and_notify() -> int:
    orders = fetch_recent_orders(minutes=POLL_WINDOW_MINUTES)
    processed = 0
    
    if len(orders) == 0:
        print("No orders found")
        
    for o in orders:
        # Use your existing dedupe + notify
        process_order(
            o["order_id"],
            o["units"],
            f"{o['amount']:.2f}",
            o["purchase_date"],
            o["isBusiness"],
            o["canceled"]
        )
        processed += 1
    return processed

def test_list_orders():
    client = _orders_client()
    created_after = (datetime.now(timezone.utc) - timedelta(days=20)) \
                      .replace(microsecond=0).isoformat().replace("+00:00","Z")
    print("DEBUG CreatedAfter:", created_after)

    try:
        resp = client.get_orders(
            MarketplaceIds=[settings.MARKETPLACE_ID],
            CreatedAfter=created_after,
            MaxResultsPerPage=100,
        )
    except SellingApiException as e:
        print("SP-API get_orders error:", e)
        return

    payload = resp.payload or {}
    orders = payload.get("Orders", []) or []
    print(f"Found {len(orders)} orders in last 7 days")

    # show a few
    for o in orders[:]:
        print({
            "AmazonOrderId": o.get("AmazonOrderId"),
            "PurchaseDate": o.get("PurchaseDate"),
            "OrderStatus": o.get("OrderStatus"),
            "SalesChannel": o.get("SalesChannel"),
            "OrderTotal": o.get("OrderTotal"),
            "IsBusinessOrder": o.get("IsBusinessOrder"),
            "NumberOfItemsUnshipped": o.get("NumberOfItemsUnshipped")
        })

    # if paginated
    while payload.get("NextToken"):
        try:
            resp = client.get_orders(NextToken=payload["NextToken"])
        except SellingApiException as e:
            print("Paging error:", e)
            break
        payload = resp.payload or {}
        more = payload.get("Orders", []) or []
        print(f"+{len(more)} more")
        orders.extend(more)

    print("TOTAL orders:", len(orders))