# def indicies(board, tuple):
#     l = list(tuple)
#     while len(l) > 0:
#         board = board[l[0]]
#         del l[0]
#         # now ur at the point you want to be

# indicies(board, [1,2,2,2])

def cart_product_1(result,*seqs):
    if not seqs:
        return [[]]
    else:
        result = []
        for x in seqs[0]:                 
            for p in cart_product_1(result,*seqs[1:]):
                 result.append([x]+p)
        return result

if __name__ == "__main__":
    seq = (-1,0,1)*3
    print(cart_product_1([],))