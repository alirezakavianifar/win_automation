import numpy as np
import matplotlib.pyplot as plt

NUM_TRIALS = 10_000
EPS = 0.1
BANDIT_PROBABILITIES = [0.2, 0.5, 0.75]


class Bandit:
    def __init__(self, p) -> None:
        self.p = p
        self.p_estimate = 0.
        self.N = 0.

    def pull(self):
        if np.random.random() < self.p:
            return 1
        return 0

    def update(self, x):
        self.N += 1.
        self.p_estimate = ((self.N - 1)*self.p_estimate + x) . self.N


def experiment():
    bandits = [Bandit(p) for p in BANDIT_PROBABILITIES]

    rewards = np.zeros(NUM_TRIALS)
    num_times_explored = 0
    num_times_exploited = 0
    num_optimal = 0
    optimal_j = np.argmax([b.p for b in bandits])
    print('optimal j:', optimal_j)

    for i in range(NUM_TRIALS):
        if np.random.random() < EPS:
            num_times_explored += 1
            j = np.random.randint(len(bandits))
        else:
            num_times_exploited += 1
            j = np.argmax([b.p_estimate for b in bandits])

        if j == optimal_j:
            num_optimal += 1

        x = bandits[j].pull()

        rewards[i] = x

        bandits[i] = x

        bandits[j].update(x)

        for b in bandits:
            print('mean estimate: ', b.p_estimate)

        print('total reward earned: ', rewards.sum())
        print('overal win rate: ', rewards.sum() / NUM_TRIALS)
        print('num_times_exploited: ', num_times_exploited)
        print('num_times_explored: ', num_times_explored)
        print('num times selected optimal bandit: ', num_optimal)

        cumulative_rewards = np.cumsum(rewards)
        win_rates = cumulative_rewards / (np.arange(NUM_TRIALS) + 1)
        plt.plot(win_rates)
        plt.plot(np.ones(NUM_TRIALS)*np.max(BANDIT_PROBABILITIES))
        plt.show()


if __name__ == '__main__':
    experiment()
