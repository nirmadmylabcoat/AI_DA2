import random
from collections import Counter

PROB_A = {"yes": 0.8, "no": 0.2}
PROB_C = {"yes": 0.5, "no": 0.5}

PROB_G_COND_AC = {
    ("yes", "yes"): {"Good": 0.9, "OK": 0.1},
    ("yes", "no"): {"Good": 0.7, "OK": 0.3},
    ("no", "yes"): {"Good": 0.6, "OK": 0.4},
    ("no", "no"): {"Good": 0.3, "OK": 0.7},
}

PROB_J_COND_G = {
    "Good": {"yes": 0.8, "no": 0.2},
    "OK": {"yes": 0.2, "no": 0.8},
}

PROB_S_COND_G = {
    "Good": {"yes": 0.7, "no": 0.3},
    "OK": {"yes": 0.3, "no": 0.7},
}

def draw_sample(prob_distribution):

    threshold = random.random()
    cumulative_prob = 0
    for outcome, probability in prob_distribution.items():
        cumulative_prob += probability
        if threshold <= cumulative_prob:
            return outcome

def create_sample():

    a_value = draw_sample(PROB_A)
    c_value = draw_sample(PROB_C)
    g_value = draw_sample(PROB_G_COND_AC[(a_value, c_value)])
    j_value = draw_sample(PROB_J_COND_G[g_value])
    s_value = draw_sample(PROB_S_COND_G[g_value])
    return {"A": a_value, "C": c_value, "G": g_value, "J": j_value, "S": s_value}

def estimate_probability(target_node, evidence, sample_count=10000):

    valid_samples = []

    for _ in range(sample_count):
        sample = create_sample()
        if all(sample[ev_var] == ev_val for ev_var, ev_val in evidence.items()):
            valid_samples.append(sample[target_node])

    if valid_samples:
        counts = Counter(valid_samples)
        total_samples = len(valid_samples)
        return {outcome: count / total_samples for outcome, count in counts.items()}
    else:
        return None

observed_evidence = {"A": "yes", "C": "yes"}
target_variable = "J"

samples = 10000
inferred_probs = estimate_probability(target_variable, observed_evidence, samples)
print(f"Inferred probabilities:\n\tFor {target_variable}:\n\tGiven evidence {observed_evidence}: {inferred_probs}")
