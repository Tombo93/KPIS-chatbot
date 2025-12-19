import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, Response

from agent import Agent
from db import insert_entries


# Run with: python -m flask --app chatbot run
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("chatbot.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_message = (data or {}).get("message", "")
    agent = Agent()
    def invoke_agent():
        content, total_tokens = agent.invoke(user_message)
        insert_entries(user_message, content, total_tokens, None, p_type="unknown", table="exp_agent_v1")
        yield f'{{"delta": "{content}", "usage":"{total_tokens}"}}\n'

    return Response(invoke_agent(), mimetype="text/plain")


if __name__ == "__main__":
    load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv("API_KEY_OPENAI")
    
    app.run()
