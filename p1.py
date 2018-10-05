"""
PROGRAM 1 CODED BY:

Zack Lawrence
zarlawre@ucsc.edu
1493604

Hui Huang
hhuang66@ucsc.edu  
1596750
"""



import sys
from p1_support import load_level, show_level, save_level_costs
from math import inf, sqrt
from heapq import heappop, heappush




def path_to(start, end, prevList):
    #CREATED BY STUDENT
    """Begins at destination and parses through each previous cell, adding each to a list until it reaches the starting point

    Args: 
        start: initial position
        end: destination
        prevList: A dictionary of found cells and their previous cells
    """
    #go through each previous cell and save it to first entry of list "route"
    route = [end]
    current = end
    while(current != start):
        route.insert(0, prevList[current])
        current = prevList[current]
    return route






def dijkstras_shortest_path(initial_position, destination, graph, adj):
    """ Searches for a minimal cost path through a graph using Dijkstra's algorithm.

    Args:
        initial_position: The initial cell from which the path extends.
        destination: The end location for the path.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        If a path exits, return a list containing all cells from initial_position to destination.
        Otherwise, return None.

    """


    #declare dictionaries and priority queue
    queue = [(0, initial_position)]
    found = {initial_position: 0}    
    previous = {}

    #loop through queue
    while queue:
        current_cost, current_node = heappop(queue)
        if current_node == destination:
            #print('Got eem!')
            return path_to(initial_position, destination, previous)
        else:
            for node, cost in adj(graph, current_node):
                pathcost = cost + current_cost
                if node in found and pathcost >= found[node]:
                    continue
                heappush(queue, (pathcost, node))
                found[node] = pathcost
                previous[node] = current_node
    pass

    adj(graph, initial_position)






def dijkstras_shortest_path_to_all(initial_position, graph, adj):
    """ Calculates the minimum cost to every reachable cell in a graph from the initial_position.

    Args:
        initial_position: The initial cell from which the path extends.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        A dictionary, mapping destination cells to the cost of a path from the initial_position.
    """
    #I'm sure there's probably a more efficient way to do this, but it's Thursday and this'll do.

    #iterate through all cells until every cell that can be found is found with its lowest possible cost
    queue = [(0, initial_position)]
    found = {initial_position: 0}
    while queue:
        current_cost, current_node = heappop(queue)
        for node, cost in adj(graph, current_node):
            pathcost = cost + current_cost
            if node in found and pathcost >= found[node]:
                continue
            heappush(queue, (pathcost, node))
            found[node] = pathcost


    #iterate through every position in graph and add it and its cost to final dictionary
    final = {}
    i = 0
    k = 0
    while (i,k) in graph['spaces'] or (i,k) in graph['walls']:
        while (i,k) in graph['spaces'] or (i,k) in graph['walls']:
            if (i,k) in found:
                final[i,k] = found[i,k]
            else:
                final[i,k] = inf
            i += 1
        k += 1
        i = 0

    return final







def navigation_edges(level, cell):
    """ Provides a list of adjacent cells and their respective costs from the given cell.

    Args:
        level: A loaded level, containing walls, spaces, and waypoints.
        cell: A target location.

    Returns:
        A list of tuples containing an adjacent cell's coordinates and the cost of the edge joining it and the
        originating cell.

        E.g. from (0,0):
            [((0,1), 1),
             ((1,0), 1),
             ((1,1), 1.4142135623730951),
             ... ]
    """

    #loose use of https://stackoverflow.com/questions/1620940/determining-neighbours-of-cell-two-dimensional-list
    adjacent = lambda x, y : [(x2, y2) for x2 in range(x-1, x+2)
                               for y2 in range(y-1, y+2)
                               if ((x != x2 or y != y2) and
                               ((x2,y2) in level['spaces']))]

    #create a list of reachable adjacent cells
    adjCells = adjacent(cell[0], cell[1])

    #pair adjacent cells with their costs in tuples, then create a list of those tuples
    adjFinal = []
    for adjCell in adjCells:
        pair = (adjCell, sqrt(abs(adjCell[0] - cell[0]) + abs(adjCell[1] - cell[1])) * 0.5 * (level['spaces'][adjCell] + level['spaces'][cell]))
        adjFinal.append(pair)
    
    return adjFinal





def test_route(filename, src_waypoint, dst_waypoint, output_filename):
    """ Loads a level, searches for a path between the given waypoints, and displays the result.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        dst_waypoint: The character associated with the destination waypoint.

    """

    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source and destination coordinates from the level.
    src = level['waypoints'][src_waypoint]
    dst = level['waypoints'][dst_waypoint]

    # Search for and display the path from src to dst.
    #haphazardly edited to output to file aswell as stdout
    path = dijkstras_shortest_path(src, dst, level, navigation_edges)
    if path:
        show_level(level, path)
        original_out = sys.stdout
        f = open(output_filename, "w+")
        sys.stdout = f
        show_level(level, path)
        sys.stdout = original_out
        f.close
        print("Saved file:", output_filename)

    else:
        print("No path possible!")


def cost_to_all_cells(filename, src_waypoint, output_filename):
    """ Loads a level, calculates the cost to all reachable cells from 
    src_waypoint, then saves the result in a csv file with name output_filename.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        output_filename: The filename for the output csv file.

    """
    
    # Load and display the level.
    level = load_level(filename)
    #show_level(level)

    # Retrieve the source coordinates from the level.
    src = level['waypoints'][src_waypoint]
    
    # Calculate the cost to all reachable cells from src and save to a csv file.
    costs_to_all_cells = dijkstras_shortest_path_to_all(src, level, navigation_edges)
    save_level_costs(level, costs_to_all_cells, output_filename)


if __name__ == '__main__':
    filename, src_waypoint, dst_waypoint = 'test_maze.txt', 'a','d'

    # Use this function call to find the route between two waypoints.
    test_route(filename, src_waypoint, dst_waypoint, 'test_maze_path.txt')

    # Use this function to calculate the cost to all reachable cells from an origin point.
    cost_to_all_cells(filename, src_waypoint, 'test_maze_costs.csv')
