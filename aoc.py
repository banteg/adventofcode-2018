import re
import click
import requests
from pathlib import Path

from config import cookies


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
        imported = __import__(f.__module__)
        if imported.__name__ != '__main__':
            return f
        day = int(re.search(r'\d+', imported.__file__).group(0))
        part = f.__name__.split('_')[-1]
        click.secho(f'day {day}, part {part}')
        tests_ok = True
        for case, expected in cases.items():
            case_pretty = case.replace('\n', ', ')
            data = Data(case)
            result = f(data)
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


def input_file(day):
    return Path(f'inputs/day{day:02d}.txt')


def download_input(day, year=2018):
    r = requests.get(f'http://adventofcode.com/{year}/day/{day}/input', cookies=cookies)
    r.raise_for_status()
    path = input_file(day)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(r.text)
    print(f'downloaded input for day {day}')


def load_input(day):
    path = input_file(day)
    if not path.exists():
        download_input(day)
    return Data(path.read_text())
