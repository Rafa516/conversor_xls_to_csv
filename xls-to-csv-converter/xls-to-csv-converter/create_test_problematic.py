import pandas as pd
from datetime import datetime

# Criar dados com problemas típicos
data = {
    'ID_Pequeno': [1, 2, 3, 4, 5],
    'ID_Grande': [3000000000, 5000000000, 9999999999, 1234567890123, 999999999],  # Valores fora do range INTEGER
    'Nome_Problematico': [
        'João Silva',
        'María García',  # Caracteres especiais
        'Test•Invalid',  # Caractere especial
        'Normal Name',
        'Émilie Château'  # Acentos franceses
    ],
    'Valor_Extremo': [2147483647, 2147483648, -2147483648, -2147483649, 1000000000],  # No limite e além
    'Texto_UTF8': [
        'Olá Mundo! 🌍',
        'Привет мир',  # Russo
        '你好世界',  # Chinês
        'مرحبا بالعالم',  # Árabe
        'Hello World'
    ],
    'Salario': [3500.50, 4200.75, 5100.00, 3800.25, 6500.00],
    'Data': [
        datetime(2020, 1, 15),
        datetime(2019, 5, 20),
        datetime(2018, 3, 10),
        datetime(2021, 7, 1),
        datetime(2017, 11, 25)
    ]
}

# Criar DataFrame
df = pd.DataFrame(data)

# Salvar como Excel
df.to_excel('/home/ubuntu/xls-to-csv-converter/teste_problematico.xlsx', index=False)
print("Arquivo de teste com problemas criado: teste_problematico.xlsx")
print("\nProblemas incluídos:")
print("- Valores INTEGER fora do intervalo (-2147483648 a 2147483647)")
print("- Caracteres especiais e acentuação")
print("- Múltiplos encodings (russo, chinês, árabe, emojis)")
print("- Caracteres de controle inválidos")

