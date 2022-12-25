import concurrent.futures
import functools
import json
import os
from itertools import chain, combinations
from concorde.tsp import TSPSolver
import uuid

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1))

def get_solution(points, graph):
    name = f"{uuid.uuid4()}.tsp"
    with open(name, "w") as f:
        f.write("NAME: graph\n")
        f.write("TYPE: TSP\n")
        f.write(f"DIMENSION: {len(points)}\n")
        f.write("EDGE_WEIGHT_TYPE: EXPLICIT\n")
        f.write("EDGE_WEIGHT_FORMAT: FULL_MATRIX\n")
        f.write("EDGE_WEIGHT_SECTION\n")
        for i in points:
            for j in points:
                for edge in graph["Edges"]:
                    if edge[0] in (i, j) and edge[1] in (i, j):
                        f.write(f"{str(edge[2])} ")
                        break
                else:
                    f.write("0 ")
            f.write("\n")

    solver = TSPSolver.from_tspfile(name)
    solution = solver.solve()
    os.remove(name)
    return solution

def path_and_profit(subset, graph):
    profit = sum([graph["Profits"][i] for i in subset])
    solution = get_solution(subset, graph)
    if solution.success:
        tour = list(solution.tour)
        tour.append(tour[0])
        return profit, tour

if __name__ == "__main__":
    with open("graph.json", "r") as f:
        graph = json.load(f)
    path_and_profit_graph = functools.partial(path_and_profit, graph=graph)
    paths_and_profits = concurrent.futures.ThreadPoolExecutor().map(path_and_profit_graph, powerset(range(len(graph["Profits"]))))
    print(list(paths_and_profits).sort(key=lambda x: x[0]))
