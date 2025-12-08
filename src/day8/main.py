import dataclasses
from collections import defaultdict, Counter


@dataclasses.dataclass(order=True, eq=True, frozen=True)
class Node:
    x: int
    y: int
    z: int

    def __hash__(self):
        return hash((self.x, self.y, self.z))


def read_junction_map(filename) -> list[Node]:
    with open(filename, "r") as file:
        lines = file.read().split("\n")
    return [Node(*map(int, line.split(","))) for line in lines]


class Cloud:
    def __init__(self, nodes: list[Node]):
        self.nodes = nodes
        self.connections: dict[Node, set[Node]] = defaultdict(set)

    def get_clusters(self):
        # a cluster is a set of nodes we name the cluster with the smaller node in the list
        nodes_to_add: set[Node] = set(self.nodes)
        clusters = {}
        while nodes_to_add:
            node = nodes_to_add.pop()
            reachable_nodes = self.get_reachable_nodes(node)
            sorted_nodes = sorted(reachable_nodes)
            clusters[sorted_nodes[0]] = sorted_nodes
            nodes_to_add = nodes_to_add - reachable_nodes
        return sorted(clusters.values(), key=len, reverse=True)

    def get_reachable_nodes(self, node):
        known_cluster = set()
        queue = {node}  # we start from the current node
        while queue:
            current_node = queue.pop()
            known_cluster.add(current_node)
            reachable_nodes = self.connections.get(current_node, set())
            queue |= reachable_nodes - known_cluster
        return known_cluster

    def add_connection(self, a: Node, b: Node):  # connections are symmetric
        if a == b:
            return
        self.connections[a].add(b)
        self.connections[b].add(a)

    def count_connections(self):
        distinct_connections = set()
        for a, targets in self.connections.items():
            for b in targets:
                key = (min(a, b), max(a, b))
                distinct_connections.add(key)
        return len(distinct_connections)

    def nodes_by_distance(self):
        distances = []
        computed = set()
        for a in self.nodes:
            for b in self.nodes:
                if a != b:
                    key = (min(a, b), max(a, b))
                    if key not in computed:
                        distance = (
                            (a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2
                        ) ** 0.5
                        distances.append((distance, a, b))
                        computed.add(key)
        distances.sort()
        return distances

    def print_cluster_status(self):
        cluster = self.get_clusters()
        cluster_sizes_count = Counter()
        for c in cluster:
            cluster_sizes_count[len(c)] += 1
        print(
            f"{len(self.nodes)} nodes - {self.count_connections()} connections - {len(cluster)} clusters (sizes: {dict(cluster_sizes_count)})"
        )

    def multiply_cluster_sizes(self, top_most: int | None = None):
        result = 1
        clusters = self.get_clusters()
        if top_most is not None:
            clusters = clusters[:top_most]

        for cluster in clusters:
            result *= len(cluster)
        return result

    def add_connections(self, stop_after, top_most) -> tuple[Node, Node] | None:
        connections_added = 0
        for _, a, b in self.nodes_by_distance():
            # if two nodes are already in the same cluster, connect them anyway

            # same_cluster = False
            # clusters = self.get_clusters()
            # for cluster in clusters:
            #     if a in cluster and b in cluster:
            #         print(f"skipping same cluster {a} <-> {b}")
            #         same_cluster = True

            # print(f"connecting {a} <-> {b}")
            self.add_connection(a, b)
            connections_added += 1
            if stop_after is not None:
                if connections_added >= stop_after:
                    break  # part 1 stop condition
            else:  # part 2 - continue until we have 1 single cluster
                clusters = self.get_clusters()
                if len(clusters) == 1:
                    return a, b


def get_cluster_sum(
    filename: str, stop_after: int | None = None, top_most: int | None = None
) -> int:
    nodes = read_junction_map(filename)
    cloud = Cloud(nodes)
    connection = cloud.add_connections(stop_after, top_most)

    cloud.print_cluster_status()
    if connection is not None:  # part 2 output
        a, b = connection
        return a.x * b.x
    return cloud.multiply_cluster_sizes(top_most=top_most)


if __name__ == "__main__":
    assert get_cluster_sum("sample.txt", 10, top_most=3) == 40
    print("Part 1:", get_cluster_sum("input.txt", 1000, top_most=3))

    assert get_cluster_sum("sample.txt", None) == 25272
    print("Part 2:", get_cluster_sum("input.txt", None))
