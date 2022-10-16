import random

def estimate_pi(iterations):
    in_counts = 0

    for i in range(iterations):
        x = random.uniform(0,1) - 0.5
        y = random.uniform(0,1) - 0.5
        r_squared = x*x + y*y
        if r_squared < 0.25:
            in_counts += 1

    # area of circle, area_c = pi*r^2 = pi
    # area of square, area_sq = 4
    # ratio_of_counts ~= area_c / area_sq = pi / 4
    # => pi ~= 4 * ratio_of_counts
    estimates = 4 * in_counts/iterations
    return estimates

print(estimate_pi(10000))
