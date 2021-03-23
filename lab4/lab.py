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
    nodes_db has keys of ids and values of another dictionary containing {coordinates,neighbors,cost,heuristic}
    """

    ways = read_osm_data(ways_filename)
    nodes = read_osm_data(nodes_filename)
    nodes_db = {}

    for way in ways:
        if 'highway' in way['tags']:   
            highway_type = way['tags']['highway']        
            if highway_type in ALLOWED_HIGHWAY_TYPES:
                """ Adds neighbors and creates the key for each relevant id (eliminates disconected nodes) """
                num_nodes_in_way = len(way['nodes'])
                if 'maxspeed_mph' in way['tags']:
                    speed = way['tags']['maxspeed_mph']
                else:
                    speed = DEFAULT_SPEED_LIMIT_MPH[highway_type]
                for i in range(num_nodes_in_way-1): #Forward neighbors case
                    node = way['nodes'][i]
                    neighbor_node = way['nodes'][i+1]
                    update_node_neighbors(nodes_db,node,neighbor_node,speed)
                    if i == num_nodes_in_way-2: #Adds the last neighbor as a relevant node
                        if neighbor_node not in nodes_db:
                            node_dict = {'neighbors':set()}
                            nodes_db[neighbor_node] = node_dict
                
                if 'oneway' in way['tags']: #Backwards neighbors case
                    if way['tags']['oneway'] == 'no':
                        for i in range(num_nodes_in_way-1,0,-1):
                            node = way['nodes'][i]
                            neighbor_node = way['nodes'][i-1]
                            update_node_neighbors(nodes_db,node,neighbor_node,speed)
                            
                else: #In the case the tags does not include oneway, we assume it is bidirectional
                    for i in range(num_nodes_in_way-1,0,-1):
                            node = way['nodes'][i]
                            neighbor_node = way['nodes'][i-1]
                            update_node_neighbors(nodes_db,node,neighbor_node,speed)
    
    for node in nodes: #Initializes dictionary of nodes with empty neighbor set
        """ Gets the coordinates, don't need node tags, adds a cost and heuristic key"""
        node_id = node['id']
        if node_id in nodes_db:
            nodes_db[node_id]['coordinates'] = (node['lat'],node['lon'])
            nodes_db[node_id]['cost'] = 0.0
            nodes_db[node_id]['heuristic'] = 0.0
    return nodes_db

def get_distance(node_db,node1, node2):
    ''' 
    Returns the distance in miles between two Node ids
    '''
    coord1 = node_db[node1]['coordinates']
    coord2 = node_db[node2]['coordinates']
    return great_circle_distance(coord1,coord2)
#Helper Functions
def update_node_neighbors(node_db,node, neighbor_node,speed):
    """ Adds neighbors to the neighbor set in each node id"""
    if node not in node_db:
        neighbor_set = {(neighbor_node,speed)}
        node_dict = {'neighbors':neighbor_set}
        node_db[node] = node_dict
    else:  
        node_db[node]['neighbors'].add((neighbor_node,speed))
        
def get_cost_and_path(nodes_db,starting_node,node2,old_cost,path_to_consider,agenda,visited,fast=False):
    """ 
    Updates the agenda with the cost and paths of the children vertices that are not in visited
    Agenda Entries are (Cost,[Path List])
    """
    visited.add(starting_node)
    neighbors_to_consider = nodes_db[starting_node]['neighbors']
    for neighbor in neighbors_to_consider:
        neighbor_id = neighbor[0]
        # heuristic = get_distance(nodes_db,neighbor_id,node2)
        # nodes_db[neighbor_id]['heuristic'] = heuristic
        if not fast: #Cost is distance
            cost = old_cost + get_distance(nodes_db,starting_node,neighbor_id)
        else: #Cost is time
            cost = old_cost + (get_distance(nodes_db,starting_node,neighbor_id)/neighbor[1])
        new_path = path_to_consider+[neighbor_id]
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
    key_min = min(nodes_db,key = lambda x: great_circle_distance(nodes_db[x]['coordinates'],(lat,lon)))
    return key_min
#End of Helper Functions

def find_short_path_nodes(aux_structures, node1, node2, fast = False):
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
    nodes_db = aux_structures
    agenda = []
    visited = set()
    if node1 not in nodes_db or node2 not in nodes_db: #Checks if nodes in database
        return None
    elif node1==node2: #Start and end are same location
        return [node1]
    agenda,visited = get_cost_and_path(nodes_db,node1,node2,0,[node1],agenda,visited,fast) #First run updating agenda and visited with initial nodes
    if agenda == []: #No paths found
        return None
    while True: #Bread first search that iterates until goal node is found
        agenda.sort()
        old_cost,path_to_consider = agenda.pop(0)
        last_node = path_to_consider[-1]
        if last_node == node2:
            return path_to_consider
        elif last_node not in visited:
            agenda,visited = get_cost_and_path(nodes_db,last_node,node2,old_cost,path_to_consider,agenda,visited,fast)  
            
def find_short_path(aux_structures, loc1, loc2,fast=False):
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
    nodes_db = aux_structures
    node1 = get_nearest_node(nodes_db,*loc1) #Finds node locations
    node2 = get_nearest_node(nodes_db,*loc2)
    if node1 == node2: #Checks for same location
        return [nodes_db[node1]['coordinates']]
    path = find_short_path_nodes(aux_structures,node1,node2,fast) 
    if path==None or len(path)==1:
        return None
    result = [nodes_db[node_id]['coordinates'] for node_id in path]
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
    return find_short_path(aux_structures,loc1,loc2,fast=True)

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
    # mit_nodes = build_auxiliary_structures('resources/mit.nodes','resources/mit.ways')
    # print(mit_nodes)
    # midwest_nodes,midwest_ways = build_auxiliary_structures('resources/midwest.nodes','resources/midwest.ways')
    # lat = 41.4452463
    # lon = -89.3161394
    # loc = (lat,lon)
    # print(get_nearest_node(midwest_nodes,*loc))
    '''5'''
    # start_time = time.perf_counter()
    # cambridge_nodes = build_auxiliary_structures('resources/cambridge.nodes','resources/cambridge.ways')
    # loc1 = (42.3858, -71.0783)
    # loc2 = (42.5465, -71.1787)
    # find_short_path(cambridge_nodes,loc1,loc2)
    # print('Time so far:',time.perf_counter()-start_time)
    #No Heuristic popped 688128 paths
    #Heuristic popped 85578 paths
    # duration = time.perf_counter()-start_time
    # print('it took:',duration)
    '''Testing stuff '''
    #print(find_short_path_nodes((midwest_nodes,midwest_ways),272855431, 233945564))
    
    # for way in midwest_ways:
    #     if 234022411 in midwest_ways[way][0] or 272856928 in midwest_ways[way][0]:
    #         print("way:",midwest_ways[way])
    # print(len(midwest_nodes))
    # print(midwest_nodes[id_1])
    #mit_nodes,mit_ways = build_auxiliary_structures('resources/mit.nodes','resources/mit.ways')
    # print(mit_nodes)
    # node1 = 1 # Kresge
    # node2 = 2 # New House
    # expected_path = [1, 10, 3, 2]
    # print(find_short_path_nodes(mit_nodes,node1,node2))
    # compare_result_expected(load_dataset('mit'), (node1, node2), expected_path, 'short', True)
    # loc1 = (42.3576, -71.0951) #close to Kresge
    # loc2 = (42.3605, -71.091) # is near an invalid node: Unreachable Node
    # expected_path = [
    #     (42.3575, -71.0952), (42.3582, -71.0931),
    #     (42.3592, -71.0932), (42.36, -71.0907),
    # ]
    # print(find_short_path((mit_nodes,mit_ways),loc1,loc2))
    pass