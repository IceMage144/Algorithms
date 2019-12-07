# More info https://www.youtube.com/watch?v=kOnEEeHZp94

from random import shuffle

def simulate(num_sims, num_eggs):
    wins = 0
    for sim in range(num_sims):
        lost = False
        eggs = [i for i in range(num_eggs)]
        shuffle(eggs)
        for person in range(num_eggs):
            gone = [False for i in range(num_eggs)]
            egg = eggs[person]
            gone[person] = True
            tries = 0
            while egg != person and tries < 50:
                last_egg = egg
                # while gone[last_egg]:
                #     last_egg = (last_egg + 1) % num_eggs
                egg = eggs[last_egg]
                gone[last_egg] = True
                tries += 1
            if egg != person:
                lost = True
                break
        wins += (not lost)
        if sim % (num_sims // 10) == 0:
            print(f"{100 * sim // num_sims}%")
    print(f"Won {wins} of {num_sims}")


if __name__ == "__main__":
    simulate(100000, 100)