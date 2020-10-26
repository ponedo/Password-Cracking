import random
import sys
import pickle
from dataset import *
from getopt import getopt


if __name__ == "__main__":
    opts, args = getopt(sys.argv[1:], "m:d:", ["model=", "dataset-name="])
    cmd_opts = dict(opts)
    assert ("-m" in cmd_opts) ^ ("--model" in cmd_opts)
    assert ("-d" in cmd_opts) ^ ("--dataset-name" in cmd_opts)

    try:
        model_name = cmd_opts["-m"]
    except KeyError:
        model_name = cmd_opts["--model"]
    try:
        dataset_name = cmd_opts["-d"]
    except KeyError:
        dataset_name = cmd_opts["--dataset_name"]

    print("Testing " + model_name + " with " + dataset_name + "...")
    with open("../model/" + model_name + "_" + dataset_name + ".pk", "rb") as f:
        model = pickle.load(f)

    # Generate passwords
    print("Password generated: ")
    for _ in range(100):
        generated_password = model.generate()
        print(generated_password)