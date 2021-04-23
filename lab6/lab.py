#!/usr/bin/env python3
"""6.009 Lab 6 -- Boolean satisfiability solving"""

import sys
sys.setrecursionlimit(10000)
# NO ADDITIONAL IMPORTS

def simplify_clause(clause, assignments):
    '''
    Simplify the clause by removing literals that have received assignments.
    Raise exception if false
    '''
    simplified_clause = []
    for literal in clause:
        variable = literal[0]
        value = literal[1]
        if variable in assignments:
            #Any true literal truthifies the whole clause
            if value == assignments[variable]:
                return True
            # False literal is skipped
        else:
            simplified_clause.append(literal)
    #Clause is false if nothing is true
    if len(simplified_clause) == 0:
        raise Exception
    return simplified_clause
        

def simplify_formula(formula, assignments):
    '''
    Return simplified formula, True if assignments were updated with single clauses
    '''
    updated = False
    simplified_formula = []
    for clause in formula:
        simplified_clause = simplify_clause(clause, assignments)
        #Removed the satisfied clauses
        if simplified_clause is True:
            continue
        #Update assignments if only one variable
        elif len(simplified_clause) == 1:
            assignments[simplified_clause[0][0]] = simplified_clause[0][1]
            updated = True
        else:
            simplified_formula.append(simplified_clause)
    return simplified_formula, updated

def try_assignment(formula, variable, value):
    '''
    Try to satisfy a formula by setting variable to value
    Updated is a switch variable that breaks the while loop if there is no singleton clause
    '''
    simplified_formula = formula
    assignments = {variable: value}
    updated = True
    try:
        #Will loop through the formula and simplify it until it is empty
        while updated:
            simplified_formula, updated = simplify_formula(formula, assignments)
        #Attempts to satisfy the simplified formula
        result = satisfying_assignment(simplified_formula)
        #Update result if it didn't fail
        if result is not None:
            result.update(assignments)
        return result
    #Error raised if false clause
    except:
        return None

def satisfying_assignment(formula):
    """Find a satisfying assignment for a given CNF formula.
    Returns that assignment if one exists, or None otherwise.
    >>> satisfying_assignment([])
    {}
    >>> satisfying_assignment([[('a', True), ('b', False), ('c', True)]])
    {'a': True}
    >>> satisfying_assignment([[('a', True)], [('a', False)]])"""
    # Empty Case
    assignments = {}
    if len(formula) == 0:
        return assignments
    #Initial Variables
    literal = formula[0][0]
    variable = literal[0]
    value = literal[1]
    #Try the assignment
    assignments = try_assignment(formula, variable, value)
    #Try not assignment if failed
    if assignments is None:
        assignments = try_assignment(formula, variable, not value)
    return assignments


def combinations(seq, n):
    '''
    Generate all combinations of n elements from seq
    Effectively len(seq) choose n
    '''
    if n == 0:
        yield []
    elif len(seq) == n:
        yield seq
    elif n < len(seq):
        first = seq[0]
        remaining = seq[1:]
        for s in combinations(remaining,n-1):
            yield [first] + s
        yield from combinations(remaining,n)


def boolify_scheduling_problem(student_preferences, room_capacities):
    """
    Convert a quiz-room-scheduling problem into a Boolean formula.

    student_preferences: a dictionary mapping a student name (string) to a set
                         of room names (strings) that work for that student

    room_capacities: a dictionary mapping each room name to a positive integer
                     for how many students can fit in that room

    Returns: a CNF formula encoding the scheduling problem, as per the
             lab write-up

    We assume no student or room names contain underscores.
    """
    students = list(student_preferences.keys())
    rooms = list(room_capacities.keys())
    
    def variable_name(student, room):
        '''
        Construct a variable name from student and room
        '''
        return student + "_" + room
    
    # cover rule 1 and 2
    one_room = []
    preference = []
    for student in students:
        for combo in combinations(rooms, 2):
            one_room.append([(variable_name(student, room), False) for room in combo])
        preference.append([(variable_name(student, room), True) for room in student_preferences[student]])
    # cover rule 3
    oversubscribed = []
    for room in rooms:
        # include only rooms with capacity 
        # less than number of students
        capacity = room_capacities[room]
        if capacity < len(students):
            for combo in combinations(students, capacity+1):
                oversubscribed.append([(variable_name(student, room), False) for student in combo])
                
    return one_room + preference + oversubscribed


if __name__ == '__main__':
    import doctest
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)

    # print(boolify_scheduling_problem({'Alice': {'basement', 'penthouse'},
    #                         'Bob': {'kitchen'},
    #                         'Charles': {'basement', 'kitchen'},
    #                         'Dana': {'kitchen', 'penthouse', 'basement'}},
    #                        {'basement': 1,
    #                         'kitchen': 2,
    #                         'penthouse': 4}))