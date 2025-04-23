from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Telegram Mention Bot</h1><p>The bot is running and healthy.</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
