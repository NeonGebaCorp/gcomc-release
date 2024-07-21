import os
import requests
import json

SERVER_URL = 'https://neoncorp.eu.org:8853'
LOGIN_PATH = os.path.expanduser('~/.neon/login')

def save_wallet_hash(wallet_hash):
    os.makedirs(os.path.dirname(LOGIN_PATH), exist_ok=True)
    with open(LOGIN_PATH, 'w') as f:
        f.write(wallet_hash)

def load_wallet_hash():
    if os.path.exists(LOGIN_PATH):
        with open(LOGIN_PATH, 'r') as f:
            return f.read().strip()
    return None

def create_wallet():
    passphrase = input('Enter a passphrase to secure your wallet: ')
    response = requests.post(SERVER_URL + '/new_wallet', json={'passphrase': passphrase})
    wallet_hash = response.json()['wallet_hash']
    save_wallet_hash(wallet_hash)
    print(f'New wallet created: {wallet_hash}')
    print_wallet_balance(wallet_hash, passphrase)

def restore_wallet(wallet_hash):
    passphrase = input('Enter your wallet passphrase: ')
    response = requests.post(SERVER_URL + '/restore_wallet', json={'wallet_hash': wallet_hash, 'passphrase': passphrase})
    if response.status_code == 200:
        save_wallet_hash(wallet_hash)
        print(f'Wallet restored: {wallet_hash}')
        print_wallet_balance(wallet_hash, passphrase)
    else:
        print('Wallet not found or incorrect passphrase')

def send_funds(sender, passphrase):
    receiver = input('Enter receiver address: ')
    amount = int(input('Enter amount: '))
    response = requests.post(SERVER_URL + '/send', json={'sender': sender, 'receiver': receiver, 'amount': amount})
    if response.status_code == 200:
        print(f'Transaction successful: {response.json()}')
        print_wallet_balance(sender, passphrase)
    else:
        print(f'Error: {response.json()["error"]}')

def show_transactions(wallet_hash):
    response = requests.post(SERVER_URL + '/transactions', json={'wallet_hash': wallet_hash})
    print('Transactions:')
    for tx in response.json()['transactions']:
        print(tx)

def print_wallet_balance(wallet_hash, passphrase):
    response = requests.post(SERVER_URL + '/restore_wallet', json={'wallet_hash': wallet_hash, 'passphrase': passphrase})
    if response.status_code == 200:
        balance = response.json()['balance']
        print(f'Wallet balance: {balance} GCOMC')

def main():
    wallet_hash = load_wallet_hash()
    if wallet_hash:
        passphrase = input('Enter your wallet passphrase: ')
        print_wallet_balance(wallet_hash, passphrase)
    else:
        print('1. Make new wallet')
        print('2. Restore wallet')
        choice = input('Select an option: ')
        if choice == '1':
            create_wallet()
            wallet_hash = load_wallet_hash()
        elif choice == '2':
            wallet_hash = input('Enter your wallet hash: ')
            restore_wallet(wallet_hash)
            wallet_hash = load_wallet_hash()
        else:
            print('Invalid choice')
            return
    
    while True:
        print('1. Send funds')
        print('2. Show transactions')
        print('3. Exit')
        print('4. Show wallet hash (not recommended)')
        choice = input('Select an option: ')
        if choice == '1':
            send_funds(wallet_hash, passphrase)
        elif choice == '2':
            show_transactions(wallet_hash)
        elif choice == '3':
            break
        elif choice == '4':
            print(f'Wallet hash: {wallet_hash}')
        else:
            print('Invalid choice')

if __name__ == '__main__':
    print('GCOMC Wallet')
    main()
