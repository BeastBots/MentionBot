# Telegram Mention Bot

A Telegram bot to mention all group members or admins with additional settings and features. This bot is designed to be modular, scalable, and easy to deploy on platforms like Heroku and Koyeb.

---

## 🌟 Features

1. **Mention Commands**:
   - `/all` or `#all`: Mention all group members.
   - `/admin` or `#admin`: Mention all group admins.

2. **Settings Menu** (Admins Only):
   - **Message Format**:
     - `Small`: Sends mentions in batches of 5.
     - `Big`: Sends mentions up to Telegram's message limit.
   - **Silent Mention**:
     - `Off`: Mentions normally with `@username`.
     - `On`: Mentions silently with `[username](https://t.me/username)`.
   - **Bot Access**:
     - `Admins Only`: Commands can only be used by admins.
     - `All Users`: Commands can be used by all group members.

3. **Other Commands**:
   - `/help`: Displays all available commands and their descriptions.
   - `/cancel`: Cancels the currently running command.
   - `/broadcast <message>`: Broadcasts a message to all users and groups (auto-detects format).
   - `/stats`: Displays bot statistics and interaction details.

---

## 🗂️ Project Structure

```plaintext
mention/
├── app.json                # Metadata for Heroku deployment
├── config.py               # Configuration file for bot token and MongoDB URI
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Dockerfile for containerization
├── requirements.txt        # Python dependencies
├── startup                 # Startup script for the bot
├── bot/
│   ├── __init__.py         # Initialize bot package
│   ├── main.py             # Main bot logic
│   ├── database/           # Database-related code
│   │   └── __init__.py
│   ├── handlers/           # Command and callback handlers
│   │   ├── __init__.py
│   │   ├── mention.py      # Mention commands logic
│   │   └── settings.py     # Settings menu logic
│   └── modules/            # Additional modules
│       └── __init__.py
```

---

## ⚙️ Prerequisites

1. **Python 3.9+**
2. **MongoDB**: A running MongoDB instance or a connection URI.
3. **Docker** (optional): For containerized deployment.

---

## 🚀 Setup Guide

### 1. Clone the Repository

```bash
git clone <repository-url>
cd mention
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the Bot

Edit the `config.py` file and add your bot token and MongoDB URI:

```python
BOT_TOKEN = "<your-bot-token-here>"
MONGO_URI = "<your-mongodb-uri-here>"
OWNER_ID = "<your-owner-id>"
```

### 4. Run the Bot

```bash
python bot/main.py
```

---

## 🌐 Deployment

### Deploying on Heroku

1. Install the Heroku CLI.
2. Create a new Heroku app:

   ```bash
   heroku create
   ```

3. Add the MongoDB add-on or set the `MONGO_URI` environment variable.
4. Deploy the bot:

   ```bash
   git push heroku main
   ```

### Deploying on Koyeb

1. Create a new service on Koyeb.
2. Use the Dockerfile in this repository for deployment.
3. Set the environment variables `BOT_TOKEN` and `MONGO_URI`.

### Using Docker

1. Build the Docker image:

   ```bash
   docker build -t telegram-mention-bot .
   ```

2. Run the container:

   ```bash
   docker run -e BOT_TOKEN=<your-bot-token> -e MONGO_URI=<your-mongodb-uri> telegram-mention-bot
   ```

---

## 📜 License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.
