import os

from flask import Flask

from hey_cortona.bot_interface.outbound_communication import OutboundSender, User

app = Flask(__name__)

ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

sender: OutboundSender = OutboundSender(ACCOUNT_SID, AUTH_TOKEN)

bot: User = User("+14155238886", "CORONA_BOT")
ben: User = User("+972543533078", "Doron Kabilio")

@app.route('/bot/regiser_user', methods=['POST'])
def register_user():
    # TODO register users to database
    pass


@app.route('/bot/ask', methods=['POST'])
def ask():
    sender.send(bot, ben, "Hey Doron Kabilio ;)")


def start_server():
    app.run(host="0.0.0.0", port=80)