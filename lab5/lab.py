#!/usr/bin/env python3
"""6.009 Lab -- Six Double-Oh Mines"""

# NO IMPORTS ALLOWED!

def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    for key, val in sorted(game.items()):
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f'{key}:')
            for inner in val:
                print(f'    {inner}')
        else:
            print(f'{key}:', val)


# 2-D IMPLEMENTATION
def initialize_board_nd(dimensions,mask=False):
    '''
    Initializing the board with 0's

    Returns a board with a list of lists that is size num_rows x num_cols of [0]'s
    '''
    dimension = dimensions[0]
    if len(dimensions)==1:
        if not mask:
            board = [0]*dimension
        else:
            board = [False]*dimension
    else:
        board = [initialize_board_nd(dimensions[1:],mask) for i in range(dimension)]
    return board

def add_bombs_nd(board,bomb):
    '''
    Adds the bombs in their respective positions on the game board
    
    Returns the update board
    '''
    index = bomb[0]
    if len(bomb)==1:
        board[index] = '.'
    else:
        board[index] = add_bombs_nd(board[index],bomb[1:])
    return board

def get_neighbors_indices(index,dimensions):
    '''
    Returns the indicies of the neighbors of the specified location
    '''
    if len(index) == 0:
        return [[]]

    neighbors = []
    first_index = index[0]
    dim = dimensions[0]
    offset = [-1,0,1]

    for prev_index in get_neighbors_indices(index[1:],dimensions[1:]):
        for delta in offset:
            new_index = first_index+delta
            if 0<=new_index<dim:
                neighbors.append([new_index]+prev_index)
    return neighbors

def value_of(index,board):
    '''
    Gets you to the index of the board given coordinates
    '''
    if len(index)==1:
        return board[index[0]]
    return value_of(index[1:],board[index[0]])

def set_value_of(index,board,value,recurse=False):
    '''
    Sets the value of the index to the value
    '''
    if len(index) == 1:
        board[index[0]] = value
    else:
        set_value_of(index[1:],board[index[0]],value,True)

    if not recurse:
        return board

def update_bomb_neighbors_nd(board,dimensions,bombs):
    '''
    Updates the initial board state with the number of neighboring bombs for each tile

    Returns a list of lists that has updated tiles for neighboring bombs
    '''
    for bomb in bombs:
        bomb_neighbors = get_neighbors_indices(bomb,dimensions)
        for index in bomb_neighbors:
            value = value_of(index,board)
            if type(value)==int:
                set_value_of(index,board,value+1)
    return board

def new_game_2d(num_rows, num_cols, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'mask' fields adequately initialized.

    Parameters:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    mask:
        [False, False, False, False]
        [False, False, False, False]
    state: ongoing
    """
    return new_game_nd((num_rows,num_cols),bombs)

# def count_bombs_and_squares(game):
#     '''
#     Counts the number of bombs and covered squares on the current game board

#     Returns two ints of bombs and covered squares
#     '''
#     bombs = 0
#     covered_squares = 0
#     for r in range(game['dimensions'][0]):
#         for c in range(game['dimensions'][1]):
#             if game['board'][r][c] == '.':
#                 if  game['mask'][r][c] == True:
#                     bombs += 1
#             elif game['mask'][r][c] == False:
#                 covered_squares += 1
#     return bombs,covered_squares

def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['mask'] to reveal (row, col).  Then, if (row, col) has no
    adjacent bombs (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one bomb
    is visible on the board after digging (i.e. game['mask'][bomb_location] ==
    True), 'victory' when all safe squares (squares that do not contain a bomb)
    and no bombs are visible, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    mask:
        [False, True, True, True]
        [False, False, True, True]
    state: victory

    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: [2, 4]
    mask:
        [True, True, False, False]
        [False, False, False, False]
    state: defeat
    """
    return dig_nd(game,(row,col))
    # #Removed a lot of redundant comments
    # #Removed some redundant cases
    # #Initial victory or defeat cases
    # if game['state'] == 'defeat' or game['state'] == 'victory':
    #     return 0
    # elif game['board'][row][col] == '.':
    #     game['mask'][row][col] = True
    #     game['state'] = 'defeat'
    #     return 1

    # #added a helper function because this action is called on twice
    # bombs,covered_squares = count_bombs_and_squares(game)
    # #Checks for additional Vicotry or defeat cases
    # #If neither, will reveal neighboring tiles
    # if bombs != 0:
    #     game['state'] = 'defeat'
    #     return 0
    # elif covered_squares == 0:
    #     game['state'] = 'victory'
    #     return 0
    # elif game['mask'][row][col] != True:
    #     game['mask'][row][col] = True
    #     revealed = 1
    # else:
    #     return 0

    # if game['board'][row][col] == 0:
    #     num_rows, num_cols = game['dimensions']
    #     for i in range(-1,2): #Changing all the if statements into two for loops that iterate through the tiles neighboring the one of interest
    #         for j in range(-1,2):
    #             if 0 <= row+i < num_rows and 0 <= col+j < num_cols:
    #                 if game['board'][row+i][col+j] != '.' and game['mask'][row+i][col+j] == False:
    #                     revealed += dig_2d(game, row+i, col+j)

    # #Updated win condition to not have to loop to check for bombs again
    # if covered_squares-revealed == 0:
    #     game['state'] = 'victory'
    #     return revealed
    # else:
    #     game['state'] = 'ongoing'
    #     return revealed


def render_2d(game, xray=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares), '.'
    (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring bombs).
    game['mask'] indicates which squares should be visible.  If xray is True (the
    default is False), game['mask'] is ignored and all cells are shown.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['mask']

    Returns:
       A 2D array (list of lists)

    >>> render_2d({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask':  [[False, True, True, False],
    ...                   [False, False, True, False]]}, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render_2d({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask':  [[False, True, False, True],
    ...                   [False, False, False, True]]}, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """
    return render_nd(game,xray)
    # board = game['board']
    # num_rows = game['dimensions'][0]
    # num_cols = game['dimensions'][1]
    # new_board = initialize_board_nd((num_rows,num_cols))
    # for i in range(num_rows): #Iterates through every element on the board
    #     for j in range(num_cols):
    #         value = board[i][j]
    #         new_board[i][j] = value #Updates the copy of the board
    #         if game['mask'][i][j] or xray:
    #             if type(value) == str:
    #                 continue        
    #             elif value == 0:
    #                 new_board[i][j] = ' '
    #             elif value > 0:
    #                 new_board[i][j] = str(value)
    #         else:
    #             new_board[i][j] = '_'
    # return new_board

def render_ascii(game, xray=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function 'render_2d(game)'.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['mask']

    Returns:
       A string-based representation of game

    >>> print(render_ascii({'dimensions': (2, 4),
    ...                     'state': 'ongoing',
    ...                     'board': [['.', 3, 1, 0],
    ...                               ['.', '.', 1, 0]],
    ...                     'mask':  [[True, True, True, False],
    ...                               [False, False, True, False]]}))
    .31_
    __1_
    """
    board = render_nd(game,xray)
    game_str = '' #Creates a string and appends each element on the board to the string
    for row in board: 
        for tile in row:
            game_str+=tile
        game_str+='\n'
    game_str = game_str[:-1] #Removes the last \n
    return game_str

# N-D IMPLEMENTATION

def generate_indices(dimensions):
    '''
    Given the dimensions of the board, returns a list of all coordinates as tuples
    coords = [(x,y,z,...),(x+1,y,z,...)...]
    '''
    if len(dimensions) == 0:
        return [[]]
    dim = dimensions[0]
    indices = []
    for prev_index in generate_indices(dimensions[1:]):
        for i in range(dim):
            indices.append([i]+prev_index)
    return indices



def new_game_nd(dimensions, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'mask' fields adequately initialized.


    Args:
       dimensions (tuple): Dimensions of the board
       bombs (list): Bomb locations as a list of lists, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    mask:
        [[False, False], [False, False], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    state: ongoing
    """
    #Condensed each step of the process into a function and reduced number of lines per process
    board = initialize_board_nd(dimensions)

    for bomb in bombs:
        board = add_bombs_nd(board,bomb)

    mask = initialize_board_nd(dimensions,mask=True)
    
    board = update_bomb_neighbors_nd(board,dimensions,bombs)

    return {
        'dimensions': dimensions,
        'board' : board,
        'mask' : mask,
        'state': 'ongoing'}

def dig_nd(game, coordinates,recurse = False):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the mask to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    bomb.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one bomb is visible on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a bomb) and no bombs are visible, and 'ongoing' otherwise.

    Args:
       coordinates (tuple): Where to start digging

    Returns:
       int: number of squares revealed

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [False, False], [False, False]],
    ...               [[False, False], [False, False], [False, False], [False, False]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    mask:
        [[False, False], [False, True], [True, True], [True, True]]
        [[False, False], [False, False], [True, True], [True, True]]
    state: ongoing
    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [False, False], [False, False]],
    ...               [[False, False], [False, False], [False, False], [False, False]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    mask:
        [[False, True], [False, True], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    state: defeat
    """
    # Checks if dig is on a completed board or revealed tile
    if game['state'] != 'ongoing' or value_of(coordinates, game['mask']):
        return 0
    
    #Checks if a bomb is revealed
    elif value_of(coordinates, game['board']) == '.':           
        game['mask'] = set_value_of(coordinates, game['mask'], True)
        game['state'] = 'defeat'
        return 1
    # reveals a nonzero cell
    revealed = 1
    if value_of(coordinates, game['board']) != 0:
        game['mask'] = set_value_of(coordinates, game['mask'], True)
    # reveals a zero cell
    else:                            
        neighbors = get_neighbors_indices(coordinates, game['dimensions'])
        game['mask'] = set_value_of(coordinates,game['mask'], True)  
        for neighbor in neighbors:
            if value_of(neighbor,game['board']) != '.':
                revealed += dig_nd(game,neighbor,True)
    
    # If ongoing, check if all non bomb cells revealed
    if not recurse and game['state'] == 'ongoing':
        unrevealed = 0
        iterate = generate_indices(game['dimensions'])
        for index in iterate:
            if value_of(index, game['board']) != '.' and not value_of(index, game['mask']):
                unrevealed +=1
        if not unrevealed:
            game['state'] = 'victory'
    return revealed  

def render_nd(game, xray=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares),
    '.' (bombs), ' ' (empty squares), or '1', '2', etc. (squares
    neighboring bombs).  The mask indicates which squares should be
    visible.  If xray is True (the default is False), the mask is ignored
    and all cells are shown.

    Args:
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    the mask

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [True, True], [True, True]],
    ...               [[False, False], [False, False], [True, True], [True, True]]],
    ...      'state': 'ongoing'}
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> render_nd(g, True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """
    new_board = initialize_board_nd(game['dimensions'])
    indices = generate_indices(game['dimensions'])

    for index in indices:
        value = value_of(index,game['board'])
        set_value_of(index,new_board,value) #Updates the copy of the board
        if value_of(index,game['mask']) or xray:
            if type(value) == str:
                continue        
            elif value == 0:
                set_value_of(index,new_board,' ')
            elif value > 0:
                set_value_of(index,new_board,str(value))
        else:
            set_value_of(index,new_board,'_')
    return new_board


if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    import doctest
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags) #runs ALL doctests

    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d or any other function you might want.  To do so, comment
    # out the above line, and uncomment the below line of code. This may be
    # useful as you write/debug individual doctests or functions.  Also, the
    # verbose flag can be set to True to see all test results, including those
    # that pass.
    #
    # doctest.run_docstring_examples(render_2d, globals(), optionflags=_doctest_flags, verbose=False)
    #dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    #game = new_game_nd((2,4,2),[(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    # board = initialize_board_nd((2, 4, 2))
    # print(board)
    # board[0][0][1] = 'x'
    # print(board)
    # board = add_bombs_nd(board,[(0, 0, 1), (1, 0, 0), (1, 1, 1)])

    # print(generate_indices((2,2,2)))
    # print('neighbors',get_neighbors_indices((1,1,1),(2,2,2)))
    #value = value_of((0,0,0),game['board'])
    #set_value_of((0,0,0),game['mask'],True)
    #bombs,covered_squares=count_bombs_and_squares_nd(game)
    #print('bombs',bombs)
    #print('covered squares',covered_squares)
    #dig_nd(game,(0,0,1))
    #print(game)
    #set_value_of((0,0,0),game['board'],10)
    #print('value',value)
    #print('updated game',game)