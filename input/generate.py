import random

def generate(n_items, n_transactions):
    with open(f'{n_transactions}_trans_{n_items}_items.txt', "w") as f:
        for i in range(n_transactions):
            for j in range(n_items):
                is_true = random.choice([0, 1])
                f.write(str(j*2 + is_true) + " ")
            f.write("\n")
