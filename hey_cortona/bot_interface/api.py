import os
from typing import Dict

from flask import Flask, request, jsonify

from bot_interface.outbound_communication import OutboundSender, User

app = Flask(__name__)

ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

sender: OutboundSender = OutboundSender(ACCOUNT_SID, AUTH_TOKEN)

bot: User = User("+14155238886", "CORONA_BOT")

@app.route('/bot/registerUser', methods=['POST'])
def register_user():
    user_id: str = request.get_json()["user_id"]
    user: User = User.from_raw(user_id)

    sender.send(bot, user, "Gotcha, you naughty user trying to register!")

    # TODO add database check
    response: Dict[str, bool] = {"exists": True}
    return jsonify(response)


def start_server():
    app.run(host="0.0.0.0", port=80)
