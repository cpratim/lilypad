from flask import Flask, render_template, session, request
from near import *
from database import Database
from config import MONGODB_DBNAME as dbname
from config import MONGODB_PASSWORD as password

db = Database()

app = Flask(__name__)

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
    return render_template('purchase.html')

@app.route('/get_user_state/<user_id>')
def get_user_state(user_id):
    return get_user_state(user_id)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    create_user(username)
    return 'Success'

if __name__ == '__main__':
    app.run(debug=True)
