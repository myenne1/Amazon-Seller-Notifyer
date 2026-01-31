# 📦 Amazon Order Notification Bot — Step-by-Step Beginner’s Setup

**Audience:** Amazon sellers with little to no technical experience.  
No coding knowledge is required.

---

## 📝 What This Tool Does

This tool automatically checks your Amazon Seller Central account every few minutes and sends you a **Telegram notification** when you receive a new order.

**How it works:**
1. **Amazon SP-API** → Gets your latest orders.
2. **Supabase** → Stores order records so you don’t get duplicate alerts.
3. **Telegram Bot** → Sends you a notification instantly.
4. Can run:
   - On your computer (manual run), or
   - On Vercel (free hosting — runs automatically)

---

## 🔑 Keys & Accounts You’ll Need

You’ll need to sign up for or configure the following services:

1. **Supabase account** — Free online database
2. **Telegram Bot** — Sends messages to you
3. **Amazon SP-API credentials** — Allows reading your Amazon orders
4. **AWS IAM keys** — Required for SP-API authentication

You will place all these keys in a `.env` file later.

---

## 📂 Setting Up Supabase

### 1. Create a Supabase Project
1. Go to [https://supabase.com](https://supabase.com) → **Sign Up** (Google login works fine).
2. Click **New Project**.
3. Choose:
   - **Name:** Anything you like
   - **Password:** For your database
   - **Plan:** Free tier is fine

---

### 2. Create the `orders` Table
1. In your Supabase dashboard, click **Table Editor** → **New Table**.
2. Set the **table name** to: `orders`
3. Add these columns:

| Name          | Type      | Notes                         |
|---------------|-----------|-------------------------------|
| order_id      | text      | Primary Key                   |
| units_sold    | text      |                               |
| amount        | text      |                               |
| purchase_date | text      |                               |
| is_business   | boolean   |                               |
| status        | text      |                               |
| created_at    | timestamp | Default: `now()`              |

4. Mark `order_id` as the **Primary Key**.
5. Save the table.

---

### 3. Get Your Supabase Keys
1. In Supabase, go to **Project Settings** → **API**.
2. Copy these values:
   - **Project URL** → `SUPABASE_URL`
   - **anon key** → `SUPABASE_KEY`
   - **service_role key** → `SUPABASE_SERVICE_ROLE_KEY`

---

## 💬 Creating a Telegram Bot

### 1. Create Your Bot
1. Open Telegram and search for **BotFather**.
2. Type:
   ```
   /newbot
   ```
3. Follow the prompts to:
   - Give your bot a **name**
   - Choose a **username** (must end in `_bot`)
4. BotFather will give you a **Bot Token** — save this as `TELEGRAM_BOT_TOKEN`.

---

### 2. Get Your Telegram Chat ID
1. Add your bot to a Telegram group **OR** start a private chat with it.
2. Send any message to the bot.
3. Open this URL in your browser, replacing `<YOUR_BOT_TOKEN>` with your bot token:
   ```
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   ```
4. Look for `"chat":{"id":123456789}` in the response — this number is your `TELEGRAM_CHAT_ID`.

---

## 🛒 Getting Amazon SP-API & AWS Keys

### 1. Register as a Developer
1. Go to Seller Central → **Apps & Services** → **Manage Your Apps**.
2. Click **Register as a Developer** and fill out the form.

---

### 2. Create an SP-API App
1. In the **Developer Console**, click **Add New App**.
2. Amazon will give you:
   - **LWA Client ID** → `LWA_ID`
   - **LWA Client Secret** → `LWA_SECRET`

---

### 3. Get Your Refresh Token
1. In Seller Central, authorize your new app for your account.
2. Amazon will return a `refresh_token` → save as `REFRESH_TOKEN`.

---

### 4. Create IAM Role & Keys in AWS
1. Log into AWS Console → **IAM**.
2. Create a **Role** for SP-API with the correct permissions.
3. Create an **IAM User** with programmatic access.
4. Save:
   - **IAM_ROLE_ARN**
   - **IAM_USER_ACCESS_KEY_ID**
   - **IAM_USER_SECRET`

---

## 🖥 Running the Bot Locally

### 1. Install Python
Download and install Python from:  
[https://www.python.org/downloads/](https://www.python.org/downloads/)

---

### 2. Download the Project
- Either download the ZIP file from GitHub or use:
```bash
git clone https://github.com/<your-repo>.git
```

---

### 3. Create `.env`
1. Copy `.env.template` → rename it to `.env`.
2. Paste all your collected keys into `.env` in the correct spots.

---

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

### 5. Run the Bot
```bash
python amz.py
```
If your keys are correct, you’ll get a “Test Notification” in Telegram.

---

## 🌐 Deploying to Vercel (Free Hosting)

### 1. Sign Up for Vercel
Go to [https://vercel.com](https://vercel.com) → **Sign Up**.

---

### 2. Import Your Project
- Connect your GitHub (or upload manually).
- Select the repository for this bot.

---

### 3. Set Environment Variables
In Vercel:
1. Go to **Settings** → **Environment Variables**.
2. Add each key from `.env` exactly as-is.

---

### 4. Deploy
- Click **Deploy**.
- Your bot is now hosted online and will run automatically.

---

## 📌 Final Notes
- **You keep all your keys** — they are never sent to anyone else.
- Amazon SP-API approval may take up to 24 hours.
- If you make a mistake in a key, you can update `.env` or the Vercel environment variables.
