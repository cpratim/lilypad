from flask import Flask
from near import *

app = Flask(__name__)

@app.route('/')
def ping():
    return 'Status: OK'


@app.route('/create-business/<business_name>')
def create_business_api(business_name):
    return create_business(business_name)

@app.route('/create-investor/<investor_name>/<business_name>')
def create_investor_api(investor_name, business_name):
    return create_investor(investor_name, business_name)

@app.route('/get-account-state/<account_id>')
def get_account_state_api(account_id):
    return get_account_state(account_id)

@app.route('/initialize-frog-balance/<amount>/<account_id>')
def initialize_frog_balance_api(amount, account_id):
    return initialize_frog_balance(amount, account_id)

@app.route('/transfer-frog/<reciever>/<amount>')
def transfer_frog_api(reciever, amount):
    return transfer_frog(reciever, amount)


if __name__ == '__main__':
    app.run(debug=True)