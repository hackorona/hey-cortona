import os
from typing import Dict

from flask import Flask, request, jsonify

from bot_interface.outbound_communication import OutboundSender, User

app = Flask(__name__)

ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

sender: OutboundSender = OutboundSender(ACCOUNT_SID, AUTH_TOKEN)

bot: User = User("+14155238886", "CORONA_BOT")
ben: User = User("+972543533078", "Doron Kabilio")

@app.route('/bot/registerUser', methods=['POST'])
def register_user():
    # TODO register users to database
    print(f"register {request.get_json()}")
    response: Dict[str, bool] = {"exists": True}
    return jsonify(response)

@app.route('/bot/ask', methods=['POST'])
def ask():
    sender.send(bot, ben, "Hey Doron Kabilio ;)")


def start_server():
    app.run(host="0.0.0.0", port=80)
