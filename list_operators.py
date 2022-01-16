def total(a):
    sum = 0
    for i in a:
        sum+=i
    return sum

def none_greater(a, val):
    for i in a:
        if i > val or i < 0:
            return False
    return True

def find_max_indexes(a):
    result_max_index = 0
    result = [0]
    max = a[0]
    for i in range(len(a)):
        if a[i] > max : 
            max = a[i] 
            result[result_max_index] = i
        elif a[i] == max and i != 0: 
            result.append(i) 
            result_max_index+=1
    return result

def find_min_indexes(a):
    result_min_index = 0
    result = [0]
    min = a[0]
    for i in range(len(a)):
        if a[i] < min : 
            min = a[i] 
            result[result_min_index] = i
        elif a[i] == min and i != 0: 
            result.append(i) 
            result_min_index+=1
    return result