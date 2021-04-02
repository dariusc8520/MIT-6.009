# NO IMPORTS!

##################################################
##  Problem 1
##################################################

def trailing_weighted_average(S, W):
    s_len = len(S)
    w_len = len(W)
    result = []
    for i in range(s_len):
        result.append(calc_weighted_avg(S,W,i))
        #print(result)
    return result
    
def calc_weighted_avg(S,W,i):
    w_len = len(W)
    result = 0.0
    if i == 0:
        result = sum([S[0]*weight for weight in W])
    else:
        weight_index = 0
        while True:
            if weight_index/w_len == 1:
                #print('breaking')
                break
            #print('weight index:',weight_index)
            result += S[i]*W[weight_index]
            #print('result:',result)
            weight_index+=1
            i-=1
            if i<0:
                i=0
    return result


##################################################
##  Problem 2
##################################################

def all_consecutives(vals, n):
    upper_val = max(vals)
    lower_val = min(vals)
    len_of_consev = n
    
    


##################################################
##  Problem 3
##################################################

def cost_to_consume(seq1, seq2):
    raise NotImplementedError


if __name__ == "__main__":
    #print(trailing_weighted_average([1, 2], [0.8, 0.7]))
    #returns [1.5, 2.3]
    print(trailing_weighted_average([1, 5, 6, 7], [1]))
    #returns [1, 5, 6, 7]


	#pass