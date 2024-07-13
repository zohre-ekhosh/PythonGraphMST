import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.community import girvan_newman
from concurrent.futures import ThreadPoolExecutor
import itertools
import pandas as pd
import time
import numpy as np


# Function to calculate MST for a subgraph
def calculate_mst(subgraph):
    return nx.minimum_spanning_tree(subgraph, algorithm='prim')
    

# Function to calculate MST for the whole graph
def calculate_mst_1(G): 
    return calculate_mst(G), None


# Function to calculate MSTs for clusters and merge them
def calculate_mst_2(G):
    # Clustering by method girvan_newman
    clusters_girvan_newman = girvan_newman(G)

    # Extract clusters from the algorithm result
    clusters = tuple(sorted(c) for c in next(clusters_girvan_newman))
    
    # Calculate the mst of clusters in parallel
    with ThreadPoolExecutor() as executor:
        msts = list(executor.map(lambda c: calculate_mst(G.subgraph(c)), clusters))

    # Create a new graph to merge MSTs
    merged_graph = nx.Graph()
    for mst in msts:
        merged_graph.add_edges_from(mst.edges(data=True))  # data=True : Each edge is returned exactly as a tuple (u, v, d)

    #Find the minimum edge between each pair of clusters and add it to the merged graph
    for clus, clus2 in itertools.combinations(clusters, 2):  #itertools.combinations(clusters, 2) : All possible pairs of clusters(list)
        # Convert clusters(list) to sets to use | operator
        clus = set(clus)
        clus2 = set(clus2)
        
        min_edges = nx.minimum_spanning_edges(G.subgraph(clus | clus2), weight='weight', data=True)
        for u, v, d in min_edges:
            merged_graph.add_edge(u, v, **d)


    return merged_graph, clusters


# Function to visualize the graph and its MST
def visualize_graph(G, mst, layout, ax, title, clusters=None):
    ax.set_title(title)

    # Draw nodes with different colors for each clusters
    if clusters:
        colors = plt.cm.rainbow(np.linspace(0, 1, len(clusters)))
        for color, community in zip(colors, clusters):
            nx.draw_networkx_nodes(G, layout, nodelist=community, node_color=[color], node_size=500, ax=ax)
    else:
        nx.draw_networkx_nodes(G, layout, node_color="lightblue", node_size=500, ax=ax)
    
    nx.draw_networkx_edges(G, layout, edge_color="grey", ax=ax)
    nx.draw_networkx_labels(G, layout, font_size=12, font_family="sans-serif", ax=ax)
    nx.draw_networkx_edge_labels(
        G, layout, edge_labels={(u, v): d["weight"] for u, v, d in G.edges(data=True)}, ax=ax
    )
    nx.draw_networkx_edges(mst, layout, edge_color="green", width=2, ax=ax)
    ax.axis("off")


# Function to calculate and print MST results
def result(operation, num, G):
    start_time = time.time()      #time.time() : Calculate time
    mst, clusters = operation(G)
    end_time = time.time()

    print(f"Minimum Spanning Tree {num} cost: {mst.size(weight='weight')}")   #mst.size : Calculate cost
    print(f"Execution time {num} : {end_time - start_time} seconds\n")

    return mst, clusters




# Reading the CSV file
df = pd.read_csv('E:/zohreh/daneshgah/algorithmProject/soc-sign-bitcoinalpha.csv/graph3.csv', header=None)

# Selecting the first three columns (source, target, weight)
edges = df.iloc[:, :3].values.tolist()

# Creating the graph from the file
G = nx.Graph()
G.add_weighted_edges_from(edges)


# Calculate MSTs using two methods
mst_1, _ = result(calculate_mst_1, 1, G)
mst_2, clusters_2 = result(calculate_mst_2, 2, G)


# show graphs
layout = nx.spring_layout(G)   # Create the layout
# Create two subplots to display the MSTs side by side
fig, axs = plt.subplots(1, 2, figsize=(15, 7))
visualize_graph(G, mst_1, layout, axs[0], 'MST 1')
visualize_graph(G, mst_2, layout, axs[1], 'MST 2', clusters_2)
plt.show()
