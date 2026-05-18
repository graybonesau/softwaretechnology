def BubbleSort(array, draw_fn, wait_fn, event_fn):
    n = len(array)
    for i in range(n):
        sorted_from = n - i
        for j in range(0, n - i - 1):
            draw_fn(array, compare=[j, j + 1], swap=[], sorted_up_to=sorted_from)
            wait_fn(40)
            if not event_fn():
                return False

            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                draw_fn(array, compare=[], swap=[j, j + 1], sorted_up_to=sorted_from)
                wait_fn(40)
                if not event_fn():
                    return False

    draw_fn(array, compare=[], swap=[], sorted_up_to=0)
    return True