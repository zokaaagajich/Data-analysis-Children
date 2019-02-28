#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pandas
import missingno
import matplotlib.pyplot as plt

args = sys.argv
if len(args) != 2:
    sys.exit(f"usage: ./{args[0]} /path/to/.csv")

#ucitavanje iz prosledjenog csv fajla
df = pandas.read_csv(args[1])
#plotovanje missingo rezultata
plt.show(missingno.matrix(df.sample(250)))
