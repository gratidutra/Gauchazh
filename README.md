New clients probability
==============================

## Passo-a-passo para utilização

- Clone o repositório

- Direcione-se ao diretório clonado e execute o comando ```make create_environmente```

- Ative o ambiente com ```conda activate new-clientes-probability```

- Dentro do diretório ``data/raw_data`` estão as tabelas cruas. Porém esta pasta não se encontra no repositório para evitar excesso de memória, por isso ao clonar o repositório crie a pasta ``data`` e dentro dela duas outras pastas ``raw`` e ``processed`` 

- Todos os scripts estão presentes no diretório ``src``. Nesse template são possíveis executar os seguintes comandos:

- ```make raw_data``` - executa o script, localizado em ``src/dump_data``, que une as duas tabelas cruas disponilizadas no Case

- ```make process_data``` - executa o processamento dos dados (limpeza, remoção de NA's e remoção de informações erradas)

- ```make train``` - cria o modelo, separa os dados em treino e teste e salva o modelo na pasta ``models``

- ```make predict``` - local onde o modelo é avaliado com os dados de teste e salva em ``outputs/data`` a probabilidade de cada usuário ser assinante ou prospect 

--------------

## Notebooks 

No diretório ```src/notebooks``` existem 3 notebooks:

**exploratory_analysis** - é onde se encontram as análises exploratórias

**models** - onde foram testados 4 modelos diferentes e escolhido o melhor para rodar no make train

**deploy_scripts** - Script de implementação do modelo no google Cloud
