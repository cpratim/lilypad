import os
import sys
import subprocess
import json
from pprint import pprint

INITIAL_BUSINESS_BALANCE = 10
INITIAL_PERSON_BALANCE = 1

INITIAL_BUSINESS_FROG = int(1e10)
INITIAL_INVESTOR_FROG = 1

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
    command = f'near state {account_id}'  
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

def initialize_frog_balance(balance, account_name):
    command = '''near call $ID storage_deposit '{"account_id": "''' + account_name + '''"}' --accountId lilypad.testnet --amount ''' + str(balance)
    out = [None]
    execute(command, out)
    return parse_json(out[0])

def transfer_frog(reciever, amount):
    command = '''near call lilypad.testnet ft_transfer {"receiver_id": "''' + reciever + '''", "amount": "''' + str(amount) + '''"}' --accountId $ID --amount 0.000000000000000000000001'''
    out = [None]
    execute(command, out)
    return parse_json(out[0])

def get_frog_balance(account):
    command = '''near view lilypad.testnet ft_balance_of '{"account_id": "''' + account + '''"}' '''
    out = [None]
    execute(command, out)
    return parse_json(out[0])

if __name__ == '__main__':
    r = get_account_state('pratim.merry_lane.lilypad.testnet')
    pprint(r)