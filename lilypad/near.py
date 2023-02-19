import os
import sys
import subprocess
import json
from pprint import pprint

INITIAL_BUSINESS_BALANCE = 5
INITIAL_PERSON_BALANCE = 5

INITIAL_BUSINESS_FROG = 1000
INITIAL_INVESTOR_FROG = 1000

def execute(command, out):
    print(command)
    try:
        output = subprocess.check_output(command, shell=True).decode('utf-8')
        out[0] = output
        print(out)
        return True
    except Exception as error:
        print('exception, error')
        out[0] = False
    return False

def parse_json(raw):
    raw.replace(' ', '')
    raw = raw.replace(':', '":')
    raw = raw.replace(',', ',"')
    raw = raw.replace('{', '{"')
    raw = raw.replace("'", '"')
    raw = raw.replace('True', 'true')
    raw = raw.replace('False', 'false')
    raw = raw.replace('None', 'null')
    d = json.loads(raw)
    data = {}
    for key, value in d.items():
        key = key.replace(' ', '')
        data[key] = value
    return data

def get_account_state(account_id):
    out = [None]
    command = f'near state {account_id}.lilypad.testnet'  
    execute(command, out)
    raw = ''.join(out[0].split('\n')[1:-1])
    return parse_json(raw)

def create_business(business_name):
    out = [None]
    command = f"near create-account {business_name}.lilypad.testnet --masterAccount lilypad.testnet --initialBalance {INITIAL_BUSINESS_BALANCE}"
    execute(command, out)
    if (out[0]):
        out = initialize_frog_balance(INITIAL_BUSINESS_FROG, f"{business_name}.lilypad.testnet")
    return get_account_state(business_name)

def create_investor(investor_name, business_name):
    out = [None]
    command = f"near create-account {investor_name}.{business_name}.lilypad.testnet --masterAccount {business_name}.lilypad.testnet --initialBalance {INITIAL_PERSON_BALANCE}"
    execute(command, out)
    if (out[0]):
        out = initialize_frog_balance(INITIAL_INVESTOR_FROG, f"{investor_name}.{business_name}.lilypad.testnet")
    return investor_name

def create_user(username):
    out = [None]
    command = f"near create-account {username}.lilypad.testnet --masterAccount lilypad.testnet --initialBalance {INITIAL_PERSON_BALANCE}"
    execute(command, out)
    initialize_frog_balance(INITIAL_BUSINESS_FROG, f"{username}.lilypad.testnet")
    return 'success'

def initialize_frog_balance(balance, account_name):
    command = '''near call lilypad.testnet storage_deposit '' --accountId ''' + account_name + ''' --amount ''' + str(.00125)
    out = [None]
    execute(command, out)

def get_frog_balance(account):
    command = '''near view lilypad.testnet ft_balance_of '{"account_id": "''' + account + '''"}' '''
    out = [None]
    execute(command, out)
    raw = ''.join(out[0].split('\n')[1:-1])
    raw = raw.replace("'", '')
    return int(raw)

def transfer_frog(reciever, amount):
    command = '''near call lilypad.testnet ft_transfer '{"receiver_id": "''' + reciever + '''", "amount": "''' + str(amount) + '''"}' --accountId lilypad.testnet --amount 0.000000000000000000000001'''
    out = [None]
    execute(command, out)
    return 'success'

def subtract_near(username, amount):
    command = f'''near send {username}.lilypad.testnet lilypad.testnet {amount}'''
    out = [None]
    execute(command, out)
    return 'success'

if __name__ == '__main__':
    r = get_account_state('cpratim1')
    pprint(r)