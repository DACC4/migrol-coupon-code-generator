# Migrol coupon-code generator
Automate the generation of migrol coupon codes using the API and send them to a telegram chat.

## Requirements
- `uv`

## Setup
1. Clone the repository
2. Run `uv sync` to install the dependencies
3. Create a `.env` file in the root directory and add the following variables
```env
CLIENT_SECRET=""
APP_INSTALLATION_ID=""
TELEGRAM_BOT_TOKEN=""
TELEGRAM_CHAT_ID=""
```
4. Run the app using `uv run main.py`