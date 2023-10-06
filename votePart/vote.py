import numpy as np

class Vote:
    def __init__(self) -> None:
        
        self.vote = np.zeros(10)
        self.vote[0] = 1
