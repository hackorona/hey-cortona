import json
import os
from typing import Dict, List

from flask import Flask, request, jsonify

from bot_interaction.outbound_communication import OutboundSender, User, BotSender
from database.questions_database import QuestionsDatabase
from database.user_database import UserDatabase
from immediate.immediate import ImmediateSubsystem
from model.question import Question
from nlp.classifier import Classifier
from qna.qna_subsystem import QNASubsystem

app = Flask(__name__)

ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
MONGO_URI = os.getenv('MONGO_URI')

bot: User = User("+14155238886", "CORONA_BOT")

sender: BotSender = BotSender(ACCOUNT_SID, AUTH_TOKEN, bot)
users_database: UserDatabase = UserDatabase(MONGO_URI)
questions_database: QuestionsDatabase = QuestionsDatabase(MONGO_URI)
immediate_subsystem: ImmediateSubsystem = ImmediateSubsystem(users_database, sender)
qna_subsystem: QNASubsystem = QNASubsystem(users_database, sender, 3)
qna_subsystem.start()

users: List[User] = []


@app.route('/bot/checkUser', methods=['POST'])
def check_user():
    user_id = request.get_json().get("user_id")
    user: User = User.from_user_id(user_id)

    db_user: User = users_database.findUser(user)
    resp: Dict[str, str] = {}
    if db_user is None:
        resp["next_task"] = "register"
    elif db_user.answer_qid is not None:
        resp["next_task"] = "answer"
    else:
        resp["next_task"] = "proceed"

    return json.dumps(resp)


@app.route('/bot/registerUserCompleted', methods=['POST'])
def register_user_completed():
    memory: Dict = json.loads(request.values.get("Memory"))
    answers: Dict = memory.get("twilio").get("collected_data").get("register").get("answers")
    number = request.values.get("UserIdentifier")
    new_user = User.from_answers(number, answers)
    users_database.addUser(new_user)

    response: Dict = {"actions": [{"say": "You have registered successfully!"}]}
    return jsonify(response)


@app.route('/bot/immediateMessage', methods=['POST'])
def send_immediate_message():
    message: str = request.get_json().get("CurrentInput")
    sender_phone_number: str = request.get_json().get("UserIdentifier")
    user: User = User.from_user_id(sender_phone_number)
    sender_user: User = users_database.findUser(user)
    if sender_user.admin:
        immediate_subsystem.broadcast(bot, message)
    return ""

@app.route('/bot/qna', methods=['POST'])
def ask_qna():
    classifier: Classifier = Classifier(questions_database)
    user_id = request.values.get("UserIdentifier")
    user: User = User.from_user_id(user_id)
    user: User = users_database.findUser(user)
    message: str = request.values.get("CurrentInput")
    question: Question = Question(message)
    classifier.add_question(question)
    print("Finished nlp")
    qna_subsystem.ask_question(user, question)

    response: Dict = {
        "actions": [{"say": "Oops. Looks like I don't have an answer. I'll be right back with an answer."}]}
    return jsonify(response)

@app.route('/bot/answerQuestion', methods=['POST'])
def answerQuestion():
    user_answer: str = request.get_json().get("answer")
    user_id: str = request.get_json().get("user_id")
    user: User = User.from_user_id(user_id)
    user: User = users_database.findUser(user)
    questions_database.add_answer(user.answer_qid, user_answer)
    users_database.updateUser(user, {"answer_qid": None})


def start_server():
    app.run(host="0.0.0.0", port=80)
