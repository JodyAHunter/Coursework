def solve_tsp(G):
    """Function that solves the travelling salesperson problem using the
    nearest-neighbor heuristic."""

    # inf is a arbitrarily high value used to find min values between 2 vertices
    inf = 9999999
    # number of vertices in the graph
    vertices = len(G)
    # array that shows true or false depending on if a node has been visited
    visited = [False] * vertices
    # Index 0 is our starting vertex, mark as visited
    visited[0] = True
    # Array that will hold the path of vertices taken to solve TSP, start with index 0
    path = [0]
    # Current vertex initialized as 0 for starting vertex
    current_vertex = 0

    # While loop to build path taken to solve TSP
    while len(path) < vertices:

        # Start minimum value as our arbitrarily high number
        minimum = inf

        # next vertex to be visited starts as None
        next_vertex = None

        # For loop to find the minimum value of all neighboring cities for each vertex
        for city in range(vertices):
            # check if a city has been visited and has an edge, compare it to the current minimum
            if not visited[city] and G[current_vertex][city] < minimum and G[current_vertex][city] > 0:
                minimum = G[current_vertex][city]
                next_vertex = city

        # Mark next city found as visited and add it to path, make it current vertex
        if next_vertex is not None:
            visited[next_vertex] = True
            path.append(next_vertex)
            current_vertex = next_vertex

    # After all vertices have been visited, we go back to the starting vertex
    path.append(0)
    return path
