import re

from collections import OrderedDict

from fundamentus import get_data

def to_float(string):
    formatted = re.sub(r'[.%]', '', string).replace(',', '.')
    return float(formatted)

def transform(item_name, item_value):
    roic = to_float(item_value['ROIC'])
    ev_ebit = to_float(item_value['EV/EBIT'])

    return { 'name': item_name, 'roic': roic, 'ev_ebit': ev_ebit }

def rank(lst):
    eligible = []

    for item_name,item_value in lst.items():
        item = transform(item_name, item_value)
        if item['roic'] > 0 and item['ev_ebit'] > 0:
            eligible.append(item)

    eligible = sorted(eligible, key=lambda x: x['roic'], reverse=True)

    for position, item in enumerate(eligible):
        item['roic_rank'] = position

    eligible = sorted(eligible, key=lambda x: x['ev_ebit'])

    for position, item in enumerate(eligible):
        item['ev_ebit_rank'] = position
        item['final_rank'] = item['roic_rank'] + item['ev_ebit_rank']

    eligible = sorted(eligible, key=lambda x: x['final_rank'])
    return eligible

def output(lst):
    ranked = rank(lst)

    print('{0:<7} {1:<10} {2:<7} {3:<10} {4:<10} {5:<10}'.format(
        'Papel',
        'EV/EBIT',
        'ROIC',
        'EV/EBIT Rank',
        'ROIC Rank',
        'Final Rank'
    ))

    for item in ranked:
        print('{0:<7} {1:<10} {2:<7} {3:<10} {4:<10} {5:<10}'.format(
            item['name'],
            item['ev_ebit'],
            item['roic'],
            item['ev_ebit_rank'],
            item['roic_rank'],
            item['final_rank'],
        ))

if __name__ == '__main__':
    from waitingbar import WaitingBar
    
    THE_BAR = WaitingBar('[*] Downloading...')
    lst = get_data()
    THE_BAR.stop()
    
    output(lst)
