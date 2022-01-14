import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from imblearn.over_sampling import RandomOverSampler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score, f1_score
from sklearn.inspection import permutation_importance
from sklearn.metrics import roc_auc_score, roc_curve, classification_report,\
                            accuracy_score, confusion_matrix, auc
from xgboost import XGBClassifier

import pickle

import sys

print('-----\n Iniciando teste \n')

# Importando os dados de trein

X_test = pd.read_csv(sys.argv[2] + '/X_test.csv')

y_test = pd.read_csv(sys.argv[2] + '/y_test.csv')

# carregando model

model = pickle.load(open(sys.argv[1] + '/mncp.pkl', 'rb'))

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print('-----\n Avaliação do modelo: \n')
print('accuracy:', accuracy)
print('recall:  ', recall)
print('f1:      ', f1)

# criando um dataframe com as probabilidaes e as informações sobre o usuário

X_test_pred_prob_df = pd.DataFrame(model.predict_proba(X_test))

predict_prospect = pd.DataFrame()
predict_prospect['PROB_PROSPECT'] = X_test_pred_prob_df[0]*100
predict_prospect['PROB_ASSINANTE'] = X_test_pred_prob_df[1]*100
predict_prospect["PERFIL"] = y_test['PERFIL']
predict_prospect = pd.merge(predict_prospect, X_test, left_index=True, right_index=True)

# predict_prospect = predict_prospect[predict_prospect['PERFIL'] == 0]

# Salvando a tabela de probabilidades na pasta output/data

print('-----\n Predições das probabilidades dos prospects salvas em output/data \n----')

predict_prospect.to_csv(sys.argv[3] + 'data/predict_prospect.csv', index=False)
