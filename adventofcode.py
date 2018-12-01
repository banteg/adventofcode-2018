import requests
from os.path import exists
from config import cookies


def input_name(day):
    return f'inputs/day{day:02d}.txt'


def download_input(day):
    r = requests.get(f'http://adventofcode.com/2018/day/{day}/input', cookies=cookies)
    r.raise_for_status()
    with open(input_name(day), 'w') as f:
        f.write(r.text)
    print(f'downloaded input for day {day}')


def load_input(day):
    name = input_name(day)
    if not exists(name):
        download_input(day)
    return open(name).read().strip()
