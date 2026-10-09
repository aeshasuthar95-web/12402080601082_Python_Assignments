# ---------------------------------------------------------
# Assignment 1 - Q6
# Python Module Dependency Resolver
# ---------------------------------------------------------

import heapq


def main():

    # n = number of modules
    # e = number of dependency edges
    n, e = map(int, input().split())

    modules = []

    # Store all module names
    for _ in range(n):
        modules.append(input().strip())

    # adjacency[a] contains modules that depend on a
    adjacency = {
        module: [] for module in modules
    }

    # indegree[module] = number of dependencies
    indegree = {
        module: 0 for module in modules
    }

    # -----------------------------------------------------
    # Read dependency relationships
    # -----------------------------------------------------

    seen_edges = set()

    for _ in range(e):

        module_a, module_b = input().split()

        # module_a imports module_b
        # Therefore module_b must be loaded before module_a.

        edge = (module_b, module_a)

        # Ignore duplicate edges
        if edge in seen_edges:
            continue

        seen_edges.add(edge)

        adjacency[module_b].append(module_a)
        indegree[module_a] += 1

    # -----------------------------------------------------
    # Min-heap ensures lexicographically smallest module
    # is always selected first.
    # -----------------------------------------------------

    heap = []

    for module in modules:
        if indegree[module] == 0:
            heapq.heappush(heap, module)

    order = []

    # -----------------------------------------------------
    # Kahn's topological sorting algorithm
    # -----------------------------------------------------

    while heap:

        current = heapq.heappop(heap)

        order.append(current)

        for dependent in adjacency[current]:

            indegree[dependent] -= 1

            if indegree[dependent] == 0:
                heapq.heappush(heap, dependent)

    # -----------------------------------------------------
    # If not all modules were processed,
    # a cycle exists.
    # -----------------------------------------------------

    if len(order) != n:

        print("CYCLE")

        # Find one cycle using DFS
        state = {module: 0 for module in modules}
        parent = {}

        cycle = []

        def dfs(node):

            state[node] = 1

            for next_node in adjacency[node]:

                if state[next_node] == 0:

                    parent[next_node] = node

                    if dfs(next_node):
                        return True

                elif state[next_node] == 1:

                    # Back edge -> cycle found
                    cycle_start = next_node
                    cycle.append(cycle_start)

                    current = node

                    while current != cycle_start:
                        cycle.append(current)
                        current = parent[current]

                    cycle.append(cycle_start)

                    cycle.reverse()

                    return True

            state[node] = 2
            return False

        for module in modules:

            if state[module] == 0:

                if dfs(module):
                    break

        print(" ".join(cycle))

    else:

        print(" ".join(order))


if __name__ == "__main__":
    main()