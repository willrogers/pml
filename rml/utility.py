def binary_search(elements, pv_id):
    first = 0
    last = len(elements)-1
    found = False

    while first <= last and not found:
        midpoint = (first + last)//2
        if elements[midpoint].identity == pv_id:
            found = midpoint
        else:
            if pv_id < elements[midpoint].identity:
                last = midpoint-1
            else:
                first = midpoint+1

    return found
