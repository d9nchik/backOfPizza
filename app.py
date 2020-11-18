from json import load, dumps

from flask import Flask


def loadFile():
    with open('db.json') as f:
        return load(f)


bigJsonObj = loadFile()

app = Flask(__name__)

from flask import request


@app.after_request
def add_cors_headers(response):
    if True:
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Headers', 'Cache-Control')
        response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
        response.headers.add('Access-Control-Allow-Headers', 'Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
    return response


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/getProducts')
def openProducts():
    return dumps(bigJsonObj['products'])


@app.route('/getCategories')
def openCategories():
    return dumps(bigJsonObj['productsCategories'])


@app.route('/getIngredients')
def getIngredients():
    return dumps(bigJsonObj['ingredients'])


@app.route('/getRecommended')
def getRecommended():
    return dumps(bigJsonObj['recommendations'])


@app.route('/getPromotions')
def getPromotions():
    return dumps(bigJsonObj['promotions'])


import time


@app.route('/sendData', methods=['POST'])
def add_message():
    content = request.json
    print(content)
    submitDataToGod(content)
    submitToSlave(content)
    return '{}'.format(int(time.time()))


def submitDataToGod(content):
    text = ''
    for key in content:
        text += f'{key}: {content[key]}\n'
    send_message(admin_chat_id, f'Создатель тебе заказ: \n{text}')


def submitToSlave(content):
    if content['phone'] not in registration.keys():
        return
    items_text = '{\n'
    for product_url in content['cart']:
        item = list(filter(lambda product: product['url'] == product_url, bigJsonObj['products']))[0]
        items_text += f'{item["productName"]}: {content["cart"][product_url]}\n'
    items_text += '}'
    text = 'Дата: {}\nВремя: {}\nКуда: {}\n Что: {}'.format(content['date'], content['time'], content['address'],
                                                            items_text)
    send_message(registration[content]['phone'], f'Привет {content["firstName"]} вот твой заказ: \n{text}')


import requests, re

admin_chat_id = 479246950

registration = {}


@app.route('/webHook', methods=['POST'])
def receive_updates():
    content = request.json
    print(content)
    chat_id = request.json["message"]["chat"]["id"]
    chat_text = content['message']['text']
    if re.match(r'/register 09\d{8}', chat_text):
        number = chat_text.split()
        registration[number[1]] = chat_id
        send_message(chat_id, "Спасибо, что присоединился.\nЯ сообщу о твоих заказах")
    else:
        send_message(chat_id, 'Введи команду в формате /register 0975962756\n где 0975962756 - ваш номер телефона')
    return {"ok": True}


def send_message(chat_id, text):
    method = "sendMessage"
    token = "1492534854:AAG5K7FpyLGe2TEgxBYRz8jx-b588ylHYGg"
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)


if __name__ == '__main__':
    app.run()
