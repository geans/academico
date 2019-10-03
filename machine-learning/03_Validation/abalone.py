#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Atividade para trabalhar o validação dos dados.

@author: Aydano Machado <aydano.machado@gmail.com>
Adaptado por Gean Santos <geans.santos@gmail.com>
"""

import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import requests
import preproccessing
import validation

# Workspace #
y_pred = validation.run()


# Enviando previsões realizadas com o modelo para o servidor
URL = "https://aydanomachado.com/mlclass/03_Validation.php"

#TODO Substituir pela sua chave aqui
DEV_KEY = "Equipe K"

# json para ser enviado para o servidor
data = {'dev_key':DEV_KEY,
        'predictions':pd.Series(y_pred).to_json(orient='values')}

# Enviando requisição e salvando o objeto resposta
r = requests.post(url = URL, data = data)

# Extraindo e imprimindo o texto da resposta
pastebin_url = r.text
print(" - Resposta do servidor:\n", r.text, "\n")