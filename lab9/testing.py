class GlobalEnv:
    def __init__(self,parent=None):
        self.variables = {}
        self.parent = parent

    def __setitem__(self,key,value):
        self.variables.update({key:value})

    def __getitem__(self,key):
        if key in self.variables:
            return self.variables[key]
        elif self.parent != None:
            try:
                return self.parent[key]
            except:
                raise Exception
        else:
            raise Exception #SnekNameError

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


if __name__ == '__main__':
    # E1 = builtin()
    # print('e1+',E1['+'])
    # print('E1 Var',E1.variables)
    # E2 = GlobalEnv(E1)
    # print('E2 Var',E2.variables)
    # print('E2 +',E2['+'])
    # E3 = GlobalEnv(E2)
    # print('E3 +', E3['+'])
    snek_builtin = builtin()
    env = GlobalEnv(snek_builtin)
    print(env['+'])
    env['x'] = 4
    print(env.variables)
    print('+' in env)

    # G_Env = GlobalEnv()
    # G_Env['hi'] = 'hello'

    # print(G_Env['hi'])
    # G2_env = Global

    