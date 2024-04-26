from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

from ice_breaker_llama3 import ice_breaker_with

load_dotenv()

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")
    #return render_template("index2.html")


@app.route("/process", methods=["POST"])
def process():
    nome = request.form["name"]
    #summary_and_facts, interests, ice_breakers, profile_pic_url = ice_breaker_with(
    summary, profile_pic_url = ice_breaker_with(name=nome)
    return jsonify(
        {
            "summary_and_facts": summary.to_dict(),
            "picture_url": profile_pic_url,
            #"interests": interests.to_dict(),
            #"ice_breakers": ice_breakers.to_dict(),
        }
    )


if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=True)