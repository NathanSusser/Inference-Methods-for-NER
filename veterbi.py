
class Label:

    def __init__(self, label, prev, next, probability):
        self.label = label
        self.prev = prev
        self.next = next
        self.prob = probability

# This is the function you need to implement
def viterbi(tokens, distributions, transitions, labels):
    graph = {0: []}
    for l in labels:
        start_score = transitions[("START", l)] * distributions[0][l]
        node = Label(l, None, None, start_score)
        graph[0].append(node)
        
    for i in range(1, len(tokens)):
        graph[i] = []
        for l in labels:
            curr_round = []
            for lab in graph[i-1]:
                curr_score = lab.prob * transitions[(lab.label, l)] * distributions[i][l]
                seq = get_sequence(lab, [])
                seq.reverse()
                curr_round.append((curr_score, seq, lab))
            sorted_round = sorted(curr_round, key= lambda x: (-x[0], [-ord(c) for label in x[1] for c in label]))       
            node = Label(l, sorted_round[0][2], None, sorted_round[0][0])
            sorted_round[0][2].next = node
            graph[i].append(node)
    final_round = []
    for label in graph[len(tokens)-1]:
        final_score = label.prob * transitions[(label.label,"END")]
        sequen = get_sequence(label, [])
        sequen.reverse()
        final_round.append((final_score, sequen))
    final_sorted = sorted(final_round, key= lambda x: (-x[0], [-ord(c) for label in x[1] for c in label]))
    score = final_sorted[0][0]
    label_sequence = final_sorted[0][1]
    return score, label_sequence

def get_sequence(node, lst):
    if node is None:
        return lst
    else:
        lst.append(node.label)
        return get_sequence(node.prev, lst)



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

answer = viterbi(tokens, distributions, transitions, labels)
if abs(answer[0] - 0.0058482000000000004) > 1e-10:
    print("Error in score")
if ' '.join(answer[1]) != 'LOC O O':
    print("Error in sequence")