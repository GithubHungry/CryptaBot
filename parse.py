from requests import Session
import re
from main import write_json

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '0e8f29cb-7eaf-4fcc-8aa4-0a00b1802186',
}


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


def main():
    print(get_price(parse_text('Сколько стоит /bitcoin?')))


if __name__ == '__main__':
    main()
