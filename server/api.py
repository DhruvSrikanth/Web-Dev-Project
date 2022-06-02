from flask import Flask, request, render_template
import json
import sqlite3
import sys

app = Flask(__name__)

# Database Connection
# conn = sqlite3.connect('')
# cur = conn.cursor()

@app.route('/login', methods=['GET'])
def login():
    print("Login Page")
    return render_template('../templates/login/login.html')   


if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)