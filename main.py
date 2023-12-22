from flask import Flask, render_template, request, redirect, url_for, send_file
from discord_webhook import DiscordWebhook
import base64
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/pixel.png')
def print_file():
  ip = request.headers.get(
    'X-Forwarded-For', request.headers.get('X-Real-IP', request.remote_addr))
  id = request.args.get('id')
  token = request.args.get('token')
  label = base64.b64decode(request.args.get('label')).decode('utf-8')
  webhook = DiscordWebhook(
    url='https://discord.com/api/webhooks/' + id + '/' + token,
    content=datetime.now().strftime('%m-%d-%Y %H:%M:%S') +
    f' | **{label}** | {ip} @everyone')
  response = webhook.execute()
  return send_file("static/pixel.png", mimetype="image/png")


if __name__ == '__main__':
  app.run(port=8000, host='0.0.0.0')
