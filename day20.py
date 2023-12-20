from dataclasses import dataclass
from enum import Enum

ON, OFF = True, False
HIGH, LOW = True, False
PULSES = {HIGH: 0, LOW: 0}


class ModuleType(Enum):
    BROADCASTER = ''
    FLIP_FLOP = '%'
    CONJUNCTION = '&'


@dataclass
class Module:
    type: ModuleType
    ouputs: tuple[str, ...]
    memory: dict[str, bool]
    on: bool = OFF

    def process(self, input: str, pulse: bool):
        if self.type == ModuleType.FLIP_FLOP:
            if pulse is HIGH:
                return
            self.on = not self.on
            return self.on
        if self.type == ModuleType.CONJUNCTION:
            self.memory[input] = pulse
            for _, p in self.memory.items():
                if not p:
                    return HIGH
            return LOW
        return pulse


def main():
    broadcaster, modules = get_modules()
    for _ in range(1000):
        push_button(broadcaster, modules)
    part1 = PULSES[HIGH] * PULSES[LOW]
    assert part1 == 912199500
    print(f'Part 1: {part1}')


def get_modules() -> tuple[str, dict[str, Module]]:
    modules: dict[str, Module] = {}
    broadcaster = ''
    conjunctions: set[str] = set()
    with open('data/day20.txt') as f:
        for line in f:
            module, b = line.strip().split(' -> ')
            outputs = tuple(b.split(', '))
            if module[0] == ModuleType.FLIP_FLOP.value:
                module_type = ModuleType.FLIP_FLOP
                module = module[1:]
            elif module[0] == ModuleType.CONJUNCTION.value:
                module_type = ModuleType.CONJUNCTION
                module = module[1:]
                conjunctions.add(module)
            else:
                module_type = ModuleType.BROADCASTER
                broadcaster = module
            modules[module] = Module(module_type, outputs, {})

    for name, module in modules.items():
        for output in module.ouputs:
            if output in conjunctions:
                modules[output].memory[name] = False

    return broadcaster, modules


def push_button(broadcaster: str, modules: dict[str, Module]):
    queue: list[tuple[str, str, bool]] = [('button', broadcaster, LOW)]
    while queue:
        from_name, name, pulse = queue.pop(0)
        PULSES[pulse] += 1
        if name not in modules:
            continue
        module = modules[name]
        pulse = module.process(from_name, pulse)
        if pulse is None:
            continue
        for out in module.ouputs:
            queue.append((name, out, pulse))


if __name__ == '__main__':
    main()
