import math
import heapq

with open('data/day17.txt') as f:
    city = [[int(n) for n in row.strip()] for row in f]

max_x = len(city[0])
max_y = len(city)

def solve(part2: bool = False):
    queue = [(0, 0, 0, -1, -1)]
    seen = set() 
    min_heat = math.inf
    while queue:
        dist, r, c, dir_, indir = heapq.heappop(queue)
        if (r, c, dir_, indir) in seen:
            continue
        seen.add((r, c, dir_, indir))
        if (c, r) == (max_x - 1, max_y - 1):
            min_heat = min(min_heat, dist)
            continue
        for i, (dr, dc) in enumerate([[-1, 0], [0, 1], [1, 0], [0, -1]]):
            rr = r+dr
            cc = c+dc
            new_dir = i
            new_indir = (1 if new_dir != dir_ else indir+1)

            isnt_reverse = ((new_dir + 2) % 4 != dir_)

            isvalid = (new_indir <= 3)
            # isvalid_part2 = (new_indir <= 10 and (
            #     new_dir == dir_ or indir >= 4 or indir == -1))
            # isvalid = (isvalid_part2 if part2 else isvalid_part1)

            if 0 <= rr < max_y and 0 <= cc < max_y and isnt_reverse and isvalid:
                cost = city[rr][cc]
                if (rr, cc, new_dir, new_indir) in seen:
                    continue
                heapq.heappush(queue, (dist+cost, rr, cc, new_dir, new_indir))

    return min_heat
    ans = 1e9
    for (r, c, dir_, indir), v in D.items():
        if r == max_y-1 and c == max_y-1 and (indir >= 4 or not part2):
            ans = min(ans, v)
    return ans


part1 = solve()
print(part1)
assert part1 == 953
