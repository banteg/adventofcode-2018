import re
import json
import click
import requests
from os.path import exists


ok = click.style('✔︎', fg='green')
fail = click.style('✘', fg='red')


class Data(str):

    @property
    def int_lines(self):
        return [int(x) for x in self.splitlines()]

    @property
    def ints_lines(self):
        return [
            [int(x) for x in re.findall(r'-?\d+', line)]
            for line in self.splitlines()
        ]


def test(cases):
    def decorator(f):
        day = int(re.search(r'\d+', __import__(f.__module__).__file__).group(0))
        part = f.__name__.split('_')[-1]
        click.secho(f'day {day}, part {part}')
        tests_ok = True
        for case, expected in cases.items():
            case_pretty = case.replace('\n', ', ')
            result = f(Data(case))
            if result == expected:
                click.secho(f'{ok} {case_pretty} == {result}')
            else:
                print(f'{fail} {case_pretty} == {result}, expected {expected}')
                tests_ok = False
        if tests_ok:
            data = load_input(day)
            result = f(Data(data))
            click.secho(f'{result}\n')
        else:
            click.secho('tests failed\n', fg='red')
        return f
    return decorator


def input_name(day):
    return f'inputs/day{day:02d}.txt'


def download_input(day, year=2018):
    cookies = json.load(open('cookie.json'))
    r = requests.get(f'http://adventofcode.com/{year}/day/{day}/input', cookies=cookies)
    r.raise_for_status()
    with open(input_name(day), 'w') as f:
        f.write(r.text)
    print(f'downloaded input for day {day}')


def load_input(day):
    name = input_name(day)
    if not exists(name):
        download_input(day)
    return open(name).read().strip()
