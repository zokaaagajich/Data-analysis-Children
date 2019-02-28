#!/usr/bin/env python
# -*- coding: utf-8 -*-

import geoplotlib
from geoplotlib.utils import read_csv, BoundingBox
import sys

args = sys.argv
if len(args) != 2:
    sys.exit(f"usage: ./{args[0]} /path/to/.csv")

data = read_csv(args[1])
geoplotlib.kde(data, 5, cut_below=1e-4, show_colorbar=False)
geoplotlib.set_bbox(BoundingBox.USA)
geoplotlib.show()
