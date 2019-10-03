#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Atividade para trabalhar o validação dos dados.

@author: Aydano Machado <aydano.machado@gmail.com>
Adaptado por Gean Santos <geans.santos@gmail.com>
"""
from pandas import read_csv, isna, concat
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split, cross_validate
import preproccessing

# Estimators
from sklearn.neighbors import KNeighborsClassifier
from sklearn import linear_model, svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier


def debug(value=''):
    DEBUG = True
    if DEBUG:
        print(value)


def run():
    # debug('\n - Fazendo pre-processamento')
    data, target = preproccessing.run()
    debug('{:13} {}'.format('Estimator','Scores'))
    debug('{:-<20}'.format(''))
    dataset = read_csv('abalone_dataset.csv')

    X, y = dataset[data], dataset[target]
    def score (estimator, name):
        scores = cross_validate(estimator, X, y)
        i = 0
        s = 0
        for j in scores['test_score']:
            s += j
            i += 1
        s /= i
        debug('{:13}  {:.3}'.format(name, s))

    # debug(' - Avaliando modelos preditivos')
    knn = KNeighborsClassifier(n_neighbors=30)
    # lasso = linear_model.Lasso()
    svc = svm.SVC(C=1, kernel='linear')
    rfc = RandomForestClassifier(max_depth=5, random_state=0)
    gnb = GaussianNB()
    nnc = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)


    score(knn, 'K-NN')
    # score(lasso, 'lasso')
    score(svc, 'SVC')
    score(rfc, 'Random Forest')
    score(gnb, 'Gaussian NB')
    score(nnc, 'Neural Network')

    # debug(' - Aplicando modelo e enviando para o servidor')
    # data_app = pd.read_csv('abalone_app.csv')
    # best_estimator = None
    # y_pred = best_estimator.predict(data_app)
    # return y_pred
