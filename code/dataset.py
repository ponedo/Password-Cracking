import re
from tqdm import tqdm

isascii = lambda s: len(s) == len(s.encode())

def load_csdn(part="all"):
    print("Loading csdn dataset...")
    ts = []
    if part == "all":
        with open("../data/www.csdn.net.sql", "r", encoding="cp950", errors="ignore") as f:
            for line in tqdm(f.readlines()):
                try:
                    username, password, mailbox = line.strip().split(" # ")
                    # ts.append(username, password, mailbox)
                    if len(password) == 0 or not isascii(password):
                        continue
                    ts.append(password)
                except:
                    continue
    elif part == "train":
        with open("../data/csdn_train.txt", "r", encoding="cp950", errors="ignore") as f:
            for line in tqdm(f.readlines()):
                password = line.strip()
                if len(password) == 0 or not isascii(password):
                    continue
                ts.append(password)
    elif part == "test":
        with open("../data/csdn_test.txt", "r", encoding="cp950", errors="ignore") as f:
            for line in tqdm(f.readlines()):
                password = line.strip()
                if len(password) == 0 or not isascii(password):
                    continue
                ts.append(password)
    return ts


def load_yahoo(part="all"):
    print("Loading yahoo dataset...")
    ts = []
    if part == "all":
        with open("../data/plaintxt_yahoo.txt", "r", encoding="cp950", errors="ignore") as f:
            for line in tqdm(f.readlines()):
                if re.match(r".*\s=>>\s.*", line):
                    continue
                try:
                    line_tuple = line.strip().split(':')
                    if len(line_tuple) == 3:
                        idx, username, password = line_tuple
                        if len(password) == 0 or not isascii(password):
                            continue
                        # ts.append(idx, username, password)
                        ts.append(password)
                except:
                    continue
    elif part == "train":
        with open("../data/yahoo_train.txt", "r", encoding="cp950", errors="ignore") as f:
            for line in tqdm(f.readlines()):
                password = line.strip()
                if len(password) == 0 or not isascii(password):
                    continue
                ts.append(password)
    elif part == "test":
        with open("../data/yahoo_test.txt", "r", encoding="cp950", errors="ignore") as f:
            for line in tqdm(f.readlines()):
                password = line.strip()
                if len(password) == 0 or not isascii(password):
                    continue
                ts.append(password)
    return ts


def load_toy(part="all"):
    print("Loading toy dataset...")
    ts = []
    with open("../data/toy_training_set", "r", encoding="utf-8", errors="ignore") as f:
        for line in tqdm(f.readlines()):
            ts.append(line.strip())
    return ts