# Importing essential libraries and modules

from flask import Flask, render_template, request, redirect
from markupsafe import Markup
import numpy as np
import pandas as pd
from utils.fertilizer import fertilizer_dic
import requests
import config
import pickle

# ==============================================================================================

# -------------------------LOADING THE TRAINED MODELS -----------------------------------------------

# Loading crop recommendation model
import os
crop_recommendation_model_path = os.path.join(os.path.dirname(__file__), 'models', 'RandomForest.pkl')
crop_recommendation_model = pickle.load(
    open(crop_recommendation_model_path, 'rb'))

# =========================================================================================

# Custom functions for calculations

def weather_fetch(city_name):
    """
    Fetch and returns the temperature and humidity of a city
    :params: city_name
    :return: temperature, humidity
    """
    try:
        api_key = config.weather_api_key
        base_url = "http://api.openweathermap.org/data/2.5/weather?"

        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url, timeout=5)
        x = response.json()

        if x.get("cod") != "404" and "main" in x:
            y = x["main"]

            temperature = round((y["temp"] - 273.15), 2)
            humidity = y["humidity"]
            return temperature, humidity
        else:
            return None
    except Exception as e:
        print(f"Weather API error: {e}")
        return None

# ===============================================================================================
# ------------------------------------ FLASK APP -------------------------------------------------

app = Flask(__name__)

# render home page
@ app.route('/')
def home():
    title = 'Harvestify - Home'
    return render_template('index.html', title=title)

# render crop recommendation form page
@ app.route('/crop-recommend')
def crop_recommend():
    title = 'Harvestify - Crop Recommendation'
    return render_template('crop.html', title=title)

# render fertilizer recommendation form page
@ app.route('/fertilizer')
def fertilizer_recommendation():
    title = 'Harvestify - Fertilizer Suggestion'
    return render_template('fertilizer.html', title=title)

# ===============================================================================================

# RENDER PREDICTION PAGES

# render crop recommendation result page
@ app.route('/crop-predict', methods=['POST'])
def crop_prediction():
    title = 'Harvestify - Crop Recommendation'

    if request.method == 'POST':
        try:
            N = int(request.form['nitrogen'])
            P = int(request.form['phosphorous'])
            K = int(request.form['pottasium'])
            ph = float(request.form['ph'])
            rainfall = float(request.form['rainfall'])

            # Check if manual temperature and humidity are provided
            manual_temp = request.form.get('temperature')
            manual_humidity = request.form.get('humidity')
            
            if manual_temp and manual_humidity:
                # Use manual values
                temperature = float(manual_temp)
                humidity = float(manual_humidity)
                print(f"Using manual weather values: temp={temperature}, humidity={humidity}")
            else:
                # Try to fetch weather data from city
                city = request.form.get("city")
                weather_data = weather_fetch(city)
                if weather_data != None:
                    temperature, humidity = weather_data
                    print(f"Weather API successful for {city}: temp={temperature}, humidity={humidity}")
                else:
                    # Use default average values if weather API fails
                    temperature = 25.0  # Average temperature in Celsius
                    humidity = 70.0  # Average humidity percentage
                    print(f"Weather API failed for {city}, using default values: temp={temperature}, humidity={humidity}")

            data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
            print(f"Input data: N={N}, P={P}, K={K}, temp={temperature}, humidity={humidity}, pH={ph}, rainfall={rainfall}")
            my_prediction = crop_recommendation_model.predict(data)
            final_prediction = my_prediction[0]
            print(f"Predicted crop: {final_prediction}")

            return render_template('crop-result.html', prediction=final_prediction, title=title)
        except Exception as e:
            print(f"Error in crop prediction: {e}")
            import traceback
            traceback.print_exc()
            return render_template('try_again.html', title=title)

# render fertilizer recommendation result page
@ app.route('/fertilizer-predict', methods=['POST'])
def fert_recommend():
    title = 'Harvestify - Fertilizer Suggestion'

    crop_name = str(request.form['cropname'])
    N = int(request.form['nitrogen'])
    P = int(request.form['phosphorous'])
    K = int(request.form['pottasium'])

    df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'Data', 'fertilizer.csv'))

    nr = df[df['Crop'] == crop_name]['N'].iloc[0]
    pr = df[df['Crop'] == crop_name]['P'].iloc[0]
    kr = df[df['Crop'] == crop_name]['K'].iloc[0]

    n = nr - N
    p = pr - P
    k = kr - K
    temp = {abs(n): "N", abs(p): "P", abs(k): "K"}
    max_value = temp[max(temp.keys())]
    if max_value == "N":
        if n < 0:
            key = 'NHigh'
        else:
            key = "Nlow"
    elif max_value == "P":
        if p < 0:
            key = 'PHigh'
        else:
            key = "Plow"
    else:
        if k < 0:
            key = 'KHigh'
        else:
            key = "Klow"

    response = Markup(str(fertilizer_dic[key]))

    return render_template('fertilizer-result.html', recommendation=response, title=title)

# ===============================================================================================
if __name__ == '__main__':
    print('=' * 80)
    print('🌿 HARVESTIFY SERVER STARTING')
    print('=' * 80)
    print('✅ Crop recommendation available')
    print('✅ Fertilizer suggestion available')
    print('=' * 80)
    print('🌐 Open your browser and go to: http://127.0.0.1:5000')
    print('=' * 80)
    app.run(debug=True, host='0.0.0.0', port=5000)
