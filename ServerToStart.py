from RNNModelPredict import aRNNModel

import sys

sys.path.append("./ReorderVis")
from ReorderVis.Flask import ToRun


theMod=aRNNModel()

ToRun(theMod)