import math

import networkx as nx


def main():
    graph = nx.Graph()
    with open('data/day25.txt') as f:
        for line in f:
            src, dsts = line.strip().split(': ')
            for dst in dsts.split(' '):
                graph.add_edge(src, dst)

    ebc = nx.edge_betweenness_centrality(graph).items() 
    to_cut = sorted(ebc, key=lambda e: e[1], reverse=True)[:3]
    for (src, dst), _ in to_cut:
        graph.remove_edge(src, dst)
    part1 = math.prod(len(c) for c in nx.connected_components(graph)) 
    assert part1 == 525264
    print(f'Part 1: {part1}')

if __name__ == '__main__':
    main()
