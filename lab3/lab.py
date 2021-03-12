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
    return actor_id_2 in data[1][actor_id_1]

def actors_with_bacon_number(data, n):
    raise NotImplementedError("Implement me!")


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
    with  open('resources/names.pickle', 'rb') as f:
        namedb = pickle.load(f)
    with  open('resources/tiny.pickle', 'rb') as f:
        tinydb = pickle.load(f)
    print(tinydb)
    print(transform_data(tinydb))
    
    # print(transform_data(tinydb))
    # print(tinydb)
    # key_list = list(smalldb.keys())
    # val_list = list(smalldb.values())
    # position = val_list.index(557932)
    # print(key_list[position])

    
    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    pass
