from flask import Flask, request

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/', methods=['POST'])
def send():
    return 1

@app.route('/', methods=['GET'])
def do():
    return 'hello'

if __name__ == '__main__':
    app.run()
