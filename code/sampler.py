import random

class Sampler():
    """
    >>> abc_sampler = Sampler()
    >>> X = ['a', 'b', 'c']
    >>> y = [0.23, 0.44, 0.33]
    >>> abc_sampler.fit(X, y)
    >>> abc_sampler.generate()
    >>> [abc_sampler.generate() for _ in range(20)]
    could get 'a', 'b', or 'c', with probability of 0.23, 0.44, 0.33, respectively.
    """
    def __init__(self):
        self.trained = False
    
    def fit(self, X, y):
        """
        param X: entities to be sampled.
        param y: probability of being sampled for each entity in X.
        """
        self.entities = X
        pdf = y       # pdf: probability distrubution fuction
        self.cdf = [] # cdf: cumulative distrubution fuction
        cd = 0
        for pd in pdf:
            cd += pd
            self.cdf.append(cd)
        self.trained = True
        return self

    def generate(self):
        """
        Generate a sample from entities according to their probability distribution.
        """
        if not self.trained:
            print("This sampler is not trained! Please use some dataset to train it first!")
            return
        rand_float = random.random()
        for entity, cd in zip(self.entities, self.cdf):
            if cd > rand_float:
                return entity
        print("Some error occured!")
        return

