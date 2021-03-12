#!/usr/bin/env python3

import pickle
# NO ADDITIONAL IMPORTS ALLOWED!

# Note that part of your checkoff grade for this lab will be based on the
# style/clarity of your code.  As you are working through the lab, be on the
# lookout for things that would be made clearer by comments/docstrings, and for
# opportunities to rearrange aspects of your code to avoid repetition (for
# example, by introducing helper functions).


def transform_data(raw_data):
    """
    Takes in a converted pickle list of (actor #1 id, actor #2 id, film id) and creates a dictionary of films with a set of actors in the movie
    and a dictionary of actors with a set of actors they've been in a film with. Outputs as a tuple of (movies,actors).
    """
    movies = {}
    actors = {}
    for tup in raw_data:
        #updating movies dictionary
        if tup[2] not in movies.keys():
            movies[tup[2]] = {tup[0],tup[1]}
        else:
            new_tup = movies[tup[2]].union({tup[0],tup[1]})
            movies[tup[2]] = new_tup
        #updating actor dictionary for actor 1
        if tup[0] not in actors.keys():
            actors[tup[0]] = {tup[0],tup[1]}
        else:
            new_tup = actors[tup[0]].union({tup[1]})
            actors[tup[0]] = new_tup
        #updating actor dictionary for actor 2
        if tup[1] not in actors.keys():
            actors[tup[1]] = {tup[0],tup[1]}
        else:
            new_tup = actors[tup[1]].union({tup[0]})
            actors[tup[1]] = new_tup
    return (movies,actors)


def acted_together(data, actor_id_1, actor_id_2):
    """
    Returns True if actor 1 and actor 2 have been in a movie together. False otherwise
    """
    return actor_id_2 in data[1][actor_id_1]

def actors_with_bacon_number(data, n):
    """
    Takes in a graph and returns all the actors with a Bacon number n
    """
    movies = data[0]
    actors = data[1]
    bacon = 4724 #bacon's id number
    actors[bacon].discard(bacon) #Removes bacon from his own children
    if n==0: 
        return {bacon}
    elif n==1:
        return actors[bacon]
    else: #For n>1 cases
        visited = {bacon}
        parent_layer = actors[bacon] #Layer where n=1
        child_layer = set()
        while True:
            for actor in parent_layer: #Adds all the children of the parent layer
                visited.add(actor) #Updates visited actors
                child_layer.update(actors[actor])
            child_layer.difference_update(visited) #Removes actors if they've been visited
            if child_layer == set(): #Checks for the empty graph case
                return set()
            n-=1
            if n==1:
                return child_layer
            parent_layer = child_layer #Updates parent and children
            child_layer = set()
    

def bacon_path(data, actor_id):
    raise NotImplementedError("Implement me!")


def actor_to_actor_path(data, actor_id_1, actor_id_2):
    raise NotImplementedError("Implement me!")


def actor_path(data, actor_id_1, goal_test_function):
    raise NotImplementedError("Implement me!")


def actors_connecting_films(data, film1, film2):
    raise NotImplementedError("Implement me!")


if __name__ == '__main__':
    # #4
    # with open('resources/names.pickle', 'rb') as f:
    #     namedb = pickle.load(f)
    # actor_id_1 = namedb['Patrick Malahide']
    # actor_id_2 = namedb['Kristen Bone']
    # actor_id_3 = namedb['Beatrice Winde']
    # actor_id_4 = namedb['Rex Linn']
    # with open('resources/small.pickle', 'rb') as f:
    #     smalldb = pickle.load(f)
    # print('Have P. Malahide and K. Bone acted together?',acted_together(transform_data(smalldb),actor_id_1,actor_id_2))
    # print('Have B. Winde and R. Linn acted together?',acted_together(transform_data(smalldb),actor_id_3,actor_id_4))
    
    #5
    # with  open('resources/names.pickle', 'rb') as f:
    #     namedb = pickle.load(f)
    # with  open('resources/tiny.pickle', 'rb') as f:
    #     tinydb = pickle.load(f)
    # data = transform_data(tinydb)
    # print(tinydb)
    # print(data)
    # data[1][4724].discard(4724)
    # print(data[1])
    
    # with  open('resources/large.pickle', 'rb') as f:
    #     largedb = pickle.load(f)
    # data = transform_data(largedb)
    # actor_ids = actors_with_bacon_number(data,6)
    # print(actor_ids)
    # key_list = list(namedb.keys())
    # val_list = list(namedb.values())
    # position = [val_list.index(actor) for actor in actor_ids]
    # print(set([key_list[pos] for pos in position]))

    
    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    pass
