from flask import Flask
import socket

app = Flask(__name__)

@app.route('/')
def home():
    return f"Container ID: {socket.gethostname()}"

@app.route('/hello')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True)