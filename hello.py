from flask import Flask

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import numpy as np
import pandas as pd

app = Flask(__name__)




@app.route("/")
def hello_world():
    df = pd.read_csv('./dataset_bahasa_indonesia.csv', sep=',')
    analyzer = SentimentIntensityAnalyzer()
    print(analyzer.polarity_scores("VADER itu pintar dan menyenangkan"))
    df['scores'] = df['text'].apply(lambda text: analyzer.polarity_scores(text))
    df['compound']  = df['scores'].apply(lambda score_dict: score_dict['compound'])
    # print(df.head())

    return (df.head())