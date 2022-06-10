import random

def calculate_option():
    G = 13
    N = 9
    return (N + G % 60) % 30 + 1


def create_first_relationship(A, B, female_names):
    na = [i for i in A if i in female_names]
    # new a, змінена множина А в якій тільки жіночі ім"я (це матері)
    nb = [i for i in B if i not in na]
    # new a, змінена множина B в якій відсутні ім"я з множини А
    rel_list = []
    limit = 5 if len(na) >= 4 and len(nb) >= 4 else 3
    while len(rel_list) + 1 != limit:
        mother = random.choice(na)
        child = random.choice(nb)
        rel_list.append([mother, child])
        na.remove(mother)
        nb.remove(child)
    return rel_list


def create_second_relationship(A, B, first_list, female_names):
    na = [i for i in A if i in female_names]
    nb = [i for i in B if i not in female_names]
    rel_list = []
    limit = 5 if len(na) >= 4 and len(nb) >= 4 else 3
    while len(rel_list) + 1 != limit:
        law_mother = random.choice(na)
        man = random.choice(nb)
        if not [law_mother, man] in first_list:
            rel_list.append([law_mother, man])
            na.remove(law_mother)
            nb.remove(man)
    return rel_list