import itertools

# This is the function you need to implement
def exhaustive(tokens, distributions, transitions, labels):
    score = float('-inf')
    score_seq = {}
    all_sequences = itertools.product(labels, repeat=len(tokens)) # create the possible label combinations
    #loop through all the possible sequences to get the scores
    for sequence in all_sequences:
        # score for start
        score_curr = transitions[("START", sequence[0])]
        score_curr *= distributions[0][sequence[0]]
        #score for rest of sequence
        for i in range(1, len(tokens)):
            score_curr *= transitions[(sequence[i-1], sequence[i])]
            score_curr *= distributions[i][sequence[i]]
        #score for end
        score_curr*= transitions[(sequence[-1], "END")]
        #add to dictonary
        if score_curr not in score_seq:
            score_seq[score_curr] = []
        score_seq[score_curr].append(sequence)
    #sort all the scores
    sorted_scores = sorted(score_seq.items(), key=lambda x: (-x[0], sorted(x[1], reverse=True)))
    score = sorted_scores[0][0]
    label_sequence=sorted_scores[0][1][0]
    return score, label_sequence

# Sample data test
tokens = ["Sydney", "is", "nice"]
distributions = [
    {"LOC": 0.9, "O": 0.1},
    {"LOC": 0.05, "O": 0.95},
    {"LOC": 0.05, "O": 0.95},
]
transitions = {
    ("START", "O"): 0.8,
    ("START", "LOC"): 0.2,
    ("START", "END"): 0.0,
    ("O", "END"): 0.05,
    ("O", "O"): 0.9,
    ("O", "LOC"): 0.05,
    ("LOC", "END"): 0.05,
    ("LOC", "O"): 0.8,
    ("LOC", "LOC"): 0.2,
}
labels = {"LOC", "O"}

answer = exhaustive(tokens, distributions, transitions, labels)
if abs(answer[0] - 0.0058482000000000004) > 1e-10:
    print("Error in score")
if ' '.join(answer[1]) != 'LOC O O':
    print("Error in sequence")