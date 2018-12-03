import re
import adventofcode
import click

ok = click.style('✔︎', fg='green')
fail = click.style('✘', fg='red')


def test(cases):
    def decorator(f):
        day = int(re.search(r'\d+', __import__(f.__module__).__file__).group(0))
        part = f.__name__.split('_')[-1]
        click.secho(f'day {day}, part {part}')
        tests_ok = True
        for case, expected in cases.items():
            result = f(case)
            if result == expected:
                click.secho(f'{ok} {repr(case)} == {result}')
            else:
                print(f'{fail} {repr(case)} == {result}, expected {expected}')
                tests_ok = False
        if tests_ok:
            data = adventofcode.load_input(day)
            result = f(data)
            click.secho(f'{result}\n')
        else:
            click.secho('tests failed\n', fg='red')
        return f
    return decorator
