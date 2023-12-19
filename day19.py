import re
from dataclasses import dataclass
from typing import Callable, Optional, TypeAlias


Condition: TypeAlias = Callable[[dict[str, int]], Optional[str]]


@dataclass
class Workflow:
    conditions: list[Condition]

    def process(self, values: dict[str, int]):
        for condition in self.conditions:
            result = condition(values)
            if result is not None:
                return result


def main():
    workflows: dict[str, Workflow] = {}
    with open('data/day19.txt') as f:
        a, b = f.read().split('\n\n')
        for line in a.split('\n'):
            name, workflow = parse_workflow(line)
            workflows[name] = workflow
        parts: list[dict[str, int]] = []
        for line in b.split('\n'):
            parts.append(parse_part(line))

    part1 = sum(
        sum(part.values()) for part in parts if is_accepted(part, workflows)
    )
    print(f'Part 1: {part1}')


def is_accepted(part: dict[str, int], workflows: dict[str, Workflow]):
    name = 'in'
    while True:
        workflow = workflows[name]
        result = workflow.process(part)
        if result == 'A':
            return True
        if result in ('R', None):
            return False
        name = result


def parse_workflow(text: str):
    match = re.match(r'[a-z]+', text)
    if match is None:
        raise ValueError('No workflow name')
    name = match[0]
    step_str = next(re.finditer(r'(?<={)(.*?)(?=})', text))[0]
    fns: list[Condition] = []
    for s in step_str.split(','):
        if ':' in s:
            condition, destination = s.split(':')
            operator = next(re.finditer(r'[<>]', condition))[0]
            value, _, digits = condition.partition(operator)
            num = int(digits)

            def get_fn(v: str, op: str, n: int, dst: str):
                def fn(d: dict[str, int]):
                    if op == '>':
                        return dst if d[v] > n else None
                    if op == '<':
                        return dst if d[v] < n else None
                return fn
            fns.append(get_fn(value, operator, num, destination))
        else:
            fns.append(lambda d: s)
    return name, Workflow(fns)


def parse_part(text: str):
    values: dict[str, int] = {}
    split = text[1:-1].split(',')
    for item in split:
        k, v = item.split('=')
        values[k] = int(v)
    return values


if __name__ == '__main__':
    main()
