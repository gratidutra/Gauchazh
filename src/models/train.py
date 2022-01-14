import numpy as np
import pandas as pd
from imblearn.over_sampling import RandomOverSampler
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
import pickle

import sys

df = pd.read_csv(sys.argv[1] + '/data_model.csv')

# Separando o datagrame em variável preditora e resposta

X = df.drop(['PERFIL'], axis=1)
y = df[['PERFIL']].astype(bool)

# Under sampling para balanceamento do dataset

random_over_sampler = RandomOverSampler()
X_res, y_res = random_over_sampler.fit_resample(X, y)

# Separando os dados em treino e teste

X_train, X_test, y_train, y_test = train_test_split(X_res, y_res)

# criando o modelo

model = XGBClassifier()

model.fit(X_train, y_train)

# Salvando o modelo e os dados de teste

# modelo (model new clientes probability - mncp) em duas opções

pickle = pickle.dump(model, open(sys.argv[2] + '/mncp.pkl', 'wb'))

#model.save_model(sys.argv[2] +'mncp.pkl')

# dados de teste

X_test.to_csv(sys.argv[1] + '/X_test.csv', index=False)

y_test.to_csv(sys.argv[1] + '/y_test.csv', index=False)

# criando o modelo com random forest para o deploy devido a memória

# model_random = RandomForestClassifier()

# model_random.fit(X_train, y_train)

# Salvando o modelo e os dados de teste

# modelo (model new clientes probability - mncp) em duas opções

# pickle = pickle.dump(model_random, open(sys.argv[2] + '/mncp_random.pkl', 'wb'))
