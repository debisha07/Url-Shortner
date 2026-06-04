from flask import Flask, request , render_template , redirect
import re
from urllib.parse import urlsplit
import random , string , sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/main") 
def validate_url():
    print("HIT /main")
    url = request.args.get('user')
    print("URL RECEIVED:", url)
    if url == None or url.strip() == "" :
        return "Invalid format has been given.."
    if len(url) > 100 :
        return "Invalid format has been given.."
    url_split = urlsplit(url) 
    if url_split.scheme not in ["http" , "https"] :
        return "Invalid format"
    if url_split.hostname is None:
        return "Invalid format"
    return generate()

def generate() :
    url = request.args.get('user')
    length = 7
    short= ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    con = sqlite3.connect("url.db")
    cursor = con.cursor()
    cursor.execute("SELECT short_url FROM urls WHERE short_url == ?" , (short,))
    result = cursor.fetchone() 
    while(result != None) :
        short= ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        cursor.execute("SELECT short_url FROM urls WHERE short_url == ?" , (short,))
        result = cursor.fetchone() 
    cursor.execute("INSERT INTO urls(short_url , main_url) VALUES(? , ?)" , (short , url))
    con.commit()
    con.close()
    res = f"{request.host_url}{short}"
    return render_template("index.html",result=res )


@app.route("/<short>")
def check(short) :
    con = sqlite3.connect("url.db")
    cursor = con.cursor()
    cursor.execute("SELECT main_url from urls WHERE short_url = ?", (short,))
    result = cursor.fetchone()
    if result is None:
        con.close()
        return "404 : Short URL not found"
    else:
        con.close()
        return redirect(result[0])

app.run(debug=True)