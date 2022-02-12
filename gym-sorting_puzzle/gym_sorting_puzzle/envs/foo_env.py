from cmath import inf
import gym
from gym import error, spaces, utils
from gym.utils import seeding
from montesori_env import PuzzleView

class FooEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.puzzle = PuzzleView()

    def step(self, action):
        player_id = action[0]
        direction = action[1]
        player = [p for p in self.puzzle.play_tiles if p.id == player_id]
        player = player.pop() if len(player) > 0 else None

        self.puzzle.move(player, direction)


        self.state = self.maze_view.robot

        info = {}

        reward = 0 # calculate reward

        return self.state, reward, self.puzzle.done, info

    def reset(self):
        self.puzzle.reset()

    def render(self, mode='human'):
        return self.puzzle.update(mode)

    def close(self):
        self.puzzle.quit()
