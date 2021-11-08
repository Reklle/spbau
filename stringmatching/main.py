import ACTG

file = open("arabidopsis suecica chromosome 1.actg").read()

m = ACTG.ACTGMathing(file)  # a primer sample
# ACTG.StringMatching(file)

print(m.list("AACCAGACAA", m.rk))
