# mention-bot

<p align="center">
  <img src="https://raw.githubusercontent.com/TelegramBots/book/master/src/docs/logo.png" width="120"/>
</p>

---

<h2 align="center">🚀 Telegram Mention Bot</h2>

A powerful, production-ready Telegram bot to mention all group members or admins, with a beautiful settings menu, MongoDB integration, and full deployment support for Heroku, Koyeb, and Docker.

---

## ✨ Features

- <b>Group & Admin Mention:</b> Use <code>@all</code>, <code>#all</code>, <code>@admin</code>, <code>#admin</code> to mention everyone or just admins.
- <b>Settings Menu:</b> Inline keyboard for message format, silent mention, and bot access (admins only).
- <b>Owner Commands:</b> <code>/broadcast</code> (send to all users/groups), <code>/stats</code> (bot stats, user/group list).
- <b>Cancel & Help:</b> <code>/cancel</code> to stop, <code>/help</code> for instructions.
- <b>MongoDB Integration:</b> Tracks users, groups, command history, and boot logs.
- <b>Markdown/HTML Detection:</b> Broadcasts auto-detect formatting.
- <b>Health Check Web Server:</b> For Koyeb/Heroku deployment.
- <b>Production Ready:</b> Robust error handling, logging, and modular code.

---

## 🗂️ Project Structure

```
/
├── config.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── app.json
├── startup
├── webapp.py
├── README.md
└── bot/
    ├── __main__.py
    ├── __init__.py
    ├── database/
    ├── handlers/
    └── modules/
```

---

## ⚡ Quick Start

1. <b>Clone the repo:</b>
   ```sh
   git clone https://github.com/yourusername/mention-bot.git
   cd mention-bot
   ```
2. <b>Install dependencies:</b>
   ```sh
   pip install -r requirements.txt
   ```
3. <b>Configure:</b> Edit <code>config.py</code> with your bot token, MongoDB URI, and owner ID.
4. <b>Run the bot:</b>
   ```sh
   python -m bot
   ```

---

## ☁️ Deploy

### <img src="https://www.herokucdn.com/favicon.ico" width="18"/> Heroku
- Click <b>Deploy to Heroku</b> or use the Heroku CLI:
- Set <code>BOT_TOKEN</code>, <code>MONGODB_URI</code>, <code>OWNER_ID</code> in Heroku config vars.
- The <code>app.json</code> and <code>startup</code> script are ready for Heroku.

### <img src="https://avatars.githubusercontent.com/u/67589757?s=200&v=4" width="18"/> Koyeb
- Deploy as a Python web service.
- Set <code>BOT_TOKEN</code>, <code>MONGODB_URI</code>, <code>OWNER_ID</code> as environment variables.
- The bot exposes <code>/</code> and <code>/health</code> endpoints for health checks.

### 🐳 Docker
- Build and run with Docker Compose:
   ```sh
   docker-compose up --build
   ```

---

## 🛠️ Settings Menu

- <b>Message Format:</b> Small (5 at a time) or Big (max allowed by Telegram)
- <b>Silent Mention:</b> On (silent) or Off (normal @user)
- <b>Bot Access:</b> Admins only or All users

---

## 📚 Commands

| Command         | Description                                 |
|-----------------|---------------------------------------------|
| <code>@all</code>, <code>#all</code> | Mention all group members                |
| <code>@admin</code>, <code>#admin</code> | Mention all admins                        |
| <code>/help</code>         | Show help and instructions                |
| <code>/settings</code>     | Settings menu (admins only)               |
| <code>/cancel</code>       | Cancel running command                    |
| <code>/broadcast</code>    | Owner only: broadcast message             |
| <code>/stats</code>        | Owner only: show bot stats and chat list  |

---

## 🧑‍💻 Contributing

Pull requests and issues are welcome! Please open an issue for bugs or feature requests.

---

## 📄 License

MIT

---

<p align="center"><b>Made with ❤️ for Telegram communities</b></p>
