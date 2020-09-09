from flask import Flask
from flask import request
from flask import jsonify
import requests
from requests import Session
import re
import json

from flask_sslify import SSLify

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '0e8f29cb-7eaf-4fcc-8aa4-0a00b1802186',
}

app = Flask(__name__)
sslify = SSLify(app)

URL = 'https://api.telegram.org/bot1205726686:AAG-lEGFB_xipMNrwA3rHxCzG6Dg04To8Vg/'


# https://api.telegram.org/bot1205726686:AAG-lEGFB_xipMNrwA3rHxCzG6Dg04To8Vg/SetWebhook?url=https://bardiervadim.pythonanywhere.com/
# https://api.telegram.org/bot1205726686:AAG-lEGFB_xipMNrwA3rHxCzG6Dg04To8Vg/deleteWebhook

def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def send_message(chat_id, text='bla-bla-bla'):
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=answer)
    return r.json()


def parse_text(text):
    pattern = r'/\w+'
    crypto = re.search(pattern=pattern, string=text).group()
    return crypto[1:]


def get_price(crypto):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?slug={}'.format(crypto)

    session = Session()
    session.headers.update(headers)
    lst = []
    r = session.get(url).json()

    for k, v in r['data'].items():
        lst.append(v)
        break

    price = lst[0]['quote']['USD']['price']

    return price


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        message = r['message']['text']

        pattern = r'/\w+'

        if re.search(pattern, message):
            price = get_price(parse_text(message))
            send_message(chat_id, text='Цена криптовалюты: {} USD.'.format(price))

        return jsonify(r)
    return '<h1>Bot welcomes you</h1>'


if __name__ == '__main__':
    app.run()
