# PythonGraphMST
Calculate Minimum Spanning Tree (MST) of a graph using two methods: Prim's algorithm and clustering-based MST calculation.

General Description:
This Python script reads a CSV file containing graph data, constructs the graph, and calculates the Minimum Spanning Tree (MST) using two different methods. It then shows the cost of the MST and the execution time of the two methods, and finally, it displays the graph and the MST.

Libraries Used:
NetworkX: For graph operations
Matplotlib: For visualization
ThreadPoolExecutor: For parallel execution
Pandas: For data manipulation
NumPy: For numerical operations
itertools: For various combinations

Functions:
subgraph_mst_calculate(subgraph): Computes the MST for a subgraph using NetworkX's Prim algorithm.
mst_calculate_1(G): Computes the MST for the entire graph.
mst_calculate_2(G): Splits the graph into clusters using the Newman-Girvan algorithm, computes the MST for each cluster in parallel using ThreadPoolExecutor, merges these MSTs, and adds the minimum edges between clusters to create an overall MST for the graph.
visualize_graph(G, mst, layout, ax, title, clusters=None): Displays the graph, the MST, and clusters using Matplotlib.
result(operation, G, num): Performs the MST calculation operation on graph G according to the input function, and announces the MST cost and execution time of the algorithm.

General Steps of the Script:
Data Reading and Processing: The data is initially read from a CSV file. Our file contains information in four columns (source, target, weight, and time), but we only use the first three columns (source, target, edge weight).
Graph Construction: Using NetworkX, a weighted graph is constructed from the read data.
MST Calculation with Two Functions: Using the functions mst_calculate_1(G) and mst_calculate_2(G).
Announcing MST Cost and Execution Time: The cost of the MST and the execution time of the algorithm are announced for both functions.
Overall Graph and MST Display: The entire graph and the MST (in green edges) are displayed for both methods. Additionally, clusters identified in the second method are shown in the 2MST display.
