# import and test
import tensorflow as tf2

print("TF version =", tf2.__version__)

# we want TF 2.x
assert tf2.__version__ >= "2.0"

# disable eager execution etc
tf = tf2.compat.v1
tf.disable_eager_execution()

# disable annoying warnings
tf.logging.set_verbosity(tf.logging.ERROR)
import warnings

warnings.filterwarnings('ignore')

# make sure we have GPU support
print("GPU support = ", tf.test.is_gpu_available())

# import other useful libs
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import time
from tqdm import tqdm_notebook
from Neural_Approximator import Neural_Approximator
from BlackScholes import BlackScholes


def test(generator,
         sizes,
         nTest,
         simulSeed=None,
         testSeed=None,
         weightSeed=None,
         deltidx=0):
    # simulation
    print("simulating training, valid and test sets")
    xTrain, yTrain, dydxTrain = generator.trainingSet(max(sizes), seed=simulSeed)
    xTest, xAxis, yTest, dydxTest, vegas = generator.testSet(num=nTest, seed=testSeed)
    print("done")

    # neural approximator
    print("initializing neural appropximator")
    regressor = Neural_Approximator(xTrain, yTrain, dydxTrain)
    print("done")

    predvalues = {}
    preddeltas = {}
    for size in sizes:
        print("\nsize %d" % size)
        regressor.prepare(size, False, weight_seed=weightSeed)

        t0 = time.time()
        regressor.train("standard training")
        predictions, deltas = regressor.predict_values_and_derivs(xTest)
        predvalues[("standard", size)] = predictions
        preddeltas[("standard", size)] = deltas[:, deltidx]
        t1 = time.time()
        print(t1-t0)

        regressor.prepare(size, True, weight_seed=weightSeed)

        t0 = time.time()
        regressor.train("differential training")
        predictions, deltas = regressor.predict_values_and_derivs(xTest)
        predvalues[("differential", size)] = predictions
        preddeltas[("differential", size)] = deltas[:, deltidx]
        t1 = time.time()
        print(t1 - t0)
    return xAxis, yTest, dydxTest[:, deltidx], vegas, predvalues, preddeltas


def graph(title,
          predictions,
          xAxis,
          xAxisName,
          yAxisName,
          targets,
          sizes,
          computeRmse=False,
          weights=None):
    numRows = len(sizes)
    numCols = 2

    fig, ax = plt.subplots(numRows, numCols, squeeze=False)
    fig.set_size_inches(4 * numCols + 1.5, 4 * numRows)

    for i, size in enumerate(sizes):
        ax[i, 0].annotate("size %d" % size, xy=(0, 0.5),
                          xytext=(-ax[i, 0].yaxis.labelpad - 5, 0),
                          xycoords=ax[i, 0].yaxis.label, textcoords='offset points',
                          ha='right', va='center')

    ax[0, 0].set_title("standard")
    ax[0, 1].set_title("differential")

    for i, size in enumerate(sizes):
        for j, regType, in enumerate(["standard", "differential"]):

            if computeRmse:
                errors = 100 * (predictions[(regType, size)] - targets)
                if weights is not None:
                    errors /= weights
                rmse = np.sqrt((errors ** 2).mean(axis=0))
                t = "rmse %.2f" % rmse
            else:
                t = xAxisName

            ax[i, j].set_xlabel(t)
            ax[i, j].set_ylabel(yAxisName)

            ax[i, j].plot(xAxis * 100, predictions[(regType, size)] * 100, 'co', \
                          markersize=2, markerfacecolor='white', label="predicted")
            ax[i, j].plot(xAxis * 100, targets * 100, 'r.', markersize=0.5, label='targets')

            ax[i, j].legend(prop={'size': 8}, loc='upper left')

    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.suptitle("% s -- %s" % (title, yAxisName), fontsize=16)
    plt.show()


# simulation set sizes to perform
sizes = [1024, 8192]
print("Starting Simulation")
print("Starting Simulation")
# show delta?
showDeltas = True

# seed
# simulSeed = 1234
simulSeed = np.random.randint(0, 10000)
print("using seed %d" % simulSeed)
weightSeed = None

# number of test scenarios
nTest = 100

# go
generator = BlackScholes()
xAxis, yTest, dydxTest, vegas, values, deltas = \
    test(generator, sizes, nTest, simulSeed, None, weightSeed)

# show predicitions
graph("Black & Scholes", values, xAxis, "", "values", yTest, sizes, True)

# show deltas
if showDeltas:
    graph("Black & Scholes", deltas, xAxis, "", "deltas", dydxTest, sizes, True)