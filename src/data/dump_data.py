# Importando as libs 

import pandas as pd
import sys
import os

# chamando as duas plainilhas 

planilha_1 = pd.read_csv(sys.argv[1] + '/Planilha_1.csv', delimiter = ";")
planilha_2 = pd.read_csv(sys.argv[1] + '/Planilha_2.csv', delimiter = ";")

# Unindo as duas tabelas em uma só

raw_data = pd.merge(planilha_1, planilha_2, on = "ID", how = "outer")

# Salvando a tabela

raw_data.to_csv(sys.argv[1] + '/raw_data.csv', index=False)