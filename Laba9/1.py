import networkx as nx
import matplotlib.pyplot as plt

def is_bipartite(graph):
    try:
        color = nx.bipartite.color(graph)
        return True, color
    except nx.NetworkXError:
        return False, None

def ford_fulkerson_matching(graph : nx.Graph, left, right):
    flow_network = nx.DiGraph()

    source = 'source'
    sink = 'sink'
    flow_network.add_node(source)
    flow_network.add_node(sink)

    for node in left:
        flow_network.add_edge(source, node, capacity=1)

    for node in right:
        flow_network.add_edge(node, sink, capacity=1)

    for u, v in graph.edges():
        if u in left and v in right:
            flow_network.add_edge(u, v, capacity=1)
        elif v in left and u in right:
            flow_network.add_edge(v, u, capacity=1)

    flow_value, flow_dict = nx.maximum_flow(flow_network, source, sink)

    matching = []
    for u in flow_dict:
        if u == source or u == sink:
            continue
        for v in flow_dict[u]:
            if v != sink and flow_dict[u][v] == 1:
                matching.append((u, v))

    return matching

def kun_matching(graph, left, right):
    pair_U = {u: None for u in left}
    pair_V = {v: None for v in right}

    def dfs(u, visited):
        for v in graph.neighbors(u):
            if v not in visited:
                visited.add(v)
                if pair_V[v] is None or dfs(pair_V[v], visited):
                    pair_U[u] = v
                    pair_V[v] = u
                    return True
        return False

    for u in left:
        dfs(u, set())
    matching = [(u, v) for u, v in pair_U.items() if v is not None]
    return matching

def visualize_graph(graph, left, right, matching, title):
    plt.figure(figsize=(10, 8))
    pos = {}
    left_nodes = sorted(left)
    right_nodes = sorted(right)

    for i, node in enumerate(left_nodes):
        pos[node] = (0, -i)

    for i, node in enumerate(right_nodes):
        pos[node] = (1, -i)

    nx.draw_networkx_nodes(graph, pos, nodelist=left, node_color='red', node_size=400)
    nx.draw_networkx_nodes(graph, pos, nodelist=right, node_color='lightblue', node_size=400)
    nx.draw_networkx_edges(graph, pos, edge_color='gray', width=1)
    nx.draw_networkx_edges(graph, pos, edgelist=matching, edge_color='green', width=2)
    nx.draw_networkx_labels(graph, pos)

    plt.title(title)
    plt.axis('off')
    plt.show()

def main():
    edges = [(4, 13), (9, 11), (5, 8), (11, 14), (2, 9), (6, 13), (3, 10), (2, 10), (5, 12), (5, 6), (10, 13), (7, 11), (13, 15),
                       (9, 13), (5, 14), (4, 5), (3, 9), (6, 11), (2, 4), (5, 15), (2, 8), (3, 12), (11, 12), (4, 11), (11, 15), (3, 4), (13, 14), (5, 10), (2, 15), (3, 16), (2, 7), (3, 15), (5, 7), (10, 11), (3, 14)]
    nodes = [i for i in range(1,17)]

    G = nx.Graph()
    G.add_edges_from(edges)
    G.add_nodes_from(nodes)

    bipartite, coloring = is_bipartite(G)
    print(f"Граф двудольный: {bipartite}")


    if not bipartite:
        cycles = list(nx.cycle_basis(G))
        edges_to_remove = set()
        for cycle in cycles:
            if len(cycle) % 2 != 0:
                edges_to_remove.add((cycle[0], cycle[1]))
        print(f"Удаляем рёбра: {edges_to_remove}")
        G.remove_edges_from(edges_to_remove)
        bipartite, coloring = is_bipartite(G)
        print(f"После удаления рёбер граф двудольный: {bipartite}")

    if bipartite:
        right = {node for node in coloring if coloring[node] == 0}
        left = set(G.nodes()) - right
        print(f"Вершины слева: {left}")
        print(f"Вершины справа: {right}")
    else:
        print("Не удалось сделать граф двудольным")
        exit()

    ff_matching = ford_fulkerson_matching(G, left, right)
    k_matching = kun_matching(G, left, right)

    print(f"Наибольшее паросочетание по алгоритму Форда-Фалкерсона: {ff_matching}")
    print(f"Наибольшее паросочетание по алгоритму Куна: {k_matching}")

    visualize_graph(G, left, right, ff_matching, "Наибольшее паросочетание по алгоритму Форда-Фалкерсона")
    visualize_graph(G, left, right, k_matching, "Наибольшее паросочетание по алгоритму Куна")

if __name__ == "__main__":
    main()


# G(V,E) - граф: V - вершины, E - ребра
# Контрольные вопросы:
# 1)Какой граф называется двудольным?
# Граф W называется двудольным, если множество его вершин можно разбить на две части U ∪ V = W так что:
#  Ни одна вершина в U не соединена с вершинами в U.
#  Ни одна вершина в V не соединена с вершинами в V.
#
# 2) Определение паросочетания:
# Паросочетание M в графе G — это множество попарно несмежных рёбер, то есть рёбер, не имеющих общих вершин
#
# 3) 3 алгоритма поиска паросочетаний и их свойства в сравнении.
# 1.
# Алгоритм: Куна
# Тип графа: Двудольный
# Сложность: O(VE)
# Прост в реализации, использует обход в глубину (DFS).
#
# 2.
# Алгоритм: Форда-Фалкерсона
# Тип графа: Двудольный
# Сложность: O(Ef)
# сводит к задаче о максимальном потоке (f — величина потока).
#
# 3.
# Алгоритм: Эдмондса
# Тип графа: Произвольный
# Сложность: O(V**3)
# Работает на любых графах, но сложен в реализации.