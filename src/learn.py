import sys, getopt
from classifier.naivehmm import NaiveHMM
from evaluation.eval import Evaluator
import pandas as pd
import numpy as np

from constants import *

def parse_args(argv):
    path = None
    model = None
    try:
        opts, args = getopt.getopt(argv, "hp:m:")
    except getop.GetoptError:
        print 'learn.py -p <trainfile> -m <model name>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'learn.py -p <trainfile> -m <model name>'
        elif opt in ('-p', '--path'):
            path = arg
        elif opt in ('-m', '--model'):
            model = arg
    return (path, model)

    return model

def get_model(model):
    if model == 'NaiveHMM':
        return NaiveHMM(NAIVE_HMM_STATES, 0)
    return None

def train(path, model, did):
    train = pd.DataFrame(columns=['T','X','Y','Z','Device'])
    for df in pd.read_csv(path, chunksize=CHUNK_SIZE):
        train = pd.concat([train, df[df['Device']== did]])


    m = get_model(model)
    m.fit(pd.DataFrame(train))
    return m


def train_models(path, model):
    """
    @return Dictionary of models for every device.
    """
    models = {}
    train = {}

    for df in pd.read_csv(path, chunksize=CHUNK_SIZE):
        devices = df['Device'].unique()

        for device in devices:
            if device not in train:
                train[device] = pd.DataFrame(columns=['T','X','Y','Z','Device'])
            train[device] = pd.concat([train[device], df[df['Device'] == device]])

    for device, data in train.items():
        print "training device id:", device
        partitions = np.array_split(df, NUM_FOLD)
        models[device] = []

        for i in range(NUM_FOLD):
            m = get_model(model)
            m.fit(pd.DataFrame(partitions[i]))
            models[device].append(m)
            print "partition:", i

    return models

if __name__=='__main__':
    path, model = parse_args(sys.argv[1:])
    models = train_models(path, model)
    evaluator = Evaluator(models)
    evaluator.evaluate()
