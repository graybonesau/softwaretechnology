def MergeSort(array, draw_fn, wait_fn, event_fn):
    if not _merge_sort_recursive(array, 0, len(array) - 1, draw_fn, wait_fn, event_fn):
        return False
    draw_fn(array, compare=[], swap=[], sorted_up_to=0)
    return True


def _merge_sort_recursive(array, left, right, draw_fn, wait_fn, event_fn):
    if left >= right:
        return True

    mid = (left + right) // 2

    if not _merge_sort_recursive(array, left, mid, draw_fn, wait_fn, event_fn):
        return False
    if not _merge_sort_recursive(array, mid + 1, right, draw_fn, wait_fn, event_fn):
        return False
    if not _merge(array, left, mid, right, draw_fn, wait_fn, event_fn):
        return False

    return True


def _merge(array, left, mid, right, draw_fn, wait_fn, event_fn):
    left_part  = array[left:mid + 1]
    right_part = array[mid + 1:right + 1]

    i = j = 0
    k = left

    while i < len(left_part) and j < len(right_part):
        draw_fn(array, compare=[left + i, mid + 1 + j], swap=[], sorted_up_to=None)
        wait_fn(30)
        if not event_fn():
            return False

        if left_part[i] <= right_part[j]:
            array[k] = left_part[i]
            i += 1
        else:
            array[k] = right_part[j]
            j += 1

        draw_fn(array, compare=[], swap=[k], sorted_up_to=None)
        wait_fn(30)
        if not event_fn():
            return False
        k += 1

    while i < len(left_part):
        array[k] = left_part[i]
        draw_fn(array, compare=[], swap=[k], sorted_up_to=None)
        wait_fn(30)
        if not event_fn():
            return False
        i += 1
        k += 1

    while j < len(right_part):
        array[k] = right_part[j]
        draw_fn(array, compare=[], swap=[k], sorted_up_to=None)
        wait_fn(30)
        if not event_fn():
            return False
        j += 1
        k += 1

    return True