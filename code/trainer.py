import random
import sys
import pickle
from hmm4 import HMM4
from mc import MarkovChain
from dataset import *
from getopt import getopt


if __name__ == "__main__":
    opts, args = getopt(sys.argv[1:], "m:d:", ["model=", "dataset_name="])
    cmd_opts = dict(opts)
    assert ("-m" in cmd_opts) ^ ("--model" in cmd_opts)
    assert ("-d" in cmd_opts) ^ ("--dataset_name" in cmd_opts)

    try:
        model_name = cmd_opts["-m"]
    except KeyError:
        model_name = cmd_opts["--model"]
    try:
        dataset_name = cmd_opts["-d"]
    except KeyError:
        dataset_name = cmd_opts["--dataset_name"]

    print("Training " + model_name + " with " + dataset_name + "...")

    if dataset_name == "toy":
        dataset = load_toy()
    elif dataset_name == "csdn":
        dataset = load_csdn()
    elif dataset_name == "yahoo":
        dataset = load_yahoo()

    if model_name == "hmm4":
        model = HMM4().fit(dataset)
    elif model_name == "mc":
        model = MarkovChain(3).fit(dataset)

    with open("../model/" + model_name + "_" + dataset_name + ".pk", "wb") as f:
        pickle.dump(model, f)
