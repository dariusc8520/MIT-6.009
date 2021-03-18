#!/usr/bin/env python3

from util import read_osm_data, great_circle_distance, to_local_kml_url

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
    for way in ways:
        if 'highway' in way['tags']:            
            if way['tags']['highway'] in ALLOWED_HIGHWAY_TYPES:
                ways_db[way['id']] = (way['nodes'],way['tags'])
    for node in nodes:
        nodes_db[node['id']] = (node['lat'],node['lon'],node['tags'])
    return (nodes_db,ways_db)
    
def get_distance(node1, node2):
    ''' 
    Returns the distance in miles given two Node ids
    '''
    lat1 = midwest_nodes[node1][0]
    lon1 = midwest_nodes[node1][1]
    lat2 = midwest_nodes[node2][0]
    lon2 = midwest_nodes[node2][1]
    return great_circle_distance((lat1,lon1),(lat2,lon2))
    
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
    for way in ways_db:
        list_of_nodes = ways_db[way][0]
        if node1 in list_of_nodes and node2 in list_of_nodes:
            index = list_of_nodes.index(node1)
            starting_node = list_of_nodes[index]
            next_node = list_of_nodes[index+1]
            cost = get_distance(starting_node,next_node)
            agenda.append((cost,[starting_node,next_node]))
            #print('We got one')
    #print('agenda:',agenda)

    visited = set()
    #While True:
    path_to_consider = agenda.pop(agenda.index(min(agenda)))
    
    
    list_of_nodes = midwest_ways[21705939][0]
    dist = 0
    for i in range(len(list_of_nodes)-1):
        id_1 = list_of_nodes[i]
        id_2 = list_of_nodes[i+1]
        dist += get_distance(id_1,id_2)

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
    raise NotImplementedError


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
    midwest_nodes,midwest_ways = build_auxiliary_structures('resources/midwest.nodes','resources/midwest.ways')

    # print('Question 3.1.3.1:', great_circle_distance((42.363745, -71.100999),(42.361283,-71.239677)))

    id_1 = 233941454
    id_2 = 233947199
    # print('Question 3.1.3.2:', get_distance(id_1,id_2))
    
    # list_of_nodes = midwest_ways[21705939][0]
    # dist = 0
    # for i in range(len(list_of_nodes)-1):
    #     id_1 = list_of_nodes[i]
    #     id_2 = list_of_nodes[i+1]
    #     dist += get_distance(id_1,id_2)
    # print('Question 3.1.3.3:',dist)
    
    '''Testing stuff '''
    find_short_path_nodes((midwest_nodes,midwest_ways),6344453428, 6344453426)
    # for way in midwest_ways:
    #     print(midwest_ways[way][0])
    # print(len(midwest_nodes))
    # print(midwest_nodes[id_1])
    pass
