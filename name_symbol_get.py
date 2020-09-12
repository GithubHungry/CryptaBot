import json

with open('crypt_info.json', 'r') as fl:
    data = json.load(fl)

    right_list = {}

    for row in data:
        right_list[row['name'].lower()] = row['symbol'].lower()

    with open('name_symbol.json', 'w') as write_file:
        json.dump(right_list, write_file)


