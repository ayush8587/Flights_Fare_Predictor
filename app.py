from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from forms import InputForm
import pandas as pd
import joblib
from datetime import timedelta

app = Flask(__name__)
app.config["SECRET_KEY"] = "this_is_the_secret_key"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

model = joblib.load("model.joblib")

@app.route('/')
@app.route('/home')
def home():
    form = InputForm()
    return render_template("home.html", form=form)

@app.route('/submit', methods=['POST'])
def submit():
    form = InputForm()
    if form.validate_on_submit():
        x_new = {
            'airline': form.airline.data,
            'date_of_journey': form.date_of_journey.data.strftime("%Y-%m-%d"),
            'source': form.source.data,
            'destination': form.destination.data,
            'dep_time': form.dep_time.data.strftime("%H:%M:%S"),
            'arrival_time': form.arr_time.data.strftime("%H:%M:%S"),
            'duration': form.duration.data,
            'total_stops': form.total_stops.data,
            'additional_info': form.additional_info.data
        }
        
        df_new = pd.DataFrame(x_new, index=[0])
        prediction = model.predict(df_new)[0]
        session['prediction'] = round(prediction, 0)
        session['form_data'] = x_new
        return jsonify({'result': round(prediction,0)})
    return jsonify({'result': 'Invalid form submission'})

@app.route('/predict')
def predict():
    if 'prediction' in session:
        pred = session['prediction']
        form_data = session['form_data']
    else:
        return redirect(url_for("home"))
    return render_template("predict.html", pred=pred, form_data=form_data)

if __name__ == '__main__':
    app.run(debug=True)
