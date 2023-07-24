from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
    "apiKey": "AIzaSyAI6yc8a3e2gGvZsVNLTpB8UN1J0WG8Hyg",
    "authDomain": "meetlab-61f94.firebaseapp.com",
    "projectId": "meetlab-61f94",
    "storageBucket": "meetlab-61f94.appspot.com",
    "messagingSenderId": "142688931872",
    "appId": "1:142688931872:web:f35eaf3056870169d4ac45",
    "databaseURL": "https://meetlab-61f94-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase =pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return render_template('add_tweet.html')
        except :
            error = "Authintication failed"
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        bio = request.form['bio']
        full_name = request.form['full_name']
        username = request.form['username']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user = {"full_name":full_name, "username":username,"bio" : bio}
            UID = login_session['user']['localId']
            db.child("Users").child(UID).set(user)
            return render_template('/add_tweet')
        except :
            error = "Authintication failed"
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == "POST":
        title = request.form["title"]
        text = request.form["text"]  
        try:
            UID = login_session['user']['localId']
            tweet = {"title": title, "text": text, "UID": UID}
            db.child("Tweets").push(tweet)
            return redirect(url_for('all_tweets'))
        except:
            error = "Authentication error"
    return render_template("add_tweet.html")

@app.route('/all_tweets', methods=['GET','POST'])
def all_tweets():
    try:
        tweets = db.child("Tweets").get().val()
        return render_template('all_tweets.html', tweets=tweets)
    except:
        return "Error fetching tweets"

if __name__ == '__main__':
    app.run(debug=True)