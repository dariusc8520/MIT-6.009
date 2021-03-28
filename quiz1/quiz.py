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
        if i not in seen:
            seen[i]=1
        else:
            seen[i]+=1
    return [i for i in seen if seen[i]<2]
    
##################################################
#  Problem 2
##################################################

def filter_graph (graph):
    ''''
    Filtering the data so that every node has all possible neighbors included
    '''
    unseen = set(graph.keys())
    filtered_graph = {}
    for node in graph:
        
        unseen.update(node)
        neighbors = graph[node].copy()
        neighbors.append(node)
        if node not in filtered_graph:
            filtered_graph[node] = set(neighbors)
        else:
            filtered_graph[node].update(neighbors)
        for neighbor in neighbors:
            if neighbor not in filtered_graph:
                filtered_graph[neighbor] = 1
                filtered_graph[neighbor] = set(neighbors)    
            else:
                filtered_graph[neighbor].update(neighbors)
    return filtered_graph, unseen

def bfs(visited, graph, node, queue, unseen):
    '''
    Standard Breadth First Search
    '''
    visited.append(node)
    queue.append(node)
    island = set()
    while queue:
        s = queue.pop(0) 
        island.update(s)
        unseen.discard(s)
        for neighbour in graph[s]:
            if neighbour not in visited:
                visited.append(neighbour)
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
    visited = []
    queue = []
    while unseen:
        starting_node = unseen.pop()
        island = bfs(visited,filtered_graph,starting_node,queue,unseen)
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
    print('starting state',start_state)
    #return start_state

                
    def moves_to_states(moves_to_consider,original_state):
        result = []
        cats_on_left = original_state[0]
        dogs_on_left = original_state[1]
        pat_on_left = original_state[2]
        cats_on_right = original_state[3]
        dogs_on_right = original_state[4]

        for move in moves_to_consider:
            cats = move.count('c')
            dogs = move.count('d')
            if pat_on_left:
                left_cat = cats_on_left-cats
                left_dog = dogs_on_left-dogs
                right_cat = cats_on_right+cats
                right_dog = dogs_on_right+dogs
                state = (left_cat,left_dog,0,right_cat,right_dog,move)
            else:
                left_cat = cats_on_left+cats
                left_dog = dogs_on_left+dogs
                right_cat = cats_on_right-cats
                right_dog = dogs_on_right-dogs
                state = (left_cat,left_dog,1,right_cat,right_dog,move)
            result.append(state)
        return result

    def successors(state):
        """
        Given a state, successors(state) should be an interable object
        containing all valid states that can be reached within one move.
        """
        #possible_moves = ['dd','cc','dc','c','d']
        moves_to_consider = []
        cats_on_left = state[0]
        dogs_on_left = state[1]
        cats_on_right = state[3]
        dogs_on_right = state[4]
        pat_on_left = state[2]
        if pat_on_left:
            if dogs_on_left-2>-1:
                if -2<cats_on_left-(dogs_on_left-2)<2:
                    moves_to_consider.append('dd')
            if dogs_on_left > 0 and cats_on_left > 0:
                moves_to_consider.append('dc')
            if cats_on_left-2>-1:
                if -2<dogs_on_left-(cats_on_left-2)<2:
                    moves_to_consider.append('cc')
            if dogs_on_left-1>-1:
                if cats_on_left-(dogs_on_left-1)<2:
                    moves_to_consider.append('d')
            if cats_on_left-1>-1:
                if dogs_on_left-(cats_on_left-1)<2:
                    moves_to_consider.append('c')  
            print('left to right')
            print(moves_to_consider)
            return moves_to_states(moves_to_consider,state)
        else:
            if dogs_on_right-2>-1:
                if -2<cats_on_right-(dogs_on_right-2)<2:
                    moves_to_consider.append('dd')
            if dogs_on_right > 0 and cats_on_right > 0:
                moves_to_consider.append('dc')
            if cats_on_right-2>-1:
                if -2<dogs_on_right-(cats_on_right-2)<2:
                    moves_to_consider.append('cc')
            if dogs_on_right-1>-1:
                if cats_on_right-(dogs_on_right-1)<2:
                    moves_to_consider.append('d')
            if cats_on_right-1>-1:
                if dogs_on_right-(cats_on_right-1)<2:
                    moves_to_consider.append('c')   
            print('right to left')
            print(moves_to_consider)
            return moves_to_states(moves_to_consider,state)

        #Adding conditionals like pat not on the side of the river, etc
        #Moving one or two cat+dog across and checking these conditions
        #Adding the possible ones to a list

    def goal_test(state):
        """
        Return True if the given state satisfies the goal condition, and False
        otherwise.
        """
        #print('goal state', state)
        return sum([state[0],state[1],state[2]])==0
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
    print('path', path)
    # if path == None:
    #     return None
    final_path = []
    for state in path:
        move = state[5]
        if move is not None:
            final_path.append(move)
    print('final path', final_path)
    print()
    return final_path


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
