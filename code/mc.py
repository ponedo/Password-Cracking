import random
import pickle
from tqdm import tqdm
from collections import Counter
from sampler import Sampler
from dataset import *

class MarkovChain():

    def __init__(self, order, smooth=False):
        self.order = order
        self.smooth = smooth
        self.trained = False


    def fit(self, ts):
        """
        Count (prefix, next) tuples in corpus.
        Set conditional probabilities according to the counts.
        """
        print("Counting (prefix, next) tuples...")
        self.cond_prob = {}
        for password in tqdm(ts):
            pswd_len = len(password)
            for i in range(pswd_len + 1):
                if i == 0:
                    prefix = "<START>"
                else:
                    prefix_lower_index = max(0, i-self.order)
                    prefix = password[prefix_lower_index : i]
                try:
                    next_ = password[i]
                except IndexError:
                    next_ = "<END>"
                try:
                    self.cond_prob[prefix][next_] += 1
                except KeyError:
                    self.cond_prob[prefix] = Counter()
                    self.cond_prob[prefix][next_] += 1
        print("Normalizing probabilities...")
        for prefix in self.cond_prob:
            prefix_cond_prob = self.cond_prob[prefix]
            prefix_n = sum(prefix_cond_prob.values())
            for next_ in prefix_cond_prob:
                prefix_cond_prob[next_] /= prefix_n

        # TODO here: smoothing

        self.trained = True
        return self

    def generate(self):
        if not self.trained:
            print("This Markov chain is not trained! Please use some dataset to train it first!")
            return
        generated = []
        prefix = "<START>"
        while True:
            # generate next_word according to prefix
            prefix_cond_prob = self.cond_prob[prefix]
            sampler = Sampler()
            sampler.fit(prefix_cond_prob.keys(), prefix_cond_prob.values())
            next_ = sampler.generate()
            generated.append(next_)
            if next_ == "<END>":
                break
            # update prefix
            try:
                prefix = ''.join(generated[-self.order : ])
            except IndexError:
                prefix = ''.join(generated)
        password = ''.join(generated[:-1])
        return password


# if __name__ == "__main__":
    
#     order = 3
#     toy_training_set = load_csdn()

#     print("Training Markov Chain...")
#     mc = MarkovChain(order).fit(toy_training_set)
#     with open("../model/mc" + str(order) + ".pk", "wb") as f:
#         pickle.dump(mc, f)
#     # print(mc.cond_prob)

#     for _ in range(100):
#         generated_password = mc.generate()
#         print(generated_password)
