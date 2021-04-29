from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    prediction = 0
    # return 'Hello World'
    if request.method == "POST":
        model = pickle.load(open("lr_model.pkl", "rb"))
        # input0 = request.form.get("unnamed")
        input1 = float(request.form.get("latitude"))
        input2 = float(request.form.get("longitude"))
        input3 = float(request.form.get("temperature"))
        input4 = float(request.form.get("humidity"))
        input5 = float(request.form.get("pressure"))
        input6 = float(request.form.get("visibility"))
        input7 = float(request.form.get("windspeed"))
        input8 = float(request.form.get("precipitation"))
        input9 = float(request.form.get("year"))
        input10 = float(request.form.get("month"))
        input11 = float(request.form.get("weekday"))
        input12 = float(request.form.get("day"))
        input13 = float(request.form.get("hour"))
        input14 = float(request.form.get("minute"))
        arr = np.array(
            [
                [
                    input1,
                    input2,
                    input3,
                    input4,
                    input5,
                    input6,
                    input7,
                    input8,
                    input9,
                    input10,
                    input11,
                    input12,
                    input13,
                    input14,
                ]
            ]
        )
        print(arr)
        prediction = model.predict(arr)
        print(prediction)

    return render_template("index.html", prediction=prediction)


if __name__ == "__main__":
    app.run(debug=True)
