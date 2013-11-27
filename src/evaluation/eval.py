import pandas as pd
# import sys
import operator

CHUNK_SIZE = 1024
QUESTION_FILE = '../data/questions.csv'
TEST_FILE = '../data/test.csv'
ANSWER_FILE = '../data/answers.csv'

class Evaluator(object):
    # def __init__(self, device_id):
    #     self.dids_qn = self.read_questions(QUESTION_FILE, device_id)
    #     self.device_id = device_id

    def __init__(self, models):
        self.models = models
        self.dids_qn = self.read_questions(QUESTION_FILE)
        self.dids_test = self.read_tests(TEST_FILE)
        self.num_devices = len(self.models)

    def read_questions(self, f, device_id=-1):
        dids = pd.DataFrame(columns=['QuestionId', 'SequenceId', 'QuizDevice'])

        if device_id != -1:
            for df in pd.read_csv(f, chunksize=CHUNK_SIZE):
                dids = pd.concat([dids, df[df['QuizDevice']==device_id]])
        else:
            for df in pd.read_csv(f, chunksize=CHUNK_SIZE):
                dids = pd.concat([dids, df])

        return dids

    def read_tests(self, f):
        dids_test = {}

        for df in pd.read_csv(f, chunksize=CHUNK_SIZE):
            seqs = df['SequenceId'].unique()

            for seq in seqs:
                if seq not in dids_test:
                    dids_test[seq] = pd.DataFrame(columns=['T', 'X', 'Y', 'Z', 'SequenceId'])
                dids_test[seq] = pd.concat([dids_test[seq], df[df['SequenceId'] == seq]])

        return dids_test

    # def read_tests(self, f, seq_id):
    #     dids = pd.DataFrame(columns=['T', 'X', 'Y', 'Z', 'SequenceId'])
    #     for df in pd.read_csv(f, chunksize=CHUNK_SIZE):
    #         dids = pd.concat([dids, df[df['SequenceId']==seq_id]])
    #     return dids

    # def evaluate(self, model):
    #     for qn_index, qn_row in self.dids_qn.iterrows():
    #         dids_test = self.read_tests(TEST_FILE, qn_row['SequenceId'])
    #         print "device_id:", self.device_id
    #         score = model.score(dids_test)
    #         print "score:", score

    def evaluate(self):
        print "Start evaluating..."

        answers = {}
        answers['QuestionId'] = []
        answers['IsTrue'] = []

        i = 1
        for qn_index, qn_row in self.dids_qn.iterrows():
            # best_score = -sys.maxint
            # best_device = -1

            scores = {}
            dids_test = self.dids_test[qn_row['SequenceId']]

            if qn_row['QuizDevice'] not in self.models.keys():
                continue

            for did, model in self.models.items():
                score = model.score(dids_test)
                scores[did] = score

                # if score > best_score:
                #     best_score = score
                #     best_device = did

            # print "question:", qn_row['QuestionId'], "prediction:", best_device, \
            #     "with score:", best_score

            # answers['QuestionId'].append(qn_row['QuestionId'])
            # if best_device == qn_row['QuizDevice']:
            #     answers['IsTrue'].append(1)
            # else:
            #     answers['IsTrue'].append(0)

            did = qn_row['QuizDevice']
            _scores = sorted(scores.iteritems(), key=operator.itemgetter(1))
            rank = _scores.index((did, scores[did])) + 1

            answers['QuestionId'].append(qn_row['QuestionId'])
            if rank > (self.num_devices * 0.90) and scores[did] > -2000:
                is_true = 1
                answers['IsTrue'].append(1)
            else:
                is_true = 0
                answers['IsTrue'].append(0)

            print "question:", qn_row['QuestionId'], "device score:", scores[did], \
                "rank:", rank, "answer:", is_true

            # if i == 100:
            #     break
            i += 1

        df_answers = pd.DataFrame(answers)
        df_answers.to_csv(ANSWER_FILE, ',', header=True, cols=["QuestionId","IsTrue"], index=False)

if __name__ == '__main__':
    _eval = Evaluator(None)
