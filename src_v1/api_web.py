from flask import Flask # , jsonify, request
import pandas as pd


########## Local Rest API ##########
# Run with: python -m flask --app api_web run

app = Flask(__name__)

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


