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
    
def get_distance(node_db,node1, node2):
    ''' 
    Returns the distance in miles given two Node ids
    '''
    lat1 = node_db[node1][0]
    lon1 = node_db[node1][1]
    lat2 = node_db[node2][0]
    lon2 = node_db[node2][1]
    return great_circle_distance((lat1,lon1),(lat2,lon2))
    
def get_cost_and_path(aux_structures,node1,node2,old_cost,path_to_consider,agenda,visited):
    """ 
    Updates the agenda with the cost and paths of the children vertices that are not in visited
    Agenda Entries are (Cost,[Path List])
    """
    nodes_db = aux_structures[0]
    ways_db = aux_structures[1]
    last_node=node1
    for way in ways_db:
        #print("we're in this loop")
        list_of_nodes = ways_db[way][0]
        if last_node in list_of_nodes:
            #print('list of nodes:', list_of_nodes)
            #print("We're in the loop")
            index = list_of_nodes.index(last_node) #Last node here instead of node1
            starting_node = list_of_nodes[index]
            #print('index:',index)
            #print('starting node:', starting_node)
            try:
                next_node1 = list_of_nodes[index+1]
                if next_node1 not in visited:
                    #print('next node(+1):',next_node1)
                    cost = old_cost + get_distance(nodes_db,starting_node,next_node1)
                    #print('old cost:',old_cost)
                    #print('cost:',cost)
                    new_path = path_to_consider+ [next_node1]
                    agenda.append((cost,new_path))
            except:
                    pass
                
            if 'oneway' in ways_db[way][1]:
                if ways_db[way][1]['oneway'] == 'yes':
                    continue
            try:
                next_node2 = list_of_nodes[index-1]
                if next_node2 not in visited:
                    #print('next node(-1):',next_node2)
                    cost = old_cost + get_distance(nodes_db,starting_node,next_node2)
                    #print('new cost:',cost)
                    new_path = path_to_consider+ [next_node2]
                    agenda.append((cost,new_path))
            except:
                pass
    return (agenda,visited)

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
    agenda,visited = get_cost_and_path(aux_structures,node1,node2,0,[node1],agenda,visited)

    #print('initial agenda:',agenda)
    visited = {node1}
    while True:
        #print('visited:',visited)
        try:
            min(agenda)
        except:
            return None
        #print('agenda',agenda)
        #print('min agenda:',min(agenda))
        #print('index:', agenda.index(min(agenda)))
        (old_cost,path_to_consider) = agenda.pop(agenda.index(min(agenda)))
        #print('path:',path_to_consider)
        last_node = path_to_consider[-1]
        #print('last node:', last_node)
        if last_node == node2:
            print('SUCCESS',path_to_consider)
            return path_to_consider
        elif last_node not in visited:
            visited.add(last_node)
            #print('visited:',visited)
            agenda,visited = get_cost_and_path(aux_structures,last_node,node2,old_cost,path_to_consider,agenda,visited)

        if agenda == []:
            break


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
    
    '''Testing stuff '''
    #print(find_short_path_nodes((midwest_nodes,midwest_ways),272855431, 233945564))
    
    for way in midwest_ways:
        if 234022411 in midwest_ways[way][0] or 272856928 in midwest_ways[way][0]:
            print("way:",midwest_ways[way])
    # print(len(midwest_nodes))
    # print(midwest_nodes[id_1])
    # mit_nodes,mit_ways = build_auxiliary_structures('resources/mit.nodes','resources/mit.ways')
    # node1 = 7 # near Building 35
    # node2 = 3 # Near South Maseeh
    # expected_path = [7, 5, 10, 3]
    # print(mit_ways)
    # find_short_path_nodes((mit_nodes,mit_ways),node1,node2)
    #compare_result_expected(load_dataset('mit'), (node1, node2), expected_path, 'short', True)
    pass
