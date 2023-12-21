start = None
plots: set[tuple[int, int]] = set()

with open('data/day21.txt') as f:
    for y, row in enumerate(f):
        for x, c in enumerate(row):
            if c == '.':
                plots.add((x, y))
            elif c == 'S':
                start = (x, y)
                plots.add(start)

if start is None:
    raise Exception('Start not found')

locations: set[tuple[int, int]] = {start}
seen: dict[tuple[int, int], set[tuple[int, int]]] = {}
for _ in range(64):
    new_locations: set[tuple[int, int]] = set()
    for location in locations:
        if location not in seen:
            x, y = location
            neighbors = set(
                neighbor for neighbor in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1))
                if neighbor in plots
            )
            seen[location] = neighbors
        new_locations.update(seen[location])
    locations = new_locations
    
print(len(locations))
