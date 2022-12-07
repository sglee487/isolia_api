import random


def generate_random_name() -> str:
    adj_list = []
    with open("utils/korean_adj.txt", "r", encoding='UTF8') as f:
        lines = f.readlines()
        for line in lines:
            adj_list.append(line.strip())

    noun_list = []
    with open("utils/korean_noun.txt", "r", encoding='UTF8') as f:
        lines = f.readlines()
        for line in lines:
            noun_list.append(line.strip())

    return f"{random.choice(adj_list)} {random.choice(noun_list)} {random.randrange(1,100)}"
