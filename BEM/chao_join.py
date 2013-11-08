
def gap(gap_length, gapopen, gapextend):
    '''Calculates the gap penalty on opening a gap o lenght gap_length'''
    return gapopen + (gap_length * gapextend)


def calc_diagonals(checker, checked):
    '''Calculates the diagonal of two fragments.

    Diagonals are roughly the points where the fragments starts referred to
    the query match points.
    '''
    checker = checker.split()
    checked = checked.split()

    if (checker[8] == "C"):
        diagonal_checker = int(checker[5]) + int(checker[11])
        diagonal_checked = int(checked[5]) + int(checked[11])
    else:
        diagonal_checker = int(checker[5]) - int(checker[10])
        diagonal_checked = int(checked[5]) - int(checked[10])

    return diagonal_checker, diagonal_checked


def calc_penalty(checker, checked, mismatch, gapopen, gapextend):
    '''Estimates the penalty of joining the fragment checker with checked.
    '''
    #First calculate the diagonals
    diagonal_checker, diagonal_checked = calc_diagonals(checker, checked)

    #Calculate the length of the match
    module = checked[6] - checked[5]

    if diagonal_checker == diagonal_checked:
        if (checker[8] == "C"):
            penalty = ((checker[10] - checked[10] - module) * mismatch)
        else:
            penalty = ((checked[10] - checker[10] - module) * mismatch)
    elif diagonal_checker > diagonal_checked:
        penalty = gap(
            diagonal_checked - diagonal_checker, gapopen, gapextend) +\
            abs((checker[10] - checked[10] - module) * mismatch)

    return penalty


def is_joinable(checker, checked, mismatch, gapopen, gapextend):
    '''Tests if a couple of matches are joinable.

    To be joinable, two matches must:
    - Be in the same chromosome.
    - Be a match of the same query.
    - Be in the sane direction.'''

    penalty = calc_penalty(checker, checked, mismatch, gapopen, gapextend)

    if (penalty < min(checked[0], checker[0]) and  # cost to join
            checked[4] == checker[4] and  # same chromosome
            checked[9] == checker[9] and  # same query
            checked[8] == checker[8]):  # same direction

        return True
    else:
        return False
