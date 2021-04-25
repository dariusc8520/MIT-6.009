import doctest

# NO ADDITIONAL IMPORTS ALLOWED!
# You are welcome to modify the classes below, as well as to implement new
# classes and helper functions as necessary.


class Symbol:
    #Redefining dunder methods
    def __add__(self, other):
        return Add(self, other)
    def __radd__(self, other):
        if type(other) == int:
            return Add(Num(other), self)
        else:
            return Add(Var(other), self)

    def __sub__(self, other):
        return Sub(self, other)
    def __rsub__(self, other):
        if type(other) == int:
            return Sub(Num(other), self)
        else:
            return Sub(Var(other), self)

    def __mul__(self, other):
        return Mul(self, other)
    def __rmul__(self, other):
        if type(other) == int:
            return Mul(Num(other), self)
        else:
            return Mul(Var(other), self)

    def __truediv__(self, other):
        return Div(self, other)
    def __rtruediv__(self, other):
        if type(other) == int:
            return Div(Num(other), self)
        else:
            return Div(Var(other), self)


class Var(Symbol):
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `name`, containing the
        value passed in to the initializer.
        """
        self.name = n

    precedence = 0

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Var(' + repr(self.name) + ')'

    def deriv(self, variable):
        '''
        d/dx x = 1
        d/dy x = 0
        '''
        if variable == self.name:
            return Num(1)
        else:
            return Num(0)

    def simplify(self):
        return Var(self.name)

    def eval(self, mapping):
        if self.name in mapping:
            return mapping[self.name]
        else:
            return self
    

class Num(Symbol):
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `n`, containing the
        value passed in to the initializer.
        """
        self.n = n

    precedence = 0

    def __str__(self):
        return str(self.n)

    def __repr__(self):
        return 'Num(' + repr(self.n) + ')'

    def deriv(self, variable):
        '''
        d/dx c = 0
        '''
        return Num(0)
    
    def simplify(self):
        return Num(self.n)

    def eval(self,mapping):
        return self.n

class BinOp(Symbol):
    def __init__(self,left,right):
        '''
        Initializes the Binary Operation and instances of left and right
        '''
        #Checks if left is str or num or symbol and initializes accordingly
        if type(left) == str:
            self.left = Var(left)
        elif type(left) == int:
            self.left = Num(left)
        else:
            self.left = left
        #Checks if right is str or num or symbol and initializes accordingly
        if type(right) == str:
            self.right = Var(right)
        elif type(right) == int:
            self.right = Num(right)
        else:
            self.right = right

    def simplify(self):
        simplified_left = self.left.simplify()
        simplified_right = self.right.simplify()
        return self.simplify_helper(simplified_left,simplified_right)

class Add(BinOp):
    def __init__(self, left, right):
        BinOp.__init__(self,left,right)
    
    precedence = 1

    def __str__(self):
        '''
        >>> 2 + Var('x')
        Add(Num(2),Var('x'))
        '''
        # x + y
        return str(self.left) + ' ' + '+' + ' ' + str(self.right)

    def __repr__(self):
        '''
        Returns the representation of the equation
        '''
        return 'Add' + '(' + repr(self.left) + ',' + repr(self.right) + ')'
    
    def deriv(self, variable):
        '''
        d/dx (u+v) = d/dx u + d/dx v
        '''
        return self.left.deriv(variable) + self.right.deriv(variable)

    def simplify_helper(self,simplified_left,simplified_right):
        '''
        x + 0 = x or 0 + x = x
        '''
        if isinstance(simplified_left,Num) and isinstance(simplified_right, Num):
            return Num(simplified_left.n + simplified_right.n)

        if isinstance(simplified_left, Num) and simplified_left.n == 0:
            return simplified_right

        if isinstance(simplified_right, Num) and simplified_right.n == 0:
            return simplified_left

        return Add(simplified_left,simplified_right)
                
    def eval(self, mapping):
        return self.left.eval(mapping) + self.right.eval(mapping)

class Sub(BinOp):
    def __init__(self, left, right):
        BinOp.__init__(self,left,right)

    precedence = 1

    def __str__(self):
        # x - (y + z) or x - (y - z) #Special Case
        if self.right.precedence == 1:
            return str(self.left) + ' ' + '-' + ' (' + str(self.right) + ')'

        # x - y
        else:
            return str(self.left) + ' ' + '-' + ' ' + str(self.right)

    def __repr__(self):
        '''
        Returns the representation of the equation
        '''
        return 'Sub'+ '(' + repr(self.left) + ',' + repr(self.right) + ')'

    def deriv(self, variable):
        '''
        d/dx (u-v) = d/dx u - d/dx v
        '''
        return self.left.deriv(variable) - self.right.deriv(variable)

    def simplify_helper(self,simplified_left,simplified_right):
        '''
        x - 0 = x
        '''
        if isinstance(simplified_left,Num) and isinstance(simplified_right, Num):
            return Num(simplified_left.n - simplified_right.n)

        if isinstance(simplified_right, Num) and simplified_right.n == 0:
            return simplified_left
            
        return Sub(simplified_left,simplified_right)

    def eval(self, mapping):
        return self.left.eval(mapping) - self.right.eval(mapping)

class Mul(BinOp):
    def __init__(self, left, right):
        BinOp.__init__(self,left,right)

    precedence = 2

    def __str__(self):
        '''
        >>> Var('a') * Var('b')
        Mul(Var('a'),Var('b'))
        '''
        # (x + y) * (a + b) ...
        if self.left.precedence == 1 and self.right.precedence == 1:
            return '(' + str(self.left) + ') ' + '*' + ' (' + str(self.right) + ')'

        # (x + y) * z or (x - y) * z
        elif self.left.precedence == 1:
            return '(' + str(self.left) + ') ' + '*' + ' ' + str(self.right)
        
        # x * (y + z) or x * (y - z)
        elif self.right.precedence == 1:
            return str(self.left) + ' ' + '*' + ' (' + str(self.right) + ')'

        # x * y 
        else:
            return str(self.left) + ' ' + '*' + ' ' + str(self.right)

    def __repr__(self):
        '''
        Returns the representation of the equation
        '''

        return 'Mul' + '(' + repr(self.left) + ',' + repr(self.right) + ')'

    def deriv(self, variable):
        '''
        d/dx (u*v) = u (d/dx v) + v (d/dx u)
        '''
        return  self.left * self.right.deriv(variable) + self.right * self.left.deriv(variable) 

    def simplify_helper(self,simplified_left,simplified_right):
        '''
        x * 1= x
        x * 0 = 0
        '''
        if (isinstance(simplified_left, Num) and simplified_left.n == 0) or (isinstance(simplified_right, Num) and simplified_right.n == 0):
            return Num(0)

        if isinstance(simplified_left,Num) and isinstance(simplified_right, Num):
            return Num(simplified_left.n * simplified_right.n)

        if isinstance(simplified_left, Num) and simplified_left.n == 1:
            return simplified_right

        if isinstance(simplified_right, Num) and simplified_right.n == 1:
            return simplified_left
            
        return Mul(simplified_left,simplified_right)

    def eval(self, mapping):
        return self.left.eval(mapping) * self.right.eval(mapping)

class Div(BinOp):
    def __init__(self, left, right):
        BinOp.__init__(self,left,right)

    precedence = 2
    
    def __str__(self):
        '''
        >>> Num(3) / 2
        Div(Num(3),Num(2))
        '''
        if self.right.precedence > 0:
            #(x + y) / (a * b) or (x + y) / (a / b) or (x - y) / (a * b) or (x - y) / (a / b)
            if self.left.precedence == 1:
                return '(' + str(self.left) + ') ' + '/' + ' (' + str(self.right) + ')'

            # x / (y + z) or x / (y - z) or x / (y * z) or x / (y / z) #Special Case
            else:
                return str(self.left) + ' ' + '/' + ' (' + str(self.right) + ')'

        # (x + y) / z or (x - y) / z
        elif self.left.precedence == 1:
            return '(' + str(self.left) + ') ' + '/' + ' ' + str(self.right)
        
        # x / y
        else:
            return str(self.left) + ' ' + '/' + ' ' + str(self.right)

    def __repr__(self):
        '''
        Returns the representation of the equation
        '''
        return 'Div' + '(' + repr(self.left) + ',' + repr(self.right) + ')'

    def deriv(self,variable):
        '''
        d/dx (u/v) = (v * d/dx u - u *d/dx v) / (v * v)
        '''
        return (self.right * self.left.deriv(variable) - self.left * self.right.deriv(variable)) / (self.right * self.right)

    def simplify_helper(self,simplified_left,simplified_right):
        '''
        x / 1 = x
        0 / x = 0
        '''
        if isinstance(simplified_left,Num) and isinstance(simplified_right, Num):
            return Num(simplified_left.n / simplified_right.n)

        if isinstance(simplified_right, Num) and simplified_right.n == 1:
            return simplified_left

        if isinstance(simplified_left, Num) and simplified_left.n == 0:
            return Num(0)

        return Div(simplified_left, simplified_right)

    def eval(self, mapping):
        return self.left.eval(mapping) / self.right.eval(mapping)

## HELPER FUNCTIONS ##
def tokenize(text):
    '''
    Tokenizes a text by taking in a string and outputing meaningful tokens and removes spaces
    Tokens can be (,),+,-,*,/,Num or Var
    >>> tokenize("(x * (2 + 3))")
    ['(', 'x', '*', '(', '2', '+', '3', ')', ')']
    >>> tokenize("(x * (200 + 3))")
    ['(', 'x', '*', '(', '200', '+', '3', ')', ')']
    >>> tokenize('x - -300')
    ['x', '-', '-300']
    '''
    tokenized_text = []
    number = ''
    for i in range(len(text)):
        if text[i] != ' ':
            if text[i] in '()':
                tokenized_text.append(text[i])
            else:
                number = number + text[i]
                if i == len(text)-1 or (i < len(text) -1 and not text[i+1].isnumeric()):
                    tokenized_text.append(number)
                    number = ''

    return tokenized_text

def parse(tokens):
    '''
    Given a string of tokens, creates a symbollic expression
    '''

    def parse_expression(index):
        '''
        Recursively parses the tokens given an integer index
        '''
        token = tokens[index]

        if token.isalpha():
            return Var(token), index + 1

        elif token.isnumeric():
            return Num(int(token)), index + 1
        
        elif token[0] == '-':
            return Num(int(token)), index + 1

        elif token == '(': #token == '('
            #E1 op E2
            E1, op_index = parse_expression(index + 1) #Finds E1 and operator index
            op = tokens[op_index]
            E2, next_index = parse_expression(op_index + 1) #Finds E2 and the index after

            #Returns the parsed operator expression
            if op == '+':
                return Add(E1, E2), next_index + 1
            elif op == '-':
                return Sub(E1, E2), next_index + 1
            elif op == '*':
                return Mul(E1, E2), next_index + 1
            elif op == '/':
                return Div(E1, E2), next_index + 1

    parsed_expression, last_index = parse_expression(0)

    return parsed_expression

def sym(string):
    tokens = tokenize(string)
    return parse(tokens)

if __name__ == '__main__':
    # print(tokenize("(x * (200 + 3))"))
    # print(tokenize('x - -300'))
    doctest.testmod()
