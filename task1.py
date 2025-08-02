import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate  

def create_graph():
    G = nx.DiGraph()
    edges = [
        ('T1', 'S1', 25), ('T1', 'S2', 20), ('T1', 'S3', 15),
        ('T2', 'S3', 15), ('T2', 'S4', 30), ('T2', 'S2', 10),
        ('S1', 'M1', 15), ('S1', 'M2', 10), ('S1', 'M3', 20),
        ('S2', 'M4', 15), ('S2', 'M5', 10), ('S2', 'M6', 25),
        ('S3', 'M7', 20), ('S3', 'M8', 15), ('S3', 'M9', 10),
        ('S4', 'M10', 20), ('S4', 'M11', 10), ('S4', 'M12', 15),
        ('S4', 'M13', 5), ('S4', 'M14', 10)
    ]
    for u, v, capacity in edges:
        G.add_edge(u, v, capacity=capacity)
    return G

def compute_max_flow(G, source, sink):
    return nx.maximum_flow(G, source, sink)

def analyze_results(flow_dict):
    result = []
    for source, destinations in flow_dict.items():
        for dest, flow in destinations.items():
            if flow > 0:
                result.append([source, dest, flow])
    return pd.DataFrame(result, columns=['Термінал/Склад', 'Магазин', 'Фактичний потік'])

def visualize_graph(G):
    pos = nx.spring_layout(G, seed=42)
    labels = nx.get_edge_attributes(G, 'capacity')
    plt.figure(figsize=(12, 7))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=1200, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.title("Логістична мережа")
    plt.savefig("logistics_network.png")
    plt.show()

if __name__ == "__main__":
    G = create_graph()

    G.add_edge('Source', 'T1', capacity=100)
    G.add_edge('Source', 'T2', capacity=100)
    for i in range(1, 15):
        G.add_edge(f'M{i}', 'Sink', capacity=100)

    max_flow_value, flow_dict = compute_max_flow(G, 'Source', 'Sink')

    df_results = analyze_results(flow_dict)

    print(tabulate(df_results, headers='keys', tablefmt='pretty'))

    df_results.to_csv("logistics_flow_results.csv", index=False)
    print("Результати збережені в logistics_flow_results.csv")

    visualize_graph(G)

    print(f"\nМаксимальный потік: {max_flow_value}")
