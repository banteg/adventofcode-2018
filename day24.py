import re
from typing import Set, List, Dict
from dataclasses import dataclass, field
from collections import defaultdict
from itertools import cycle, count
from operator import attrgetter

import aoc

import click

DEBUG = False
unit_id = count()
unit_re = re.compile(
    r'(\d+) units each with (\d+) hit points (?:\((.*)\) )?with an attack that does (\d+) (\w+) damage at initiative (\d+)'
)


def log(*args, enabled=DEBUG, **kwds):
    if enabled:
        print(*args, **kwds)


@dataclass
class Group:
    units: int
    hitpoints: int
    weak: Set[str]
    immune: Set[str]
    damage: int
    attack: str
    initiative: int
    id_: int = field(default_factory=unit_id.__next__)

    @property
    def effective_power(self):
        return self.units * self.damage

    @property
    def alive(self):
        return self.units > 0

    def damage_to(self, defending):
        if self.attack in defending.immune:
            return 0
        elif self.attack in defending.weak:
            return 2 * self.effective_power
        else:
            return self.effective_power

    def perform_attack(self, other, damage):
        other.units -= damage // other.hitpoints
        other.units = max(other.units, 0)

    @classmethod
    def from_string(cls, text, id_=None):
        match = unit_re.search(text)
        if match is None:
            raise ValueError
        units, hitpoints, raw_specials, damage, attack, initiative = match.groups()
        specials = defaultdict(set)
        if raw_specials:
            for special in raw_specials.split('; '):
                kind, types = special.split(' to ')
                specials[kind] = set(types.split(', '))
        return cls(
            int(units),
            int(hitpoints),
            specials['weak'],
            specials['immune'],
            int(damage),
            attack,
            int(initiative),
            id_,
        )

    def __hash__(self):
        return hash(self.id_)

    def __repr__(self):
        return f'<{self.id_}: {self.units}u {self.hitpoints}hp>'


class Fight:
    def __init__(self, armies):
        self.armies = armies
        self.order = cycle(armies.keys())

    def simulate(self):
        outcome = None
        r = count(1)
        while not outcome:
            log(f'round {next(r)}'.center(80, '-'))
            attacking, defending = self.switch_sides()
            log('Attacking:')
            for group in attacking:
                if not group.alive:
                    continue
                log(f'{group.id_} contains {group.units} units')
            log('Defending:')
            for group in defending:
                if not group.alive:
                    continue
                log(f'{group.id_} contains {group.units} units')
            log()
            targets = self.select_targets(attacking, defending)
            attacking, defending = self.switch_sides()
            targets.update(self.select_targets(attacking, defending))
            log()
            self.attack(targets)
            outcome = self.check_outcome()
        log('=' * 80)
        for army in self.armies:
            log(f'{army}:')
            all_dead = sum(g.units for g in self.armies[army] if g.alive) == 0
            if all_dead:
                log('No groups remain.')
            else:
                for group in self.armies[army]:
                    log(f'{group.id_} contains {group.units} units')
        log()
        return outcome

    def switch_sides(self):
        a, b = next(self.order), next(self.order)
        next(self.order)
        return self.armies[a], self.armies[b]

    def select_targets(self, attacking, defending):
        targets = {}
        for group in sorted(
            attacking, key=attrgetter('effective_power', 'initiative'), reverse=True
        ):
            if not group.alive:
                continue
            damages = [
                (group.damage_to(other), other.effective_power, other.initiative, other)
                for other in defending
                if other.alive
                and other not in targets.values()
                and group.damage_to(other) > 0
            ]
            try:
                targets[group] = sorted(damages, reverse=True)[0][3]
            except IndexError:
                pass
            for d in damages:
                log(f'{group.id_} would deal {d[3].id_} {d[0]} damage')
        return targets

    def attack(self, targets):
        kill_counter = 0
        for attacker in sorted(targets, key=attrgetter('initiative'), reverse=True):
            if not attacker.alive:
                continue
            defender = targets[attacker]
            before = defender.units
            damage = attacker.damage_to(defender)
            attacker.perform_attack(defender, damage)
            kill_counter += before - defender.units
            log(
                f'{attacker.id_} attacks {defender.id_}, killing {before - defender.units} units'
            )
        if kill_counter == 0:
            click.secho('endless fight', fg='red')
            raise ValueError('endless fight')

    def check_outcome(self):
        unit_counts = [
            sum(group.units for group in groups if group.alive)
            for groups in self.armies.values()
        ]
        unit_counts = [x for x in unit_counts if x > 0]
        if len(unit_counts) == 1:
            return unit_counts[0]


def parse_input(data):
    ids = defaultdict(count)
    groups: Dict[str, List[Group]] = {}
    for line in data.splitlines():
        if line.endswith(':'):
            faction = line.rstrip(':')
            groups[faction] = []
        elif line:
            unit = Group.from_string(
                line, id_=f'{faction} group {next(ids[faction]) + 1}'
            )
            groups[faction].append(unit)
    return groups


example = '''
    Immune System:
    17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
    989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

    Infection:
    801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
    4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
    '''


@aoc.test({example: 5216})
def part_1(data: aoc.Data):
    log(data, end='\n\n')
    groups = parse_input(data)
    fight = Fight(groups)
    return fight.simulate()
