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

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city = request.form.get("city")
        image = request.files.get("image")

        # your existing logic
        result = process(city, image)  # or whatever your function is

        return render_template("index.html", result=result)

    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    city = request.form["city"]

    # file upload
    file = request.files["image"]
    image_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(image_path)

    # get live news
    news_text, keyword_score = build_social_text(city)

    # run models
    weather = automatic_weather_risk(city)
    cnn = predict_cnn_risk(image_path)
    nlp = predict_text_risk(news_text)

    final, w1, w2, w3 = fuse_risk(weather, cnn, nlp)
    level = risk_level(final)

    return render_template(
        "index.html",
        result=True,
        city=city,
        weather=round(weather, 3),
        cnn=round(cnn, 3),
        nlp=round(nlp, 3),
        final=round(final, 3),
        level=level,
        news=news_text[:300]
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
