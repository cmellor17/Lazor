import time
import random
import os

def load_puzzle(filename):
    if ".bff" in filename:
        filename = filename.split(".bff")[0]
    f = open(filename + ".bff", "r")
    print(f.readline())
    print(f.readline())
    print(f.readline())
    print(f.readline())
    return f















if __name__ == "__main__":
    puz = load_puzzle("Lazor Project/lazor_fall_2024/bff_files/dark_1.bff")
    print(puz)