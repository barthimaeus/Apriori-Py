minsup = 0.02
minconf = 0.8


def read_file(path):
    transactions = []
    with open(path, "r") as f:
        while True:
            line = f.readline()[:-1]
            if line == "":
                break
            transactions.append(frozenset(line.split(",")).difference(frozenset(["fr"])))
    return transactions


def calculate_support(itemset, transactions):
    return float(len([1 for t in transactions if itemset <= t])) / len(transactions)


def compute_hull(supports, transactions):
    i = 1
    while True:
        supports2 = [(k1.union(k2), calculate_support(k1.union(k2), transactions))
                     for k1, _ in supports for k2, _ in supports if len(k1) == i and len(k2) == i and k1 != k2]
        supports2 = list(set([(k, v) for k, v in supports2 if v > minsup]))
        if len(supports2) > 0:
            supports = supports + supports2
            i *= 2
        else:
            break
    return supports


def generate_rules(supports):
    prules = {k: v for k, v in supports.items() if len(k) > 1}
    rules = []
    for s in prules:
        for cons in s:
            conf = supports[s] / supports[s.difference([cons])]
            if conf > minconf:
                rules.append((round(conf, 2), list(s.difference([cons])), cons ))
    return sorted(rules, reverse=True)

if __name__ == "__main__":
    print "Reading file"
    transactions = read_file("extract.csv")

    print "Calculate initial support values"
    items = [frozenset([i]) for i in reduce(lambda x, y: x.union(y), transactions)]
    supports = [(k, calculate_support(k, transactions)) for k in items]
    supports = [(k, v) for k, v in supports if v > minsup]

    print "Compute hull"
    supports = dict(compute_hull(supports, transactions))

    print "Generate Rules"
    rules = generate_rules(supports)
    for rule in rules:
        print "Rule(%s): %s -> %s" % rule

