from distutils.log import debug
from flask import Flask, redirect, url_for, render_template, request
import random 
import json
import pickle 
import numpy as np 
import nltk
from nltk.stem import WordNetLemmatizer
import tensorflow.keras as keras
from keras.models import load_model
from flask_ngrok import run_with_ngrok

app = Flask(__name__)

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl','rb'))
model = load_model('chatbot_model.h5')

def getResponse(ints, intents_json):
    tag = ints[0]["intent"]
    list_of_intents = intents_json["intents"]
    for i in list_of_intents:
        if i["tag"] == tag:
            result = random.choice(i["responses"])
            break
    return result

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
 sentence_words = clean_up_sentence(sentence)
 bag = [0] * len(words)
 for w in sentence_words:
  for i, word in enumerate(words):
      if word==w:
          bag[i] = 1
 return np.array(bag)

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bag_of_words(sentence)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


@app.route("/home")
def landing():
    return render_template("landing.html")
    
@app.route("/chatbot", methods=["POST","GET"])
def chatbot():
    if request.method == "POST":
        message = request.form["msg"]
        ints = predict_class(message, model)
        res = getResponse(ints, intents)
        return render_template("chatbot.html", message=res)
    else:    
        return render_template("chatbot.html")

@app.route("/resources")
def resources():
    return render_template("resources.html")

if __name__ == '__main__':
    app.run()
