"""
Removes empty lines from the front and back of the list
"""
def stripEnds(l):
    empties = ['\n', '']
    for i in range(len(l)):
        if l[i] not in empties:
            break
    
    for j in reversed(range(len(l))):
        if l[j] not in empties:
            break

    return l[i:j+1]