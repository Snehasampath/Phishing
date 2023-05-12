from flask import Flask
from flask import Flask, render_template, request, redirect, url_for, session
from flask import render_template
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################

@app.route("/")
def index():
    #return (
        # f"Welcome to the Phx Software Companies <br/>")
    return render_template('index.html')

@app.route('/predict', methods =['GET', 'POST'])
def predict():
    msg = ''
    if request.method == 'POST' and 'inputurl' in request.form :
        inputurl = request.form['inputurl']
        legitimate_urls = pd.read_csv("dataset/legitimate-urls.csv")
        phishing_urls = pd.read_csv("dataset/phishing-urls.csv")
        lurls=legitimate_urls['Domain']
        purls=phishing_urls['Domain']
        urls = legitimate_urls.append(phishing_urls)
        urls = urls.drop(urls.columns[[0,3,5]],axis=1)
        urls = urls.sample(frac=1).reset_index(drop=True)
        urls_without_labels = urls.drop('label',axis=1)
        labels = urls['label']
        data_train, data_test, labels_train, labels_test = train_test_split(urls_without_labels, labels, test_size=0.30, random_state=110)
        custom_random_forest_classifier = RandomForestClassifier(n_estimators=500, max_depth=20, max_leaf_nodes=10000)
        custom_random_forest_classifier.fit(data_train,labels_train)
        custom_classifier_prediction_label = custom_random_forest_classifier.predict(data_test)
        importances = custom_random_forest_classifier.feature_importances_
        indices = np.argsort(importances)[::-1]
        model = DecisionTreeClassifier()
        model.fit(data_train,labels_train)
        #pred_label = model.predict(data_test)
        msg='Data not trained!'
        for dt in lurls:
            if dt == inputurl:
                print('Legitimate URL!')
                msg='Legitimate URL!'
        for dt in purls:
            if dt == inputurl:
                print('Phishing URL!')
                msg='Phishing URL!'
    return render_template('index.html', msg = msg)
    
if __name__ == "__main__":
    app.run(debug=True)