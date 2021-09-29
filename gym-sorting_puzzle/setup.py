from setuptools import setup

setup(name="gym_sorting_puzzle",
      version="0.0.1",
      author="Eduard Maghakyan",
      license="MIT",
      packages=["gym_sorting_puzzle", "gym_sorting_puzzle.envs"],
      install_requires=["gym", "pygame", "numpy"]
      )
