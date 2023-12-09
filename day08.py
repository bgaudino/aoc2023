import math
import re
from itertools import cycle
from typing import Mapping, TypeAlias

Network: TypeAlias = Mapping[str, Mapping[str, str]]


def main():
    with open('data/day08.txt') as f:
        instructions, data = f.read().split('\n\n')

    network = get_network(data)
    part1 = traverse(instructions, network)
    assert part1 == 19951
    print(f'Part 1: {part1}')

    part2 = traverse(instructions, network, ghosts=True)
    assert part2 == 16342438708751
    print(f'Part 2: {part2}')


def get_network(data: str) -> Network:
    network: Network = {}
    for line in data.split('\n'):
        node, left, right = re.findall(r'[A-Z]{3}', line)
        network[node] = {'L': left, 'R': right}
    return network


def traverse(instructions: str, network: Network, ghosts: bool = False) -> int:
    locations = [n for n in network if n.endswith('A')] if ghosts else ['AAA']
    cycles: dict[int, int] = {}
    for i, instruction in enumerate(cycle(instructions), 1):
        locations = [network[location][instruction] for location in locations]
        if ghosts:
            for j, location in enumerate(locations):
                if location.endswith('Z'):
                    cycles[j] = i
            if len(cycles) == len(locations):
                return math.lcm(*cycles.values())
        elif all(location == 'ZZZ' for location in locations):
            return i
    raise ValueError('Network is empty')


if __name__ == '__main__':
    main()
