from flask import Flask

app = Flask(__name__)

@app.route('/')
def ping():
    return 'Status: OK'


if __name__ == '__main__':
    app.run(debug=True)