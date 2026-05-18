def SelectionSort(array, draw_fn, wait_fn, event_fn):
    n = len(array)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            draw_fn(array, compare=[min_idx, j], swap=[], sorted_up_to=i)
            wait_fn(40)
            if not event_fn():
                return False
            if array[j] < array[min_idx]:
                min_idx = j

        if min_idx != i:
            array[i], array[min_idx] = array[min_idx], array[i]
            draw_fn(array, compare=[], swap=[i, min_idx], sorted_up_to=i)
            wait_fn(40)
            if not event_fn():
                return False

    draw_fn(array, compare=[], swap=[], sorted_up_to=0)
    return True