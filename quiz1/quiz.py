import os
import doctest

import sys
if '.' not in sys.path:
    sys.path.insert(0, '.')
from search import search

# NO OTHER IMPORTS!


##################################################
#  Problem 1
##################################################
'''
Returns an ordered list of elements in L that occur more than 2 times
'''

# def foo(L):
#     out = []
#     seen = []
#     seenagain = []
#     for i in L:
#         if i not in set(seen):
#             seen.append(i)
#         elif i not in set(seenagain):
#             seenagain.append(i)
#     for i in L:
#         if i not in set(seenagain) and i not in out:
#             out.append(i)
#     return out


def foo(L):
    seen = {}
    for i in L:
        if i not in seen:
            seen[i]=1
        else:
            seen[i]+=1
    return [i for i in seen if seen[i]<2]
    
##################################################
#  Problem 2
##################################################


def get_islands(graph):
    """
    Given a graph dictionary, return the "islands" in the graph, where an
    island is a set of nodes that are transitively connected through the edges
    of that graph.

    >>> get_islands({'A': []})
    [{'A'}]
    >>> x = get_islands({'A': [], 'B': ['B']})
    >>> len(x)
    2
    >>> {'B'} in x and {'A'} in x
    True
    >>> g1 = {'A': ['B', 'C'], 'B': [], 'C': [], 'D': []}
    >>> x = get_islands(g1)
    >>> len(x)
    2
    >>> {'A', 'B', 'C'} in x and {'D'} in x
    True
    >>> g2 = {'A': ['B'], 'C': ['A'], 'B': ['C'], 'D': ['E'],
    ...       'E': [], 'F': ['F'], 'G': [],}
    >>> x = get_islands(g2)
    >>> len(x)
    4
    >>> all(i in x for i in ({'A', 'B', 'C'}, {'D', 'E'}, {'F'}, {'G'}))
    True
    """
    '''
    Iterate through all the nodes in graph
    If a node is not seen before, create a new island add all the neighbors into the new island
    If in the path down neighbors, it finds a neighbor that has been seen before, it means it is connected to a previous island
    Look for that island and merge the two sets
    Once all nodes have been seen, then return the result
    '''
    result = []
    seen = set()
    #print('graph',graph)
    for node in graph:
        if node not in seen:
            seen.add(node) #Updates seen and starts new island
            island = set()
            island.add(node)
            neighbors = graph[node]
            for neighbor in neighbors: #Adds neighbors
                island,seen,result = adding_neighbors(neighbor,island,seen,result)
            result.append(island)
            #print(island)
    #print('result:',result)
    return result

def adding_neighbors(neighbor,island,seen,result):
    island.add(neighbor) #Updates seen and islands
    seen.add(neighbor)
    for islands in result:
        if neighbor in islands: #Checks if the island with this neighbor exists
            #print('found one in islands')
            old_island = result.pop(result.index(islands)) #Replaces this old island with new island that is a union
            #print('old island',old_island)
            island.update(old_island)
            #print('new island', island)
    return island,seen,result
##################################################
#  Problem 3
##################################################


def setup_cats_and_dogs(cats, dogs):
    '''
    Dictionary of left side and right side that is a list consisting of cats (c) and dogs(d) and pat(p) and a path which is the path that should be taken
    ''''
    start_state = {'leftside':['c']*cats+['d']*dogs+['p'],'rightside':[], 'path':[]}
    #return start_state
    """
    start_state should contain the initial state (vertex label) for the search
    process
    """

    def successors(state):
        """
        Given a state, successors(state) should be an interable object
        containing all valid states that can be reached within one move.
        """
        raise NotImplementedError
        #Adding conditionals like pat not on the side of the river, etc
        #Moving one or two cat+dog across and checking these conditions
        #Adding the possible ones to a list

    def goal_test(state):
        """
        Return True if the given state satisfies the goal condition, and False
        otherwise.
        """
        raise NotImplementedError
        #Checks that all cats and dogs and pat is on the right side of the river

    return successors, start_state, goal_test


def interpret_result(path):
    """
    Given a path as returned from the search process, return a list of actions
    that the pet herder must take in order to successfully move the animals
    across the river, or None if that is not possible.

    For example, ['dd', 'cd', 'c'] means:
      1. take 2 dogs across, then
      2. take a cat and a dog across, then
      3. take a cat across
    """
    raise NotImplementedError
    #Not neceesary, just return start_state['path'] when goal_test true.


def cats_and_dogs(cats, dogs):
    """
    This end-to-end function is included here for testing.  You should not
    change it.
    """
    result = search(*setup_cats_and_dogs(cats, dogs))
    return interpret_result(result)



if __name__ == '__main__':
    #print(setup_cats_and_dogs(3,2))
    doctest.testmod()
