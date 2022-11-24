# for loop from 0 to 10000000
# edit the constants.py file DEFAULT_SEED = that_number
# run visual.py
# save the score like "Score= 123" from the std output to a variable
# check if the score in [1083,2334,2766,3150,1647]
# if yes, print the number and the score

import subprocess
from tqdm import tqdm


for i in tqdm(range(10000000)):
    with open("constants.py", "r") as f:
        lines = f.readlines()
    lines[4] = "DEFAULT_SEED = {}\n".format(i)
    with open("constants.py", "w") as f:
        f.writelines(lines)

    output = subprocess.check_output(["python", "visual.py"])
    last_line = output.splitlines()[-2]
    score = int(last_line.split()[-1])
    # print(score)
    if score in [1083,2334,2766,3150,1647]:
        print("number: ", i)
        print("score: ", score)
        print("==========")