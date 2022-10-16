from random import random


def estimate_pi(precision):
    N_hits = 0
    N_tot = 0
    centreX = 0.5
    centreY = 0.5
    for i in range(2**precision):
        thisRandX = random()
        thisRandY = random()
        distanceToCentre = ((thisRandX-centreX)**2 + (thisRandY-centreY)**2)**0.5
        if distanceToCentre < 0.5:
            # if in circle
            N_hits += 1
        N_tot += 1
    est_pi = (N_hits/N_tot)*4
    print(round(est_pi,precision))


if __name__ == "__main__":
    estimate_pi(10)