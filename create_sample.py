import pandas as pd
from datetime import datetime, timedelta

# Criar dados de exemplo
data = {
    'ID': [1, 2, 3, 4, 5],
    'Nome': ['João Silva', 'Maria Santos', 'Pedro Oliveira', 'Ana Costa', 'Carlos Souza'],
    'Idade': [25, 30, 35, 28, 42],
    'Salário': [3500.50, 4200.75, 5100.00, 3800.25, 6500.00],
    'Ativo': [True, True, False, True, True],
    'Data_Admissão': [
        datetime(2020, 1, 15),
        datetime(2019, 5, 20),
        datetime(2018, 3, 10),
        datetime(2021, 7, 1),
        datetime(2017, 11, 25)
    ],
    'Departamento': ['TI', 'RH', 'Vendas', 'TI', 'Financeiro'],
    'Email': ['joao@empresa.com', 'maria@empresa.com', 'pedro@empresa.com', 'ana@empresa.com', 'carlos@empresa.com']
}

# Criar DataFrame
df = pd.DataFrame(data)

# Salvar como Excel
df.to_excel('/home/ubuntu/xls-to-csv-converter/exemplo_funcionarios.xlsx', index=False)
print("Arquivo de exemplo criado: exemplo_funcionarios.xlsx")

