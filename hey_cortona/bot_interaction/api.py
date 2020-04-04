import json
from typing import Dict

from flask import Flask, request, jsonify, Response

from bot_interaction.outbound_communication import User, BotSender
from config.app_config import AppConfig
from database.questions_database import QuestionsDatabase
from database.user_database import UserDatabase
from immediate.immediate import ImmediateSubsystem
from model.question import Question
from nlp.classifier import Classifier
from qna.qna_subsystem import QNASubsystem

app = Flask(__name__)


class SystemContainer:
    app_config: AppConfig = None
    bot: User = None
    sender: BotSender = None
    users_database: UserDatabase = None
    questions_database: QuestionsDatabase = None
    immediate_subsystem: ImmediateSubsystem = None
    qna_subsystem: QNASubsystem = None

    def __new__(cls):
        def decorator(func):
            return lambda: func(cls.users_database, cls.questions_database, cls.immediate_subsystem, cls.qna_subsystem)
        return decorator


@SystemContainer()
@app.route('/bot/checkUser', methods=['POST'])
def check_user(users_database: UserDatabase, questions_database: QuestionsDatabase,
               immediate_subsystem: ImmediateSubsystem, qna_subsystem: QNASubsystem):
    user_id = request.get_json().get("user_id")
    user: User = User.from_user_id(user_id)

    db_user: User = users_database.find_user(user)
    resp: Dict[str, str] = {}
    if db_user is None:
        resp["next_task"] = "register"
    elif db_user.answer_qid is not None:
        resp["next_task"] = "answer"
    else:
        resp["next_task"] = "proceed"

    return json.dumps(resp)


@SystemContainer()
@app.route('/bot/registerUserCompleted', methods=['POST'])
def register_user_completed(users_database: UserDatabase, questions_database: QuestionsDatabase,
                            immediate_subsystem: ImmediateSubsystem, qna_subsystem: QNASubsystem):
    memory: Dict = json.loads(request.values.get("Memory"))
    answers: Dict = memory.get("twilio").get("collected_data").get("register").get("answers")
    number = request.values.get("UserIdentifier")
    new_user = User.from_answers(number, answers)
    users_database.add_user(new_user)

    response: Dict = {"actions": [{"say": "You have registered successfully!"}]}
    return jsonify(response)


@SystemContainer()
@app.route('/bot/immediateMessage', methods=['POST'])
def send_immediate_message(users_database: UserDatabase, questions_database: QuestionsDatabase,
                           immediate_subsystem: ImmediateSubsystem, qna_subsystem: QNASubsystem):
    message: str = request.get_json().get("CurrentInput")
    sender_phone_number: str = request.get_json().get("UserIdentifier")
    user: User = User.from_user_id(sender_phone_number)
    sender_user: User = users_database.find_user(user)
    if sender_user.admin:
        immediate_subsystem.broadcast(message)
    else:
        return {"actions": [{"redirect": "task://fallback"}]}
    return Response(status=200)


@SystemContainer()
@app.route('/bot/qna', methods=['POST'])
def ask_qna(users_database: UserDatabase, questions_database: QuestionsDatabase,
            immediate_subsystem: ImmediateSubsystem, qna_subsystem: QNASubsystem):
    classifier: Classifier = Classifier(questions_database)
    user_id = request.get_json().get("UserIdentifier")
    user: User = User.from_user_id(user_id)
    user: User = users_database.find_user(user)
    message: str = request.get_json().get("CurrentInput")
    question: Question = Question(message)
    classifier.add_question(question)
    qna_subsystem.ask_question(user, question)

    response: Dict = {
        "actions": [{"say": "Oops. Looks like I don't have an answer. I'll be right back with an answer."}]}
    return jsonify(response)

@SystemContainer()
@app.route('/bot/answerQuestion', methods=['POST'])
def answer_question(users_database: UserDatabase, questions_database: QuestionsDatabase,
                    immediate_subsystem: ImmediateSubsystem, qna_subsystem: QNASubsystem):
    user_answer: str = request.get_json().get("answer")
    user_id: str = request.get_json().get("user_id")
    user: User = User.from_user_id(user_id)
    user: User = users_database.find_user(user)
    questions_database.add_answer(user.answer_qid, user_answer)
    users_database.update_user(user, {"answer_qid": None})
    return Response(status=200)


def start_server(app_config: AppConfig):
    SystemContainer.app_config = app_config
    SystemContainer.bot = User(app_config.BOT_PHONE_NUMBER, "BOT")
    SystemContainer.sender = BotSender(app_config.ACCOUNT_SID, app_config.AUTH_TOKEN, SystemContainer.bot)
    SystemContainer.users_database = UserDatabase(app_config.MONGO_URI)
    SystemContainer.questions_database = QuestionsDatabase(app_config.MONGO_URI)
    SystemContainer.immediate_subsystem = ImmediateSubsystem(SystemContainer.users_database, SystemContainer.sender)
    SystemContainer.qna_subsystem = QNASubsystem(SystemContainer.users_database, SystemContainer.questions_database,
                                                 SystemContainer.sender, app_config.number_of_people_to_ask)
    app.run(host="0.0.0.0", port=80)
