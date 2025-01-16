def Prims(G):
    """This function implements Prim's algorithm to form a minimum spanning tree
    from a given graph G.
    Input: a graph represented as an adjacency matrix
    Output: a list of tuples, wherein each tuple represents an edge of the MST
    as (v1, v2, weight)"""

    # INF represents an arbitrarily high number
    INF = 9999999

    # V represents the number of vertices in the graph G
    V = len(G)

    # selected array of booleans to represent if a vertex is chosen for MST
    selected = [False] * V

    # edge counter for the MST
    edge_number = 0

    # 0th vertex will be selected to start the MST with
    selected[0] = True

    # output array to hold and return the expected values from function
    output = []

    # While loop that runs until edge_number is equal to total vertices of graph
    while edge_number < (V - 1):

        # minimum is set to arbitrarily high value to begin each iteration
        minimum = INF
        # x value of adjacency matrix
        x = 0
        # y value of adjacency matrix
        y = 0
        for i in range(V):
            if selected[i]:
                # Below code section is ran if i-th vertex has been selected
                for j in range(V):
                    # Checking each adjacent vertex and the weight of the edges
                    if not selected[j] and G[i][j]:
                        # Update minimum if value at [i][j] is < current minimum
                        if minimum > G[i][j]:
                            minimum = G[i][j]
                            x = i
                            y = j
        # Update output after all adjacent vertices have been checked for i-th
        # vertex, in the form of vertex 1, vertex 2, edge value
        output.append((x, y, G[x][y]))
        # Mark y vertex as visited
        selected[y] = True
        # Increment edge number
        edge_number += 1

    return output

