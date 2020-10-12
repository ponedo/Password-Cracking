import random
import pickle
import numpy as np
from tqdm import tqdm
from sampler import Sampler
from dataset import *


class HMM4():
    """
    When fitted, useful member variables will include:
        self.states, self.IS, self.SS, self.OB, self.LD
    MEMO: 
        HMM4的问题是，一不能利用字符级别的上下文，二没有个人信息
        改进方向一：使用n-gram改进
        改进方向二：看一看targeted Markov
        这专利8太行，害得重新看看HMM思索一下
    """
    def __init__(self):
        ### define hidden states
        self.states = {
            0: "letter", 
            1: "number", 
            2: "char"
        }
        self.trained = False

    def fit(self, ts):
        """
        param ts: training set
        output states: hidden states
        output IS: initial state matrix
        output SS: state shift matrix
        output OB: observation matrix
        output LD: length distribution
        """
        ts_n = len(ts)
        states_n = len(self.states)
        def stateof(s):
            """
            封装一下每个hidden state的判断条件，以后就改这里就完事了
            """
            if s.isalpha():
                return 0
            elif s.isdigit():
                return 1
            elif not s.isalnum():
                return 2
        def isstate(s, state):
            return stateof(s) == state

        ### Count initial state distribution
        print("Counting initial state distribution...")
        self.IS = np.zeros(states_n)
        for password in tqdm(ts):
            init_state = stateof(password[0])
            self.IS[init_state] += 1
        self.IS /= ts_n
        
        ### Count 1-gram state shift situation
        print("Counting 1-gram state shift situation...")
        self.SS = np.zeros((states_n, states_n))
        for password in tqdm(ts):
            pswd_n = len(password)
            for i in range(pswd_n - 1):
                self.SS[stateof(password[i]), stateof(password[i+1])] += 1
        for state in self.states:
            self.SS[state] /= sum(self.SS[state])

        ### Count observation probability
        print("Counting observation probability...")
        self.OB = {}
        for state in self.states:
            self.OB[state] = {}
        for password in tqdm(ts):
            for ob in password:
                state_OB = self.OB[stateof(ob)]
                state_OB[ob] = state_OB.get(ob, 0) + 1
        for state in self.states:
            state_OB = self.OB[state]
            state_ob_count = sum(state_OB.values())
            for ob in state_OB:
                state_OB[ob] /= state_ob_count

        ### Count length distribution
        print("Counting length distribution...")
        self.LD = {}
        for password in tqdm(ts):
            l = len(password)
            self.LD[l] = self.LD.get(l, 0) + 1
        for k in self.LD:
            self.LD[k] /= ts_n

        ### Setting samplers
        print("Setting samplers...")
        self.length_sampler = Sampler().fit(
            list(self.LD.keys()), list(self.LD.values())
            )
        self.IS_sampler = Sampler().fit(
            list(self.states.keys()), list(self.IS)
            )
        self.SS_samplers = [Sampler().fit(
            list(self.states.keys()), list(self.SS[state])) 
            for state in self.states]
        self.OB_samplers = [Sampler().fit(
            list(self.OB[state].keys()), list(self.OB[state].values())) 
            for state in self.states]

        self.trained = True
        return self

    def generate(self):
        if not self.trained:
            print("This HMM is not trained! Please use some dataset to train it first!")
            return
        length = self.length_sampler.generate()
        cur_state = self.IS_sampler.generate()
        tmp_password = ""
        for _ in range(length):
            observation = self.OB_samplers[cur_state].generate()
            tmp_password += observation
            cur_state = self.SS_samplers[cur_state].generate()
        return tmp_password


# if __name__ == "__main__":

#     toy_training_set = load_csdn()

#     print("Training HMM4...")
#     hmm4 = HMM4().fit(toy_training_set)
#     with open("../model/hmm4.pk", "wb") as f:
#         pickle.dump(hmm4, f)

#     # Generate passwords
#     print("Password generated: ")
#     for _ in range(100):
#         generated_password = hmm4.generate()
#         print(generated_password)