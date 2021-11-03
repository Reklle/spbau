import random

import numpy as np

#
# genetic-like algorithm of changing seeds
#


class Genetics:
    good_genes = []

    def __init__(self, ref="seeds.npy"):
        self.ref = ref
        try:
            self.download()
        except:
            print("error: the file cannot be read")
        self.good_genes = []

    # IO from file seeds.npy

    def upload(self):
        """save good seeds"""
        np.save(self.ref, self.good_genes)

    def download(self):
        """read seeds form file "seeds.npy" """
        self.good_genes = np.load("seeds.npy", allow_pickle='TRUE')

    def legacy_seed(self):
        legacy_rule = {"1": [["2", "1", "1", "1"], ["2", "2", "1", "1"], ["2", "2", "1", "1"], ["1", "2", "3", "3"]],
                       "2": [["11", "1", "1", "1"], ["11", "2", "2", "2"], ["11", "1", "3", "1"],
                             ["11", "3", "3", "3"]],
                       "3": [["2", "1", "1", "1"], ["1", "2", "3", "3"], ["1", "2", "3", "3"], ["1", "3", "3", "1[1]"]]}

        dict = {}
        for i in range(0, 4):
            for j in range(1, 4):
                for k in range(0, 4):
                    dict.update({str(i) + str(j) + str(k): legacy_rule.get(str(j))[i][k]})
        return dict

    def random_seed(self):
        dict = {}
        alpha = ["1[1]", "2[1]", "3[1]", "1[2]", "2[2]", "3[2]", "1[3]", "2[3]", "3[3]",
                 "[1]1", "[1]2", "[1]3", "[2]1", "[2]2", "[2]3", "[3]1", "[3]2", "[3]3"]
        beta = ["1", "2", "3"]
        gamma = ["11", "21", "31", "12", "22", "32", "13", "23", "33"]
        for i in range(0, 4):
            for j in range(1, 4):
                for k in range(0, 4):
                    if (random.randint(0, 100) > 100 - 50):
                        dict.update({str(i) + str(j) + str(k): beta[random.randint(0, len(beta) - 1)]})
                    elif (random.randint(0, 100) > 100 - 50):
                        dict.update({str(i) + str(j) + str(k): gamma[random.randint(0, len(gamma) - 1)]})
                    else:
                        dict.update({str(i) + str(j) + str(k): alpha[random.randint(0, len(alpha) - 1)]})
        return dict

    def rand(self, arg):
        """return random value from array"""
        return arg[random.randint(0, len(arg) - 1)]

    def random_from_file(self):
        """just random seed form file "seeds.npy" """
        return self.rand(self.good_genes)

    # functions with genes

    def breeding(self):
        """genetic-like (in/out)bringing of 2 seeds"""
        x = self.random_from_file()
        y = self.random_from_file()
        return self.gen_mix(x, y)

    def weak_breeding(self, x: float):
        """genetic-like (in/out)bringing of 2 seeds
        change only x‰ values"""
        z = self.random_from_file()
        y = self.random_from_file()
        return self.weak_gen_mix(z, y, x)

    def gen_mix(self, seed_a: dict, seed_b: dict):
        chld = {}
        for k in seed_a.keys():
            if random.randint(0, 1) == 0:
                chld.update({k: seed_a[k]})
            else:
                chld.update({k: seed_b[k]})
        return chld

    def weak_gen_mix(self, seed_main: dict, seed_additional: dict, f: float):
        chld = {}
        for k in seed_main.keys():
            if random.randint(0, 1000) < f * 1000:
                chld.update({k: seed_additional[k]})
            else:
                chld.update({k: seed_main[k]})
        return chld
