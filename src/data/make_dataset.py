
import pandas as pd
import numpy as np
import datetime
import sys
import os

# Lendo o raw_data

raw_data = pd.read_csv(sys.argv[1] + '/raw_data.csv')

# Se existir deletar as NA's

raw_data_non_na = raw_data.dropna()

# removendo datas inconsistentes

df_filtered_date = raw_data_non_na[raw_data_non_na['PES_NASCIMENTO_DATA'] != "08.04.4194 00:00:00"]
df_filtered_date = df_filtered_date[df_filtered_date['PES_NASCIMENTO_DATA'] != "03.02.0068 00:00:00"]
df_filtered_date = df_filtered_date[df_filtered_date['PES_NASCIMENTO_DATA'] != "02.01.0001 00:00:00"]
df_filtered_date = df_filtered_date[df_filtered_date['PES_NASCIMENTO_DATA'] != "08.08.0072 00:00:00"]
df_filtered_date = df_filtered_date[df_filtered_date['PES_NASCIMENTO_DATA'] != "22.08.1088 00:00:00"]
df_filtered_date = df_filtered_date[df_filtered_date['PES_NASCIMENTO_DATA'] != "28.03.0060 00:00:00"]

# criando coluna do dia atual 

df_filtered_date['TODAY'] = pd.to_datetime("today")

# alterando para o tipo data a coluna PES_NASCIMENTO_DATA --- today foi realizado por precaução

df_filtered_date[['TODAY','PES_NASCIMENTO_DATA']] = df_filtered_date[['TODAY','PES_NASCIMENTO_DATA']].apply(pd.to_datetime) 

# Criando a coluna idade

df_filtered_date['IDADE'] = (df_filtered_date['TODAY'] - df_filtered_date['PES_NASCIMENTO_DATA']).astype('timedelta64[Y]')

# Filtrando clientes de acordo com mínimo permitido e a idade mais longeva possível

df_filtered_final = df_filtered_date[df_filtered_date['IDADE'] >= 18]

df_filtered_final = df_filtered_final[df_filtered_final['IDADE'] <= 100]

# Salvando o dataframa para análise exploratória

df_filtered_final.to_csv(sys.argv[2] + '/df_filtered.csv', index=False)

# criando dicionarios para alterar os valores das colunas categóricas para construção do modelo

income_dict = {"ATE 1SM":0,
            "DE 2SM ATE 3SM" : 1,
            "DE 3SM ATE 4SM" : 2,
            "DE 4SM ATE 8SM" : 3,
            "DE 8SM ATE 14SM": 4,
            "DE 14SM ATE 25SM" : 5,
            "ACIMA DE 25SM": 6}

boolean_dict = {"PROSPECT ": 0, # considerando o espaço a mais
            "NAO": 0,
            "M": 0,
            "ASSINANTE": 1,
            "SIM": 1,
            "F": 1}

df_filtered_final["ATR_PF_GEO_RENDA_FAM"].replace(income_dict, inplace=True)
df_filtered_final["USOU_APP"].replace(boolean_dict, inplace=True)
df_filtered_final["PERFIL"].replace(boolean_dict, inplace=True)
df_filtered_final["PES_GENERO"].replace(boolean_dict, inplace=True)


df_filtered_final = df_filtered_final.drop(['TODAY'], axis=1)
df_filtered_final = df_filtered_final.drop(['PES_NASCIMENTO_DATA'], axis=1)
df_filtered_final = df_filtered_final.drop(['ID'], axis=1)
df_filtered_final['PES_GENERO'] = df_filtered_final['PES_GENERO'].astype(bool)
df_filtered_final['USOU_APP'] = df_filtered_final['USOU_APP'].astype(bool)

df_filtered_final.to_csv(sys.argv[2] + '/data_model.csv', index=False)

print(f'Processamento concluído! \nO dataframe inicial continha, {raw_data.shape[0]} entradas. Pós tratamento o dataframe final ficou com {df_filtered_final.shape[0]} entradas')
