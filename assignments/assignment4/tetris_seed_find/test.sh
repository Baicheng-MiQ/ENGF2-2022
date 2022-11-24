# for loop from 0 to 10000000
# edit the constants.py file DEFAULT_SEED = that_number
# run visual.py
# save the score like "Score=123" from the std output to a variable
# check if the score in [1083,2334,2766,3150,1647]
# if yes, print the number and the score

for i in {0..10000000}
do
    sed -i "s/DEFAULT_SEED = .*/DEFAULT_SEED = $i/" constants.py
    score=$(python visual.py | grep Score | cut -d'=' -f2)
    if [[ $score == 1083 || $score == 2334 || $score == 2766 || $score == 3150 || $score == 1647 ]]; then
        echo "Score=$score for seed=$i"
    fi
done


