from flask import Flask, render_template, request
from utils.weather_auto import automatic_weather_risk
from utils.cnn_predict import predict_cnn_risk
from utils.nlp_predict import predict_text_risk
from utils.social_intelligence import build_social_text
from utils.fusion import fuse_risk, risk_level

import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", result=None)


@app.route("/predict", methods=["POST"])
def predict():

    try:
        city = request.form.get("city")
        file = request.files.get("image")

        # validation (like streamlit)
        if not city:
            return render_template("index.html", result=None, error="Enter city")

        if not file or file.filename == "":
            return render_template("index.html", result=None, error="Upload image")

        # save image
        image_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(image_path)

        # get social/news signals
        news_text, _ = build_social_text(city)

        # model predictions
        weather = automatic_weather_risk(city)
        cnn = predict_cnn_risk(image_path)
        nlp = predict_text_risk(news_text)

        final, w1, w2, w3 = fuse_risk(weather, cnn, nlp)
        level = risk_level(final)

        result = {
            "city": city,
            "weather": round(weather, 3),
            "cnn": round(cnn, 3),
            "nlp": round(nlp, 3),
            "final": round(final, 3),
            "level": level,
            "news": news_text.split(".")[:5]
        }

        return render_template("index.html", result=result)

    except Exception as e:
        print("ERROR:", e)
        return render_template("index.html", result=None, error=str(e))


if __name__ == "__main__":
    app.run(debug=True)
