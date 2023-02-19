from flask import Flask, render_template, session, request, redirect
from near import *
from database import Database
from config import MONGODB_DBNAME as dbname
from config import MONGODB_PASSWORD as password
from pprint import pprint

db = Database()

app = Flask(__name__)
app.config['SECRET_KEY'] = "lilypad"

@app.route('/create-business/<business_name>')
def create_business_api(business_name):
    return create_business(business_name)

@app.route('/get-account-state/<account_id>')
def get_account_state_api(account_id):
    return get_account_state(account_id)

@app.route('/initialize-frog-balance/<amount>/<account_id>')
def initialize_frog_balance_api(amount, account_id):
    return initialize_frog_balance(amount, account_id)

@app.route('/transfer-frog/<reciever>/<amount>')
def transfer_frog_api(reciever, amount):
    return transfer_frog(reciever, amount)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/browse')
def browse():
    return render_template('browse.html')

@app.route('/purchase')
def purchase():
    if 'username' not in session:
        return render_template('login.html')
    username = session.get('username')
    state = get_account_state(username)
    frog = get_frog_balance(f"{username}.lilypad.testnet")
    state['formattedAmount'] = state['formattedAmount'][:5]
    pprint(state)
    pprint(frog)
    return render_template('purchase.html', username=username, state=state, frog=frog)


@app.route('/login/<username>')
def login(username):
    session['username'] = username
    return redirect('/browse')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    session['username'] = username
    create_user(username)
    return 'Success'

@app.route('/api/buy', methods=['POST'])
def buy():
    data = request.get_json()
    amount = int(data['amount'])
    username = session.get('username')
    transfer_frog(f"{username}.lilypad.testnet", amount)
    subtract_near(username, amount)
    return 'Success'

if __name__ == '__main__':
    app.run(debug=True)
