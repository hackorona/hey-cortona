import json
import os
from typing import Dict, List

from flask import Flask, request, jsonify

from bot_interaction.outbound_communication import OutboundSender, User, BotSender
from database.user_database import UserDatabase
from immediate.immediate import ImmediateSubsystem
from model.question import Question
from qna.qna_subsystem import QNASubsystem

app = Flask(__name__)

ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
MONGO_URI = os.getenv('MONGO_URI')

bot: User = User("+14155238886", "CORONA_BOT")

sender: BotSender = BotSender(ACCOUNT_SID, AUTH_TOKEN, bot)
users_database: UserDatabase = UserDatabase(MONGO_URI)
immediate_subsystem: ImmediateSubsystem = ImmediateSubsystem(users_database, sender)
qna_subsystem: QNASubsystem = QNASubsystem(users_database, sender, 3)


users: List[User] = []

@app.route('/bot/registerUser', methods=['POST'])
def register_user():
    user_id = request.get_json().get("user_id")
    user: User = User.from_user_id(user_id)

    db_user: User = users_database.findUser(user)

    resp: Dict[str, bool] = {"exists": (db_user is not None)}
    return json.dumps(resp)

@app.route('/bot/registerUserCompleted', methods=['POST'])
def register_user_completed():
    memory: Dict = json.loads(request.values.get("Memory"))
    answers: Dict = memory.get("twilio").get("collected_data").get("register").get("answers")
    city: str = answers.get("city").get("answer")
    name: str = answers.get("name").get("answer")
    help_us: str = answers.get("help_us").get("answer")
    number = request.values.get("UserIdentifier")
    new_user = User.from_user_id(number, name, city, help_us)
    users_database.addUser(new_user)

    response: Dict = {"actions": [{"say": "נרשמת בהצלחה. שאל אותי כל שאלה (:"}]}
    return jsonify(response)

@app.route('/bot/immediateMessage', methods=['POST'])
def send_immediate_message():
    message: str = request.get_json().get("CurrentInput")
    sender_phone_number: str = request.get_json().get("UserIdentifier")
    user: User = User.from_user_id(sender_phone_number)
    sender_user: User = users_database.findUser(user)
    if sender_user.admin:
        immediate_subsystem.broadcast(bot, message)

@app.route('/bot/qna', methods=['POST'])
def ask_qna():
    user_id = request.get_json().get("user_id")
    user: User = User.from_user_id(user_id)
    message: str = request.get_json().get("CurrentInput")
    question: Question = Question(message)
    qna_subsystem.ask_question(user, question)

    response: Dict = {"actions": [{"say": "תפסת אותי לא מוכן. מיד מברר לך."}]}
    return jsonify(response)






def start_server():
    app.run(host="0.0.0.0", port=80)
