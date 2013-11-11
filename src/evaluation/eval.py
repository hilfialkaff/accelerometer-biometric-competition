import pandas as pd

CHUNK_SIZE = 1024
QUESTION_FILE = '../data/questions.csv'
TEST_FILE = '../data/test.csv'

class Evaluator(object):
    def __init__(self, device_id):
        self.dids_qn = self.read_questions(QUESTION_FILE, device_id)
        self.device_id = device_id

    def read_questions(self, f, device_id):
        dids = pd.DataFrame(columns=['QuestionId', 'SequenceId', 'QuizDevice'])
        for df in pd.read_csv(f, chunksize=CHUNK_SIZE):
            dids = pd.concat([dids, df[df['QuizDevice']==device_id]])
        return dids

    def read_tests(self, f, seq_id):
        dids = pd.DataFrame(columns=['T', 'X', 'Y', 'Z', 'SequenceId'])
        for df in pd.read_csv(f, chunksize=CHUNK_SIZE):
            dids = pd.concat([dids, df[df['SequenceId']==seq_id]])
        return dids

    def evaluate(self, model):
        for qn_index, qn_row in self.dids_qn.iterrows():
            dids_test = self.read_tests(TEST_FILE, qn_row['SequenceId'])
            print "device_id:", self.device_id
            score = model.score(dids_test)
            print "score:", score
