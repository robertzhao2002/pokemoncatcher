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