import random
import pickle
import numpy as np
from tqdm import tqdm
from sampler import Sampler
from dataset import *


class PCFG():
    """
    When fitted, useful member variables will include:
        self.states, self.IS, self.SS, self.OB, self.LD
    TODO:
        pcfg 对于L(Alpha)，可以考虑引入大小写敏感的因素
        pcfg 无法自动选择pattern，需要手动指定或使用默认
    """
    def __init__(self):
        ### define hidden states
        
        self.trained = False

    def fit(self, ts):
        """
        param ts: training set
        output PP: Pattern Probability
        output FG: Fragment 
        """
        ts_n = len(ts)
        #states_n = len(self.states)
        def stateof(ch):
            if ((ord(ch) >= ord('A') and ord(ch) <= ord('Z')) or 
                (ord(ch) >= ord('a') and ord(ch) <= ord('z'))):
                return 'L'
            if (ord(ch) >= ord('0') and ord(ch) <= ord('9')):
                return 'D'
            return 'S'
        def get_pattern(s):
            pattern = ''
            prev_stat = stateof(s[0])
            count = 0
            for ch in s:
                if prev_stat == stateof(ch):
                    count += 1
                else:
                    pattern += (prev_stat + str(count))
                    prev_stat = stateof(ch)
                    count = 1
            pattern += (prev_stat + str(count))
            return pattern
        def get_fragment(s):
            fragment = {}
            pattern = get_pattern(s)
            n = 0
            cnt = 0
            while n < len(pattern):
                type_ = pattern[n]
                n += 1
                num_ = ''
                while n < len(pattern) and stateof(pattern[n]) == 'D':
                    num_ += pattern[n]
                    n += 1
                key = type_ + num_
                if key in fragment:
                    if s[cnt: cnt + int(num_)] in fragment[key]:
                        fragment[key][s[cnt: cnt + int(num_)]] += 1
                    else:
                        fragment[key][s[cnt: cnt + int(num_)]] = 1
                else:
                    fragment[key] = {}
                    fragment[key][s[cnt: cnt + int(num_)]] = 1
                cnt += int(num_)
            return fragment
        
        ### Matching pattern types (e.g. L5S2D3) and counting probability
        print("Counting pattern probability...")
        self.PP = {}
        rate_base = 1.0 / len(ts)
        for password in tqdm(ts):
            pw_pattern = get_pattern(password)
            if pw_pattern in self.PP:
                self.PP[pw_pattern] += rate_base
            else:
                self.PP[pw_pattern] = rate_base

        ### Merging each fragment (e.g. D3 123) 
        print("Merging fragment...")
        self.FG = {}
        for password in tqdm(ts):
            frag = get_fragment(password)
            for type_ in frag:
                if type_ not in self.FG:
                    self.FG[type_] = frag[type_]
                else:
                    for str_ in frag[type_]:
                        if str_ in self.FG[type_]:
                            self.FG[type_][str_] += frag[type_][str_]
                        else:
                            self.FG[type_][str_] = frag[type_][str_]
        ### Saving Results

        self.trained = True
        return self

    def generate(self, pattern = 'D3L7'):
        if not self.trained:
            print("This PCFG is not trained! Please use some dataset to train it first!")
            return
        
        def stateof(ch):
            if ((ord(ch) >= ord('A') and ord(ch) <= ord('Z')) or 
                (ord(ch) >= ord('a') and ord(ch) <= ord('z'))):
                return 'L'
            if (ord(ch) >= ord('0') and ord(ch) <= ord('9')):
                return 'D'
            return 'S'
        def get_next_pattern(pattern, idx):
            type_ = pattern[idx]
            idx += 1
            num_ = ''
            while idx < len(pattern) and stateof(pattern[idx]) == 'D':
                num_ += pattern[idx]
                idx += 1
            return (type_, num_, idx)

        def get_top_frag(frag, n):
            c = 0
            #password = {}
            password = []
            for item in sorted(frag.items(), key = lambda item:item[1], reverse = True):
                c += 1
                #password[item[0]] = item[1]
                password.append(item[0])
                if c == n:
                    break
            return password
            
        idx = 0
        frags = {}
        while idx < len(pattern):
            type_, num_, idx = get_next_pattern(pattern, idx)
            frags[type_ + num_] = get_top_frag(self.FG[type_ + num_], 10)
        
        total = 0
        for patt in frags:
            if total == 0:
                total = len(frags[patt])
            else:
                total *= len(frags[patt])
        tmp_password = ''
        for i in range(total):
            tmp_pass = ''
            c = i
            for patt in frags:
                tmp_pass += frags[patt][c % len(frags[patt])]
                c = int(c / len(frags[patt]))
            tmp_password += (tmp_pass + '\n')

        return tmp_password


if __name__ == "__main__":

    toy_training_set = load_csdn()

    print("Training PCFG...")
    pcfg = PCFG().fit(toy_training_set)
#     with open("../model/hmm4.pk", "wb") as f:
#         pickle.dump(hmm4, f)

    # Generate passwords
    print("Password generated: ")
    print(pcfg.generate())
#     for _ in range(100):
#         generated_password = hmm4.generate()
#         print(generated_password)