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
    'X-CMC_PRO_API_KEY': '0e8f29cb-7eaf-4fcc-8aa4-0a00b1802186',  # Auth token
}

with open('name_symbol.json', 'r') as fl:
    data = json.load(fl)

app = Flask(__name__)
sslify = SSLify(app)

URL = 'https://api.telegram.org/bot1205726686:AAG-lEGFB_xipMNrwA3rHxCzG6Dg04To8Vg/'  # Telegram bot


# https://api.telegram.org/bot1205726686:AAG-lEGFB_xipMNrwA3rHxCzG6Dg04To8Vg/SetWebhook?url=https://bardiervadim.pythonanywhere.com/
# https://api.telegram.org/bot1205726686:AAG-lEGFB_xipMNrwA3rHxCzG6Dg04To8Vg/SetWebhook?url=https://https://0651af91b033.ngrok.io/
# https://api.telegram.org/bot1205726686:AAG-lEGFB_xipMNrwA3rHxCzG6Dg04To8Vg/deleteWebhook   -> delete webhook

def write_json(data, filename='answer.json'):
    """Save server json-answer."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def send_message(chat_id, text='There in no text here'):
    """Send back message to the user."""
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=answer)
    return r.json()


def parse_text(text):
    """Parse user text (return name of the crypt)."""
    print(text)
    if text[0] != '/':
        return text
    pattern = r'/\w+'
    crypto = re.search(pattern=pattern, string=text).group()
    return crypto[1:].lower()


def get_price(crypto):
    """get crypt-name, returns price or error."""
    """Parse server answer (return crypt price)."""
    try:
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={}'.format(data[crypto])
    except KeyError:
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?slug={}'.format(crypto)

    session = Session()
    session.headers.update(headers)
    lst = []
    r = session.get(url).json()

    write_json(r, filename='aaa.json')

    try:
        for k, v in r['data'].items():
            lst.append(v)
            break
    except KeyError:
        return 'Invalid name of crypt! Please, use /name_cryptocurrency to get the current value of the cryptocurrency ' \
               'on the market (e.g. /bitcoin).'

    price = lst[0]['quote']['USD']['price']
    name = lst[0]['name']
    symbol = lst[0]['symbol']

    return price, name, symbol


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        message = r['message']['text']

        pattern = r'/\w+'

        if message == '/start':
            hello_text = 'Hi, I am a telegram bot that will help you stay abreast of the latest developments in the ' \
                         'world of cryptology. Write me /name_cryptocurrency to get the current value of the ' \
                         'cryptocurrency on the market (e.g. /bitcoin).'
            send_message(chat_id, text=hello_text)

        elif message == '/commands':
            commands_text = 'List of commands: \n' \
                            '1) /name_cryptocurrency to get the current value of the ' \
                            'cryptocurrency on the market (e.g. /bitcoin). \n' \
                            'P.S. Other commands are coming soon!'
            send_message(chat_id, text=commands_text)

        elif re.search(pattern, message):
            price = get_price(parse_text(message))
            if type(price) == tuple:
                send_message(chat_id, text='Цена криптовалюты {0} ({1}): {2} USD.'.format(price[1], price[2], price[0]))
            else:
                send_message(chat_id, text=price)
        else:
            send_message(chat_id,
                         text='Please, use /name_cryptocurrency to get the current value of the cryptocurrency ' \
                              'on the market (e.g. /bitcoin).')

        return jsonify(r)
    return '<h1>Bot welcomes you</h1>'


if __name__ == '__main__':
    app.run()
