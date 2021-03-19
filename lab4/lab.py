#!/usr/bin/env python3

from util import read_osm_data, great_circle_distance, to_local_kml_url
import time
# NO ADDITIONAL IMPORTS!


ALLOWED_HIGHWAY_TYPES = {
    'motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'unclassified',
    'residential', 'living_street', 'motorway_link', 'trunk_link',
    'primary_link', 'secondary_link', 'tertiary_link',
}


DEFAULT_SPEED_LIMIT_MPH = {
    'motorway': 60,
    'trunk': 45,
    'primary': 35,
    'secondary': 30,
    'residential': 25,
    'tertiary': 25,
    'unclassified': 25,
    'living_street': 10,
    'motorway_link': 30,
    'trunk_link': 30,
    'primary_link': 30,
    'secondary_link': 30,
    'tertiary_link': 25,
}

start_time = time.perf_counter()
def build_auxiliary_structures(nodes_filename, ways_filename):
    """
    Create any auxiliary structures you are interested in, by reading the data
    from the given filenames (using read_osm_data)
    
    Returns a tuple consisting of a dictionary of nodes and a dictionary of ways
    nodes_db has keys of ids and values of (lat, lon, {tags})
    ways_db has keys of ids and values of ([List of Nodes], {tags})
    """

    ways = read_osm_data(ways_filename)
    nodes = read_osm_data(nodes_filename)
    ways_db = {}
    nodes_db = {}

    for node in nodes: #Initializes dictionary of nodes with empty neighbor set
        nodes_db[node['id']] = (node['lat'],node['lon'],node['tags'],set())
    
    for way in ways:
        if 'highway' in way['tags']:            
            if way['tags']['highway'] in ALLOWED_HIGHWAY_TYPES:
                ways_db[way['id']] = (set(way['nodes']),way['tags']) #Initializes ways dictionary
                
                for i in range(len(way['nodes'])-1): #Forward neighbors case
                    node = way['nodes'][i]
                    neighbor_node = way['nodes'][i+1]
                    update_node_neighbors(nodes_db,node,neighbor_node)
                if 'oneway' in way['tags']: #Backwards neighbors case
                    if way['tags']['oneway'] == 'no':
                        for i in range(len(way['nodes'])-1,0,-1):
                            node = way['nodes'][i]
                            neighbor_node = way['nodes'][i-1]
                            update_node_neighbors(nodes_db,node,neighbor_node)
                else: #In the case the tags does not include oneway, we assume it is bidirectional
                    for i in range(len(way['nodes'])-1,0,-1):
                            node = way['nodes'][i]
                            neighbor_node = way['nodes'][i-1]
                            update_node_neighbors(nodes_db,node,neighbor_node)

    return (nodes_db,ways_db)
#Helper Functions
def update_node_neighbors(nodes_db,node1,node2):
    """ 
    Updates the neighbors of node1 with node2
    """
    set_of_neighbors = nodes_db[node1][3]
    set_of_neighbors.add(node2)
    position_data = [nodes_db[node1][0],nodes_db[node1][1],nodes_db[node1][2]]
    position_data.append(set_of_neighbors)
    nodes_db[node1] = tuple(position_data)
    
def get_distance(node_db,node1, node2):
    ''' 
    Returns the distance in miles between two Node ids
    '''
    lat1 = node_db[node1][0]
    lon1 = node_db[node1][1]
    lat2 = node_db[node2][0]
    lon2 = node_db[node2][1]
    return great_circle_distance((lat1,lon1),(lat2,lon2))
    
def get_cost_and_path(nodes_db,starting_node,node2,old_cost,path_to_consider,agenda,visited):
    """ 
    Updates the agenda with the cost and paths of the children vertices that are not in visited
    Agenda Entries are (Cost,[Path List])
    """
    visited.add(starting_node)
    neighbors_to_consider = list(nodes_db[starting_node][3])
    for neighbor in neighbors_to_consider:
        cost = old_cost + get_distance(nodes_db,starting_node,neighbor)
        new_path = path_to_consider+[neighbor]
        agenda.append((cost,new_path))
    return(agenda,visited)

def get_nearest_node(nodes_db,lat,lon):
    """ 
    Returns the nearest node that is in a relevant way
    
    Parameters:
        nodes_db: A node database which should be the first element when calling build_auxiliary_database on a database
        lat: a latitude coordinate
        lon: a longitude coordinate
    Returns:
        a node's ID that is the closest to the specified coordinate
    """
    min_dist = -1
    key_min = 1
    for node in nodes_db:
        lat1 = nodes_db[node][0]
        lon1 = nodes_db[node][1]
        dist = great_circle_distance((lat1,lon1),(lat,lon))
        # print('node outside:',node)
        # print('distance outside:',dist)
        if dist<min_dist or min_dist == -1:
           # print('node:',node)
            #print('distance:',dist)
            if dist == 0:
                for node2 in nodes_db:
                    if node in nodes_db[node2][3]:
                        min_dist = dist
                        key_min = node
            elif nodes_db[node][3] != set():
                min_dist = dist
                key_min = node
    return key_min

def get_coordinates(nodes_db,node_id):
    lat = nodes_db[node_id][0]
    lon = nodes_db[node_id][1]
    return (lat,lon)
def heuristic(key,goal,nodes_db):
    cost = key[0]
    path_list = key[1]
    last_node = path_list[-1]
    return cost+get_distance(nodes_db,last_node,goal)
#End of Helper Functions
def find_short_path_nodes(aux_structures, node1, node2):
    """
    Return the shortest path between the two nodes

    Parameters:
        aux_structures: the result of calling build_auxiliary_structures
        node1: node representing the start location
        node2: node representing the end location

    Returns:
        a list of node IDs representing the shortest path (in terms of
        distance) from node1 to node2
    """
    nodes_db = aux_structures[0]
    ways_db = aux_structures[1]
    agenda = []
    visited = set()
    
    if node1==node2:
        return [node1]
    agenda,visited = get_cost_and_path(nodes_db,node1,node2,0,[node1],agenda,visited)
    i = 0
    print(i)
    while True:
        #print('Time per loop:',time.perf_counter()-start_time)
        agenda.sort()
        #agenda.sort(key = lambda x: heuristic(x,node2,nodes_db))
        if agenda == []:
            return None
        old_cost,path_to_consider = agenda.pop(0)
        i+=1
        last_node = path_to_consider[-1]
        if last_node == node2:
            print(i)
            return path_to_consider
        elif last_node not in visited:
            agenda,visited = get_cost_and_path(nodes_db,last_node,node2,old_cost,path_to_consider,agenda,visited)
    

def find_short_path(aux_structures, loc1, loc2):
    """
    Return the shortest path between the two locations

    Parameters:
        aux_structures: the result of calling build_auxiliary_structures
        loc1: tuple of 2 floats: (latitude, longitude), representing the start
              location
        loc2: tuple of 2 floats: (latitude, longitude), representing the end
              location

    Returns:
        a list of (latitude, longitude) tuples representing the shortest path
        (in terms of distance) from loc1 to loc2.
    """
    
    print('Time before nearest node:',time.perf_counter()-start_time)
    nodes_db = aux_structures[0]
    ways_db = aux_structures[1]
    #print(nodes_db)
    node1 = get_nearest_node(nodes_db,*loc1)
    print('Nearest Node 1:',time.perf_counter()-start_time)
    #print('node1:',node1)
    node2 = get_nearest_node(nodes_db,*loc2)
    print('Nearest Node 2:',time.perf_counter()-start_time)
    #print('node2:',node2)
    if node1 == node2:
        return [get_coordinates(nodes_db,node1)]
    path = find_short_path_nodes(aux_structures,node1,node2)
    #print(path)
    if path==None or len(path)==1:
        return None
    result = [get_coordinates(nodes_db,node_id) for node_id in path]
    return result

def find_fast_path(aux_structures, loc1, loc2):
    """
    Return the shortest path between the two locations, in terms of expected
    time (taking into account speed limits).

    Parameters:
        aux_structures: the result of calling build_auxiliary_structures
        loc1: tuple of 2 floats: (latitude, longitude), representing the start
              location
        loc2: tuple of 2 floats: (latitude, longitude), representing the end
              location

    Returns:
        a list of (latitude, longitude) tuples representing the shortest path
        (in terms of time) from loc1 to loc2.
    """
    raise NotImplementedError


if __name__ == '__main__':
    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    # nodes = read_osm_data('resources/cambridge.nodes')
    '''2'''
    # cambridge_nodes,cambridge_ways = build_auxiliary_structures('resources/cambridge.nodes','resources/cambridge.ways')

    # for node in cambridge_nodes:
    #     if 'name' in cambridge_nodes[node][2]:
    #         if cambridge_nodes[node][2]['name'] == '77 Massachusetts Ave':
    #             print('Question 2.1.3:',node)
    
    # ways = read_osm_data('resources/cambridge.ways')
    # for way in ways:
    #     if 'oneway' in way['tags']:
    #         if way['tags']['oneway'] == 'yes':
    #             i+=1
    # print(i)
    
    '''3''' 
    #midwest_nodes,midwest_ways = build_auxiliary_structures('resources/midwest.nodes','resources/midwest.ways')

    # print('Question 3.1.3.1:', great_circle_distance((42.363745, -71.100999),(42.361283,-71.239677)))

    # id_1 = 233941454
    # id_2 = 233947199
    # print('Question 3.1.3.2:', get_distance(id_1,id_2))
    
    # list_of_nodes = midwest_ways[21705939][0]
    # dist = 0
    # for i in range(len(list_of_nodes)-1):
    #     id_1 = list_of_nodes[i]
    #     id_2 = list_of_nodes[i+1]
    #     dist += get_distance(id_1,id_2)
    # print('Question 3.1.3.3:',dist)
    
    '''4'''
    # mit_nodes,mit_ways = build_auxiliary_structures('resources/mit.nodes','resources/mit.ways')
    # print(mit_ways)
    # midwest_nodes,midwest_ways = build_auxiliary_structures('resources/midwest.nodes','resources/midwest.ways')
    # lat = 41.4452463
    # lon = -89.3161394
    # loc = (lat,lon)
    # print(get_nearest_node(midwest_nodes,*loc))
    '''5'''
    #start_time = time.perf_counter()
    cambridge_nodes,cambridge_ways = build_auxiliary_structures('resources/cambridge.nodes','resources/cambridge.ways')
    loc1 = (42.3858, -71.0783)
    loc2 = (42.5465, -71.1787)
    find_short_path((cambridge_nodes,cambridge_ways),loc1,loc2)
    print('Time so far:',time.perf_counter()-start_time)
    #No Heuristic popped 688127 paths
    #Heustic popped 85578 paths
    # duration = time.perf_counter()-start_time
    # print('it took:',duration)
    '''Testing stuff '''
    #print(find_short_path_nodes((midwest_nodes,midwest_ways),272855431, 233945564))
    
    # for way in midwest_ways:
    #     if 234022411 in midwest_ways[way][0] or 272856928 in midwest_ways[way][0]:
    #         print("way:",midwest_ways[way])
    # print(len(midwest_nodes))
    # print(midwest_nodes[id_1])
    # mit_nodes,mit_ways = build_auxiliary_structures('resources/mit.nodes','resources/mit.ways')
    # print(mit_nodes)
    # node1 = 7 # near Building 35
    # node2 = 3 # Near South Maseeh
    # expected_path = [7, 5, 10, 3]
    # #print(mit_ways)
    # print(find_short_path_nodes((mit_nodes,mit_ways),node1,node2))
    #compare_result_expected(load_dataset('mit'), (node1, node2), expected_path, 'short', True)
    # loc1 = (42.3575, -71.0956) # Parking Lot - end of a oneway and not on any other way
    # loc2 = (42.3575, -71.0940) #close to Kresge
    # print(get_nearest_node(mit_nodes,*loc1))
    pass
