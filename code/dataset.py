from tqdm import tqdm

def load_csdn():
    print("Loading csdn dataset...")
    ts = []
    with open("../data/www.csdn.net.sql", "r", encoding="cp950", errors="ignore") as f:
        for line in tqdm(f.readlines()):
            try:
                username, password, mailbox = line.strip().split(" # ")
                # ts.append(username, password, mailbox)
                ts.append(password)
            except:
                continue
    return ts


def load_yahoo():
    print("Loading yahoo dataset...")
    ts = []
    with open("../data/plaintxt_yahoo.txt", "r", encoding="cp950", errors="ignore") as f:
        for line in tqdm(f.readlines()):
            try:
                line_tuple = line.strip().split(':')
                if len(line_tuple) == 3:
                    idx, username, password = line_tuple
                    # ts.append(idx, username, password)
                    ts.append(username)
            except:
                continue
    return ts


def load_toy():
    print("Loading toy dataset...")
    ts = []
    with open("../data/toy_training_set", "r", encoding="utf-8", errors="ignore") as f:
        for line in tqdm(f.readlines()):
            ts.append(line.strip())
    return ts