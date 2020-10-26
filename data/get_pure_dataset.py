import sys, os, random
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
sys.path.insert(0, parentdir)
from code.dataset import load_csdn, load_yahoo
from tqdm import tqdm


def dataset_to_file(dataset, path):
    random.shuffle(dataset)
    n = len(dataset)
    split_n = int(0.8 * n)
    f_all = open(path + ".txt", "w", encoding="utf-8")
    f_train = open(path + "_train.txt", "w", encoding="utf-8")
    f_test = open(path + "_test.txt", "w", encoding="utf-8")
    for i, password in tqdm(enumerate(dataset)):
        f_all.write(password + "\n")
        if i < split_n:
            f_train.write(password + "\n")
        else:
            f_test.write(password + "\n")


if __name__ == "__main__":
    csdn_dataset = load_csdn()
    dataset_to_file(csdn_dataset, "csdn")
    yahoo_dataset = load_yahoo()
    dataset_to_file(yahoo_dataset, "yahoo")