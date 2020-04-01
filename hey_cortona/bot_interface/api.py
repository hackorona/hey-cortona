import os
from typing import Dict, List

from flask import Flask, request, jsonify

from bot_interface.outbound_communication import OutboundSender, User

app = Flask(__name__)

ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

sender: OutboundSender = OutboundSender(ACCOUNT_SID, AUTH_TOKEN)

bot: User = User("+14155238886", "CORONA_BOT")

users: List[User] = []

@app.route('/bot/registerUser', methods=['POST'])
def register_user():
    user_id: str = request.get_json().get("user_id")
    user: User = User.from_raw(user_id)

    sender.send(bot, user, "Gotcha, you naughty user trying to register!")

    # TODO add database check
    exists: bool = False
    for u in users:
        if u.number == user.number:
            exists = True
            break
    response: Dict[str, bool] = {"exists": exists}
    return jsonify(response)

@app.route('/bot/registerUserCompleted', methods=['POST'])
def register_user_completed():
    questions = request.values.get("collected_data").get("register").get("answers")
    number = request.values.get("From")
    name = questions.get("name").get("answer")
    city = questions.get("city").get("answer")
    new_user = User(number, name, city)
    users.append(new_user)

    print(f"register completed:\n\n\n{new_user}\n\n\n")
    response: Dict = {"actions": [{"say": "נרשמת בהצלחה. שאל אותי כל שאלה (:"}]}
    return jsonify(response)


def start_server():
    app.run(host="0.0.0.0", port=80)
