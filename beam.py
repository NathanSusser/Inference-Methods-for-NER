from collections import defaultdict

def beam(tokens, distributions, transitions, labels, k):
    score_seq = [(1, ["START"])]  # Start with initial score and initial sequence

    for w in range(1, len(tokens)+1):  # +1 to handle the final transition to "END"
        curr_round = []
        for curr_score, curr_seq in score_seq:
            for l in labels:
                # Copy the current sequence to avoid modifying the original
                new_seq = curr_seq.copy()
                new_seq.append(l)
                
                # Calculate the new score based on the previous label and the current label
                new_score = curr_score
                new_score *= distributions[w-1].get(l, 0)  # Use the distribution at index w-1
                new_score *= transitions.get((curr_seq[-1], l), 0)  # Transition from the last element of curr_seq to l
                
                # Add the new score and sequence to the current round
                curr_round.append((new_score, new_seq))
        
        # Sort and select the top k sequences
        sorted_round = sorted(curr_round, key=lambda x: (-x[0], [-ord(c) for label in x[1] for c in label]))
        score_seq = sorted_round[:k]

    # Final transition to "END"
    final_scores = []
    for curr_score, curr_seq in score_seq:
        end_score = curr_score * transitions.get((curr_seq[-1], "END"), 0)
        curr_seq.append("END")
        final_scores.append((end_score, curr_seq))

    final_sorted = sorted(final_scores, key=lambda x: (-x[0], [-ord(c) for label in x[1] for c in label]))
    score = final_sorted[0][0]
    label_sequence = final_sorted[0][1]
    return score, label_sequence[1:-1]

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
k = 5

answer = beam(tokens, distributions, transitions, labels, k)
print("Score:", answer[0])
print("Sequence:", ' '.join(answer[1]))
