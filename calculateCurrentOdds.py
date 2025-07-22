#Calculate current outcome of game based on multiple factors

#Read about Multivariate Hypergeometric Distribution:
from collections import Counter
from scipy.stats import hypergeom
import numpy as np
import matplotlib.pyplot as plt

def estimate_decks_confidence(seen_cards, D_max=10, plot=False):
    card_counts = list(seen_cards.values())
    total_seen = sum(card_counts)
    unique_cards = len(card_counts)
    
    # Unique card definitions in a single deck: 52
    total_card_types = 52 * np.arange(1, D_max + 1)
    
    likelihoods = []
    
    for D in range(1, D_max + 1):
        L = 0
        for count in card_counts:
            # For each unique card, the number of that card in D decks is D
            # Probability of seeing count copies of it in total_seen draws
            # (assumes all cards equally likely)
            M = 52 * D      # total population
            n = D           # number of "successes" in population for this card
            N = total_seen  # number of draws
            k = count       # observed successes
            if k > n or n > M or N > M:
                L += -np.inf
            else:
                L += np.log(hypergeom.pmf(k, M, n, N) + 1e-20)  # avoid log(0)
        likelihoods.append(L)
    
    likelihoods = np.array(likelihoods)
    
    # Convert to relative probabilities
    probs = np.exp(likelihoods - np.max(likelihoods))  # for stability
    probs /= np.sum(probs)

    # Compute confidence interval (e.g., 95%)
    sorted_indices = np.argsort(-probs)
    cumulative = 0
    ci_decks = []
    for i in sorted_indices:
        ci_decks.append(i + 1)
        cumulative += probs[i]
        if cumulative >= 0.95:
            break
    ci_lower, ci_upper = min(ci_decks), max(ci_decks)
    
    mle_decks = np.argmax(probs) + 1

    if plot:
        import matplotlib.pyplot as plt
        plt.bar(range(1, D_max + 1), probs)
        plt.axvline(mle_decks, color='r', linestyle='--', label='MLE')
        plt.title("Estimated Deck Count Distribution")
        plt.xlabel("Number of Decks")
        plt.ylabel("Relative Likelihood")
        plt.legend()
        plt.show()
    
    return {
        "MLE_decks": mle_decks,
        "confidence_interval": (ci_lower, ci_upper),
        "probabilities": probs
    }
