def calculate_option():
    G = 13
    N = 9
    return (N + G % 60) % 30 + 1


def not_set(a, u):
    notA = []
    for i in list(u):
        if not (i in list(a)): notA.append(i)
    return set(notA)


def association(a, b):
    la = list(a)
    lb = list(b)
    la.extend(lb)
    return set(la)


def crossing(a, b):
    new_set = [i for i in a if i in list(b)]
    return set(new_set)


def solve_full_equation(step, a, b, c, u):
    step1 = association(a, b)
    step2 = association(a, not_set(b, u))
    step3 = association(step1, step2)
    step4 = crossing(step3, not_set(b, u))
    step5 = crossing(step4, a)
    step6 = association(not_set(a, u), c)
    step7 = crossing(step5, step6)

    steps = [step1, step2, step3, step4, step5, step6, step7]

    return steps[step]


def solve_simplified_equation(step, a, b, c, u):
    step1 = crossing(not_set(b, u), a)
    step2 = crossing(step1, c)
    return step1 if step == 0 else step2
