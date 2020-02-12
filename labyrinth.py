from collections import OrderedDict

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator
from tqdm import tqdm


class OrderedSet(OrderedDict):
    def add(self, val):
        self[val] = None


class Labyrinth:
    DIR = {
        "N": np.array([0, 1]),
        "W": np.array([-1, 0]),
        "S": np.array([0, -1]),
        "E": np.array([1, 0]),
    }
    
    lefts = {
        # Current `dr`: `dr` after rotating 90 degrees ccw
        "N": "W", "W": "S", "S": "E", "E": "N"
    }
    rights = {
        # Current `dr`: `dr` after rotating 90 degrees cw
        "N": "E", "E": "S", "S": "W", "W": "N"
    }

    def __init__(self, *nums, lean_left=False):
        self.r = np.array([0, 0])
        self.lean_left = lean_left
        self.orientation = "E" if lean_left else "W" # go up first
        self.nums = nums
        self.visited = OrderedSet()
        self.switches = OrderedSet()
        self.visited.add(tuple(self.r))
        
        # Run
        self.success = self.run()
        self.plot()
    
    def __repr__(self):
        return ""
    
    @property
    def dr(self) -> "ndarray":
        return self.DIR[self.orientation]
    
    def run(self) -> bool:
        with tqdm(total=sum(self.nums)) as pbar:
            for n in self.nums:
                for i in range(n):
                    if not self.try_move():
                        return False
                    pbar.update(1)
                self.switches.add(tuple(self.r))
                self.switch()
        return True

    def try_move(self) -> bool:
        tries = [self.lefts[self.orientation], self.orientation, self.rights[self.orientation]]
        if not self.lean_left:
            tries = tries[::-1]
        o = None
        for orientation in tries:
            if tuple(self.r + self.DIR[orientation]) in self.visited:
                continue
            o = orientation
            break
        if o is None:
            return False
        self.orientation = o
        self.r += self.dr
        self.visited.add(tuple(self.r))
        return True
    
    def switch(self):
        self.lean_left = not self.lean_left
    
    @property
    def start(self):
        for pt in self.visited:
            return pt
    
    @property
    def end(self):
        return next(reversed(self.visited))
    
    def plot(self):
        fig, ax = plt.subplots()
        
        # Plot
        ax.plot(*zip(*self.visited))
        ax.scatter(*self.start, s=200, marker="^")
        ax.scatter(*zip(*self.switches))
        sym, col = ("*", "green") if self.success else ("x", "red")
        ax.scatter(*self.end, s=400, marker=sym, c=col)
        
        # Figure
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.grid()
        plt.show()