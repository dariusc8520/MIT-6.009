#!/usr/bin/env python3
"""6.009 Lab 9: Snek Interpreter"""

import doctest
# NO ADDITIONAL IMPORTS!
# import sys
# sys.setrecursionlimit(20)
#########
# Class #
#########

# class Environment():
    

###########################
# Snek-related Exceptions #
###########################

class SnekError(Exception):
    """
    A type of exception to be raised if there is an error with a Snek
    program.  Should never be raised directly; rather, subclasses should be
    raised.
    """
    pass


class SnekSyntaxError(SnekError):
    """
    Exception to be raised when trying to evaluate a malformed expression.
    """
    pass


class SnekNameError(SnekError):
    """
    Exception to be raised when looking up a name that has not been defined.
    """
    pass


class SnekEvaluationError(SnekError):
    """
    Exception to be raised if there is an error during evaluation other than a
    SnekNameError.
    """
    pass


############################
# Tokenization and Parsing #
############################


def tokenize(source):
    """
    Splits an input string into meaningful tokens (left parens, right parens,
    other whitespace-separated values).  Returns a list of strings.

    Arguments:
        source (str): a string containing the source code of a Snek
                      expression
    """
    tokenized_source = []
    numorword = ''
    i = 0
    while i < len(source):
        if source[i] != ' ':
            if source[i] in '()':
                tokenized_source.append(source[i])
            elif source[i] == ';':
                while True:
                    i += 1
                    if i == len(source) or source[i:i+1] == '\n':
                        break
            elif source[i:i+1] == '\n':
                tokenized_source.append(numorword)
                numorword = ''
            else: #letter or number or other punctuation#
                numorword = numorword + source[i]
                if i == len(source)-1 or (i < len(source) - 1 and source[i+1] in '() '):
                    tokenized_source.append(numorword)
                    numorword = ''
        i += 1
    return tokenized_source

def parse(tokens):
    """
    Parses a list of tokens, constructing a representation where:
        * symbols are represented as Python strings
        * numbers are represented as Python ints or floats
        * S-expressions are represented as Python lists

    Arguments:
        tokens (list): a list of strings representing tokens

    (:= circle-area (function (r) (* 3.14 (* r r))))
    [':=', 'circle-area', ['function', ['r'], ['*', 3.14, ['*', 'r', 'r']]]]
    """
    def is_number(N):
        '''
        Determine if a string is a float or int
        >>> is_number(3.0)
        True
        >>> is_number(3)
        True
        >>> is_number(3.0.0)
        False
        '''
        try:
            a = float(N)
            return True
        except:
            return False

    def parse_expression(index):
        '''
        Recursively parses the tokens given an integer index
        '''
        token = tokens[index] 
        nonlocal open_counter,closed_counter

        # if token.isalpha():
        #     return str(token), index + 1
        if is_number(token):
            if '.' in token:
                return float(token), index + 1
            else:
                return int(token), index + 1
        elif token in '+-*/' :
            return token, index + 1
        elif token == '(':
            open_counter += 1
            subexpr = []
            index += 1
            while tokens[index] != ')':
                par_expr,index = parse_expression(index)
                if par_expr != None:
                    subexpr.append(par_expr)
                if index >= len(tokens):
                    raise SnekSyntaxError
            closed_counter += 1
            return subexpr, index + 1
        elif token == ')':
            closed_counter += 1
            return None, index + 1
        else: #Alphabet letters and punctuation
            return token, index + 1

    open_counter = 0
    closed_counter = 0
    
    if len(tokens) > 1 and '(' not in tokens and ')' not in tokens:
        raise SnekSyntaxError ('missing brackets')
    elif '(' in tokens and ')' not in tokens:
        raise SnekSyntaxError ('open bracket no closed bracket')
    elif '(' not in tokens and ')' in tokens:
        raise SnekSyntaxError ('no open bracket but closed bracket')

    print('tokens',tokens)
    if len(tokens) > 1 and tokens[1] == ':=':
        if len(tokens) < 5:
            raise SnekSyntaxError (':= but not three elements ')
        if type(tokens[3]) != str:
            raise SnekSyntaxError ('variable is not string')
        if tokens[2] == '(':
            i = 3
            while tokens[i] != ')':
                if type(tokens[i]) != str:
                    raise SnekSyntaxError ('variable is invalid')
                i += 1

    parsed_expression, index = parse_expression(0)

    if parsed_expression == None:
        raise SnekSyntaxError ('parsed = none')

    while index < len(tokens):
        new_parsed_expression, index = parse_expression(index)
        if new_parsed_expression != None and parsed_expression != None:
            parsed_expression = parsed_expression + new_parsed_expression
        
    if open_counter != closed_counter:
        raise SnekSyntaxError ('counters not equal')

    if type(parsed_expression) == list:
        if parsed_expression[0] == 'function' or parsed_expression[0] == ':=':
            if len(parsed_expression) != 3:
                raise SnekSyntaxError
            if type(parsed_expression[1]) == int:
                raise SnekSyntaxError
            if type(parsed_expression[1]) == list:
                for ele in parsed_expression[1]:
                    if type(ele) != str:
                        raise SnekSyntaxError
            if parsed_expression[0] == ':=' and parsed_expression[1] == []:
                raise SnekSyntaxError

    return parsed_expression



######################
# Built-in Functions #
######################
class GlobalEnv:
    def __init__(self,parent=None):
        self.variables = {}
        self.parent = parent

    def __setitem__(self,key,value):
        self.variables.update({key:value})

    def __getitem__(self,key):
        if key in self.variables:
            return self.variables[key]
        try:
            return self.parent[key]
        except:
            raise SnekNameError

    def __contains__(self,key):
        if key in self.variables:
            return True
        elif self.parent != None:
            try:
                value = None
                value = self.parent[key]
                if value != None:
                    return True
            except:
                return False
        else:
            return False #SnekNameError

class builtin(GlobalEnv):

    def __init__(self):
        snek_builtins = {
        '+': lambda args: 0 if len(args) == 0 else sum(args),
        '-': lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
        '*': lambda args: 1 if len(args) == 0 else ( args[0] if len(args) == 1 else (args[0] * args[1])),
        '/': lambda args: 'Error' if len(args) == 0 else ( 1 / args[0] if len(args) == 1 else (args[0] / args[1]))
    }
        self.variables = snek_builtins

class function():
    def __init__(self, vars, exp, parent):
        self.vars = vars
        self.exp = exp
        self.env = parent


##############
# Evaluation #
##############


def evaluate(tree, env = None):
    """
    Evaluate the given syntax tree according to the rules of the Snek
    language.

    Symbol in snek_builtins, return associated object
    Number should return number
    Expression should return evaluated expression
    Symbol not in snek_builtins, raise SnekNameError

    Arguments:
        tree (type varies): a fully parsed expression, as the output from the
                            parse function
    """
    def recurse_update(tree,env):
        '''
        recursively goes through a tree and updates all values that are in the environment
        '''
        updated_tree = tree.copy()
        for i in range(len(tree)): #updates the variables
            if type(tree[i]) == list:
                updated_tree[i] = recurse_update(tree[i],env)
            if type(tree[i]) == str and (tree[i] not in '+-*/:=' or tree[i] != 'function') and tree[i] in env:
                if type(env[tree[i]]) != function:
                    updated_tree[i] = env[tree[i]]
        return updated_tree

    print('input',tree)
    func = None
    if env == None:
        snek_builtin = builtin()
        env = GlobalEnv(snek_builtin)

    if type(tree) == int or type(tree) == float:
        return tree
    
    elif type(tree) == str:
        return env[tree]

    if type(tree[0]) == str:
        if tree[0] == ':=':
            if type(tree[1]) == list and tree[1]: #Easier function
                env[tree[1][0]] = function(tree[1][1:],tree[2],env)
                return env[tree[1][0]]
            else:
                try: #Assigning value
                    env[tree[1]] = evaluate(tree[2], env)
                    # print('assigned value', env[tree[1]])
                    return env[tree[1]]
                except:
                    raise SnekNameError('could not update env')
        elif tree[0] == 'function': #Function Creation
            return function(tree[1],tree[2],env)
        else: #Looking for a function
            try:
                func = env[tree[0]]
            except:
                raise SnekNameError('not in snek_builtins!!')

    if type(tree[0]) == list:
        func = evaluate(tree[0], env)
    if type(tree) == list and type(tree[0]) == int:
        raise SnekEvaluationError ('first element is not valid function')

    updated_tree = recurse_update(tree,env)
    print('updated tree',updated_tree)

    if func == None:
        func = tree[0]

    if type(func) == function:
        parent_env = func.env
        new_env = GlobalEnv(parent_env)
        vars = func.vars
        exp = func.exp
        if len(vars) != len(updated_tree[1:]):
            raise SnekEvaluationError

        for i in range(len(vars)):
            updated_element = evaluate(updated_tree[i+1],parent_env)
            new_env[vars[i]] = updated_element
        print(new_env.variables)
        
        return evaluate(exp,new_env)

    if len(tree)>2:
        value = evaluate(updated_tree[1],env)
        new_tree = updated_tree[2:]
        # print('modified input',new_tree)
        for ele in new_tree:
            if type(ele) == list:
                ele = evaluate(ele, env)
            if func != None:
                value = func([value, ele])
    elif len(tree) == 2:
        value = updated_tree[1]
        value = func([value])
    else:
        value = func([])

    # print('value',value)
    return value

def REPL():
    snek_builtin = builtin()
    env = GlobalEnv(snek_builtin)
    inp = input('Input:')
    while inp != 'QUIT':
        try:
            tokens = tokenize(inp)
            expression = parse(tokens)
            output = evaluate(expression, env)
            print('Output:', output)
        except SnekEvaluationError:
            print('Error: First element is not a valid function')
        except SnekNameError:
            print('Error: Not in snek_builtins')
        except SnekSyntaxError:
            print('Error: Not a parsable expression')
        inp = input('Input:')
        # except:
        #     print('Error: Non Snek Error')
        #     inp = input()

def result_and_env(tree, env = None):
    if env == None:
        snek_builtin = builtin()
        env = GlobalEnv(snek_builtin)
    output = evaluate(tree, env)
    return (output, env)

if __name__ == '__main__':
    # code in this block will only be executed if lab.py is the main file being
    # run (not when this module is imported)

    # uncommenting the following line will run doctests from above
    # doctest.testmod()

    # print(tokenize('hello'))
    # print(parse(['(', 'spam', ')']))
    # print(tokenize('-500'))
    # print(tokenize('(spam); asdfasdfs \n   (hello(dfdf)) ; asdfsdf \n'))
    # print(parse(tokenize("(cat (dog (tomato)))")))
    # print(is_number('-'))
    # print(parse(['-6.28']))
    # print(parse(['(', '+', '2', '(', '-', '5', '3', ')', '7', '8', ')']))
    # print(evaluate(['+', 3, ['-', 3, 1],[3]]))
    # print(evaluate(['+', 2, 3]))
    # tokens =  tokenize('(:= pi)')
    # parse_exp = parse(tokens)
    # print(evaluate(parse_exp))
    REPL()
    # exp = parse(tokenize('(:= square (function (x) (* x x)))'))
    # print(exp)
    # print(evaluate(exp))
    # first = parse(tokenize('(:= (square x) (* x x))'))
    # evaluate(first)
    # second = parse(tokenize('(:= (fourthpow x) (square (square x)))'))
    # evaluate(second)
    # third = parse(tokenize('(fourthpow (square 2))'))
    # evaluate(third)