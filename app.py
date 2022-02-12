from flask import Flask, render_template

app = Flask(__name__)

@app.route("/home")
def landing():
    return render_template("landing.html")
    
@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

@app.route("/journal")
def journal():
    return render_template("journal.html")

@app.route("/signin")
def signin():
    return render_template("signin.html")

if __name__ == '__main__':
    app.run(debug=True)