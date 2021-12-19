import flair
from flair.models import TextClassifier
from flair.data import Sentence, Corpus
import torch
from flair.datasets import ClassificationCorpus
from flair.embeddings import WordEmbeddings, FlairEmbeddings, DocumentLSTMEmbeddings
from flair.models import TextClassifier
from flair.trainers import ModelTrainer
from flair.visual.training_curves import Plotter
import sys
import csv
import pandas as pd

maxInt = sys.maxsize



while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

def train():
    # Change the name of your folder to the directory with splitted csv files
    data_folder = "./"
    corpus_fst: Corpus = ClassificationCorpus(data_folder, label_type='class', test_file='test.csv', dev_file='dev.csv', train_file='train.csv')
    label_dict_fst = corpus_fst.make_label_dictionary(label_type='class')
    word_embeddings = [FlairEmbeddings('news-forward-fast'), FlairEmbeddings('news-backward-fast')]
    document_embeddings = DocumentLSTMEmbeddings(word_embeddings, hidden_size=512, reproject_words=True, reproject_words_dimension=256)
    classifier = TextClassifier(document_embeddings, label_dictionary=label_dict_fst, label_type='class')
    trainer = ModelTrainer(classifier, corpus_fst)
    trainer.train('./', max_epochs=2)


def predict(text='Flair is pretty neat!'):
    classifier = TextClassifier.load('en-sentiment')
    sentence = Sentence(text)
    classifier.predict(sentence)
    # print sentence with predicted labels
    print('Sentence above is: ', sentence.labels)

def pre_process():
    cols = ['label','id','date','query_string','user','text']
    data = pd.read_csv("./training.1600000.processed.noemoticon.csv", encoding='latin-1', names=cols)
    data.drop(columns=['id', 'date', 'query_string', 'user'], axis=1, inplace=True)
    #data.loc[data['label']==4, 'label'] = 'positive'
    #data.loc[data['label']==0, 'label'] = 'negative'
    print(type(data['label'][0]))
    data['label'] = '__label__' + data['label'].astype(str)
    data = data[['label', 'text']]
    print(len(data))
    data = data.truncate(after=(0.6*len(data)))
    print(len(data))

# data.iloc[0:int(len(data)*0.8)].to_csv('train.csv', sep='\t', index = False, header = False)
# data.iloc[int(len(data)*0.8):int(len(data)*0.9)].to_csv('test.csv', sep='\t', index = False, header = False)
# data.iloc[int(len(data)*0.9):].to_csv('dev.csv', sep='\t', index = False, header = False)


plotter = Plotter()
plotter.plot_training_curves('loss.tsv')
plotter.plot_weights('weights.txt')