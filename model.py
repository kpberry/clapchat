import os
from math import pi, sqrt

import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelBinarizer

train_amount = 500
X, y = [], []
for file in os.listdir('data'):
    X.append(np.load('data/' + file))
    y.append('clap' if 'clap' in file else 'noise')
    # plt.plot(X[-1])
    # plt.title(y[-1])
    # plt.show()


best_acc = 0
best = None
SIGMAS = np.arange(0.01, 5, 0.2)
KERNEL_BASES = [np.arange(-50, 50, 1)]
OFFSETS = np.arange(0, 0.02, 0.01)
THRESHOLDS = [1 * 10 ** -(i + 1) for i in range(6)]
candidates = len(SIGMAS) * len(KERNEL_BASES) * len(OFFSETS) * len(THRESHOLDS)
i = 0
for SIGMA in SIGMAS:
    for KERNEL_BASE in KERNEL_BASES:
        for OFFSET in OFFSETS:
            for THRESHOLD in THRESHOLDS:
                i += 1
                print(str(i) + ' / ' + str(candidates))
                KERNEL = np.exp(-KERNEL_BASE ** 2 / (2 * SIGMA ** 2)) / sqrt(pi * 2) / SIGMA - OFFSET
                pred = []
                for x in X:
                    cur_chunk = np.abs(x)
                    convolved = np.convolve(KERNEL, cur_chunk)
                    if np.max(convolved) > THRESHOLD:
                        pred.append('clap')
                    else:
                        pred.append('noise')
                acc = accuracy_score(y, pred)
                print('Acc:', acc)
                if acc > best_acc:
                    best = SIGMA, KERNEL_BASE, OFFSET, THRESHOLD
                    best_acc = acc
                    print("New best:", best_acc)
print(best_acc)
print(best)
