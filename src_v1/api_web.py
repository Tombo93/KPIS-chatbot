from flask import Flask, render_template, request, Response #, jsonify
import time
import pandas as pd
import os
from dotenv import load_dotenv


load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("API_KEY_OPENAI")


# Run with: python -m flask --app api_web run
app = Flask(__name__)

########## Chatbot Web-Interface ##########
@app.route("/")
def index():
    return render_template("chatbot.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_message = (data or {}).get("message", "")

    # Replace this with your model streaming logic
    def stream():
        text = f"You said: {user_message}. Here's a thoughtful response."
        usage = 0
        for token in text.split():
            chunk = token + " "
            usage += len(chunk)
            yield f'{{"delta": "{chunk}", "usage": {usage}}}\n'
            time.sleep(0.04)  # simulate streaming
        # Final newline ensures reader completes cleanly
        yield "\n"

    def invoke_agent():
        yield f'{{"delta": "{user_message}", "usage": "placeholder"}}\n'

    return Response(invoke_agent(), mimetype="text/plain")  # plain text with JSON lines

if __name__ == "__main__":
    app.run(debug=True)


########## Local Rest API ##########
@app.route("/api/v1/")
def get_articles():
   return "Hello, Articles!"


class Articles:
    def __init__(self):
        self.df = pd.read_csv("artikel-fiktiv.csv")

    def get_articles(self):
        pass

    def get_filtered_articles(self):
        pass