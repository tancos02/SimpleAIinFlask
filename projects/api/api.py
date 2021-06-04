# Import library
import flask
from flask import request, jsonify
import joblib 
import pickle
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures

# Import model from file
model = joblib.load('../../model.pkl')

# Flask initiation
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Read data for transforming platform, genre, and publisher into number
data = pd.read_excel("../../output.xlsx")
platform_arr = data['Platform'].unique()
genre_arr = data['Genre'].unique()
publisher_arr = data['Publisher'].unique()

@app.route('/result', methods=['POST'])
def result():
    query_body = request.form
    platform = query_body.get('platform')
    genre = query_body.get('genre')
    publisher = query_body.get('publisher')
    return (getResult(platform, genre, publisher))

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

def getResult(platform, genre, publisher) :
    plat_found = 0
    gen_found = 0
    publ_found = 0
    # Transform input into number
    for i in range(len(platform_arr)) :
        if(platform_arr[i] == platform) :
            platform_num = i + 1
            plat_found = 1
            break
    for i in range(len(genre_arr)) :
        if(genre_arr[i] == genre) :
            genre_num = i + 1
            gen_found = 1
            break
    for i in range(len(publisher_arr)) :
        if(publisher_arr[i] == publisher) :
            publisher_num = i + 1
            publ_found = 1
            break
    if((plat_found == 1) and (gen_found == 1) and (publ_found == 1)) :
        arr_in = [[platform_num, genre_num, publisher_num]]
    else :
        if(plat_found == 0) :
            platform_num = len(platform_arr) + 1
        if(gen_found == 0) :
            genre_num = len(genre_arr) + 1
        if(publ_found == 0) :
            publisher_num = len(publisher_arr) + 1
        arr_in = [[platform_num, genre_num, publisher_num]]
    data_in = pd.DataFrame(arr_in,columns = ['Platform','Genre','Publisher'])
    # Transform number input into input for model
    poli_degree = 6
    pr = PolynomialFeatures(degree=poli_degree)
    data_in_pr=pr.fit_transform(data_in)
    # Predict result 
    prediction = model.predict(data_in_pr)
    return jsonify(prediction[0])    
app.run()