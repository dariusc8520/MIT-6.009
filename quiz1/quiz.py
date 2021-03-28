import os
import doctest

import sys
from typing import final
if '.' not in sys.path:
    sys.path.insert(0, '.')
from search import search

# NO OTHER IMPORTS!


##################################################
#  Problem 1
##################################################
'''
Returns an ordered list of elements in L that occur less 2 times
'''

def foo(L):
    seen = {}
    for i in L:
        if i not in seen: #Initializes key
            seen[i]=1
        else: #Counter
            seen[i]+=1
    return [i for i in seen if seen[i]<2]
    
##################################################
#  Problem 2
##################################################

def filter_graph (graph):
    ''''
    Filtering the data so that every node has all possible neighbors included
    '''
    unseen = set(graph.keys()) #Set of nodes to pop from
    filtered_graph = {}
    for node in graph:
        unseen.update(node)
        neighbors = graph[node].copy()
        neighbors.append(node) #Includes itself
        if node not in filtered_graph:
            filtered_graph[node] = set(neighbors)
        else:
            filtered_graph[node].update(neighbors)
        for neighbor in neighbors:
            if neighbor not in filtered_graph:
                filtered_graph[neighbor] = set(neighbors)    
            else:
                filtered_graph[neighbor].update(neighbors)
    return filtered_graph, unseen

def bfs(graph, node, queue, unseen):
    '''
    Standard Breadth First Search
    Uses an unseen set instead of a visited set
    '''
    queue.append(node)
    island = set()
    while queue:
        s = queue.pop(0) 
        island.update(s)
        unseen.discard(s)
        for neighbour in graph[s]:
            if neighbour in unseen:
                queue.append(neighbour)
    return island

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
    filtered_graph,unseen = filter_graph(graph)
    result = []
    queue = []
    while unseen:
        starting_node = unseen.pop() #Takes a random element from set
        island = bfs(filtered_graph,starting_node,queue,unseen)
        result.append(island)
    return result

##################################################
#  Problem 3
##################################################


def setup_cats_and_dogs(cats, dogs):
 
    """
    start_state should contain the initial state (vertex label) for the search
    process
    """
    '''
    Dictionary of left side and right side that is a list consisting of cats (c) and dogs(d) and pat(p)
    '''
    start_state = (cats,dogs,1,0,0,None)

    def check_state(state):
        cats_on_left = state[0]
        dogs_on_left = state[1]
        cats_on_right = state[3]
        dogs_on_right = state[4]
        pat_on_left = state[2]

        if cats_on_left > 0 and dogs_on_left > 0 and not pat_on_left: #Checks for a fight on left side
            if abs(cats_on_left-dogs_on_left)>1:
                return False
        elif cats_on_right > 0 and dogs_on_right > 0 and pat_on_left: #Checks for a fight on right side
            if abs(cats_on_right-dogs_on_right)>1:
                return False
        if cats_on_left < 0 or dogs_on_left < 0 or cats_on_right < 0 or dogs_on_right < 0: #Checks for impossible states
            return False
        else:
            return True

    def moves_to_states(moves_to_consider,original_state):
        '''
        Takes a list of moves to consider and creates a state from that move
        Input will be all 5 possible moves ['dd','cc','dc','c','d']
        '''
        result = []
        cats_on_left = original_state[0]
        dogs_on_left = original_state[1]
        pat_on_left = original_state[2]
        cats_on_right = original_state[3]
        dogs_on_right = original_state[4]

        for move in moves_to_consider:
            cats = move.count('c')
            dogs = move.count('d')
            if pat_on_left: #Adds and removes dogs and cats accordingly
                left_cat = cats_on_left-cats 
                left_dog = dogs_on_left-dogs
                right_cat = cats_on_right+cats
                right_dog = dogs_on_right+dogs
                state = (left_cat,left_dog,0,right_cat,right_dog,move) #0 represents Pat on Rightside Now
            else:
                left_cat = cats_on_left+cats
                left_dog = dogs_on_left+dogs
                right_cat = cats_on_right-cats
                right_dog = dogs_on_right-dogs
                state = (left_cat,left_dog,1,right_cat,right_dog,move)#1 represents Pat on Leftside Now
            result.append(state)
        return result

    def successors(state):
        """
        Given a state, successors(state) should be an interable object
        containing all valid states that can be reached within one move.
        """
        moves_to_consider = ['dd','cc','dc','c','d']
        successors = []
        states_to_consider = moves_to_states(moves_to_consider,state) #Gets all possible states to consider
        for state in states_to_consider:
            if check_state(state):
                successors.append(state)
        return successors #only returns the valid ones

    def goal_test(state):
        """
        Return True if the given state satisfies the goal condition, and False
        otherwise.
        """
        return sum([state[0],state[1],state[2]])==0 #There should be no cats, dogs or pat on the left

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
    if path == None: #No valid solutions
        return None
    final_path = []
    for state in path: 
        move = state[5] #The corresponding move is included as the 6th element in each state
        if move is not None:
            final_path.append(move)
    return final_path


def cats_and_dogs(cats, dogs):
    """
    This end-to-end function is included here for testing.  You should not
    change it.
    """
    result = search(*setup_cats_and_dogs(cats, dogs))
    return interpret_result(result)



if __name__ == '__main__':
    doctest.testmod()
