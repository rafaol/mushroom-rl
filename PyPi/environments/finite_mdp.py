import numpy as np

from environment import Environment
from PyPi.utils import spaces


class FiniteMDP(Environment):
    def __init__(self, p, rew, mu=None, gamma=.9):
        self.__name__ = 'FiniteMDP'

        assert p.shape == rew.shape
        assert mu is None or p.shape[0] == mu.size

        # MDP spaces
        self.observation_space = spaces.Discrete(p.shape[0])
        self.action_space = spaces.Discrete(p.shape[1])

        # MDP parameters
        self.horizon = np.inf
        self.gamma = gamma

        # MDP properties
        self.p = p
        self.r = rew
        self.mu = mu

        super(FiniteMDP, self).__init__()

    def reset(self, state=None):
        if state is None:
            if self.mu is not None:
                self._state = np.array(
                    [np.random.choice(self.mu.size, p=self.mu)])
            else:
                self._state = np.array([np.random.choice(self.p.shape[0])])
        else:
            self._state = state

        return self._state

    def step(self, action):
        p = self.p[self._state[0], action[0], :]
        next_state = np.array([np.random.choice(p.size, p=p)])
        absorbing = not np.any(self.p[next_state[0], :, :])
        reward = self.r[self._state[0], action[0], next_state[0]]

        self._state = next_state

        return self._state, reward, absorbing, {}
