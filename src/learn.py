import sys, getopt
from classifier.naivehmm import NaiveHMM
from evaluation.eval import Evaluator
import pandas as pd

NAIVE_HMM_STATES=3
CHUNK_SIZE = 1024

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
        return NaiveHMM(NAIVE_HMM_STATES)
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
    for df in pd.read_csv(path, chunksize=CHUNK_SIZE):
        devices = df['Device'].unique()
        for device in devices:
            if not device in models:
                models[device] = train(path, model, device)
        # endfor
    # end
    return models


if __name__=='__main__':
    path, model = parse_args(sys.argv[1:])
    models = train_models(path, model)
    print models

    for device_id, model in models.items():
        evaluator = Evaluator(device_id)
        evaluator.evaluate(model)
