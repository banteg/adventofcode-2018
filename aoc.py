import re
import click
import requests
from os.path import exists
from config import cookies


ok = click.style('✔︎', fg='green')
fail = click.style('✘', fg='red')


def test(cases):
    def decorator(f):
        day = int(re.search(r'\d+', __import__(f.__module__).__file__).group(0))
        part = f.__name__.split('_')[-1]
        click.secho(f'day {day}, part {part}')
        tests_ok = True
        for case, expected in cases.items():
            case_pretty = case.replace('\n', ', ')
            result = f(case)
            if result == expected:
                click.secho(f'{ok} {case_pretty} == {result}')
            else:
                print(f'{fail} {case_pretty} == {result}, expected {expected}')
                tests_ok = False
        if tests_ok:
            data = load_input(day)
            result = f(data)
            click.secho(f'{result}\n')
        else:
            click.secho('tests failed\n', fg='red')
        return f
    return decorator


def input_name(day):
    return f'inputs/day{day:02d}.txt'


def download_input(day, year=2018):
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
