# Amazon Notification Tool

An automated notification system that monitors Amazon Seller Central orders and sends real-time Telegram notifications when new orders are received or cancelled.

## Features

- **Real-time Order Monitoring**: Polls Amazon SP-API for new orders within a configurable time window
- **Telegram Notifications**: Sends instant notifications to a specified Telegram chat when new orders are detected
- **Business Order Detection**: Special notifications for business orders
- **Order Cancellation Tracking**: Monitors and notifies when orders are cancelled
- **Duplicate Prevention**: Uses Supabase database to prevent duplicate notifications
- **Flexible AWS Authentication**: Supports both IAM user credentials and STS temporary credentials
- **REST API**: Includes a simple Flask API endpoint for manual polling

## Architecture

The application consists of several key modules:

- **`amz.py`** - Amazon SP-API integration and order processing logic
- **`messager.py`** - Telegram bot functionality for sending notifications
- **`supa.py`** - Supabase database operations for order tracking
- **`config.py`** - Configuration management using Pydantic settings
- **`api/index.py`** - Flask REST API for manual order polling

## Prerequisites

- Python 3.8+
- Amazon Seller Central account with SP-API access
- Supabase account and database
- Telegram bot token and chat ID
- AWS credentials (IAM user or STS temporary credentials)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Amazon-Notification-Tool
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with the required configuration (see Configuration section).

## Configuration

Create a `.env` file in the root directory with the following variables:

### Supabase Configuration
```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
```

### Telegram Configuration
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
TELEGRAM_BOT_USERNAME=your_telegram_bot_username
```

### Amazon SP-API Configuration
```env
LWA_ID=your_lwa_app_id
LWA_SECRET=your_lwa_client_secret
REFRESH_TOKEN=your_refresh_token
MARKETPLACE_ID=your_marketplace_id
REGION=your_region  # optional: "na", "eu", "fe"
```

### AWS Credentials (Choose One Option)

**Option A: IAM User + Role Assumption (Recommended)**
```env
IAM_ROLE_ARN=arn:aws:iam::account:role/YourRole
IAM_USER_ACCESS_KEY_ID=your_iam_access_key
IAM_USER_SECRET=your_iam_secret_key
```

**Option B: STS Temporary Credentials**
```env
STS_ACCESS_KEY_ID=your_sts_access_key
STS_SECRET_ACCESS_KEY=your_sts_secret_key
STS_SESSION_TOKEN=your_sts_session_token
```

### Application Configuration
```env
POLL_WINDOW_MINUTES=5  # How often to check for new orders (in minutes)
```

## Database Setup

The application requires a Supabase database with an `orders` table. Create a table with the following schema:

```sql
CREATE TABLE orders (
  order_id TEXT PRIMARY KEY,
  units_sold INTEGER,
  amount DECIMAL,
  purchase_date TEXT,
  is_business BOOLEAN,
  status TEXT DEFAULT 'New',
  created_at TIMESTAMP DEFAULT NOW()
);
```

## Usage

### Direct Execution
Run the order monitoring script directly:
```bash
python amz.py
```

### API Endpoint
Start the Flask API server:
```bash
python api/index.py
```

Then trigger order polling via HTTP:
```bash
curl http://localhost:5000/notifyer
```

### Testing
Test the Amazon SP-API connection:
```python
from amz import test_list_orders
test_list_orders()
```

## How It Works

1. **Order Polling**: The system queries Amazon SP-API for orders created within the specified time window
2. **Duplicate Check**: Each order is checked against the Supabase database to prevent duplicate notifications
3. **Order Processing**: New orders are stored in the database and trigger Telegram notifications
4. **Cancellation Monitoring**: The system detects when previously processed orders are cancelled and sends notifications
5. **Business Order Detection**: Special handling and notifications for business orders

## Notification Format

- **New Order**: `[💸 Cha-Ching!] X unit(s) sold`
- **Business Order**: `[💸 Cha-Ching!] X unit(s) sold Business Order!`
- **Cancelled Order**: `Order was canceled Order ID: XXXXX`

## Dependencies

- `supabase` - Database operations
- `fastapi` - Web framework (for potential future expansion)
- `uvicorn` - ASGI server
- `requests` - HTTP requests for Telegram API
- `python-amazon-sp-api` - Amazon Seller Partner API client

## Security Notes

- Store all sensitive credentials in the `.env` file
- Never commit the `.env` file to version control
- Use Supabase service role key for database operations
- Consider using AWS IAM roles instead of long-term access keys when possible

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is provided as-is for educational and personal use.