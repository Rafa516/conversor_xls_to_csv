# 🚀 Guia de Início Rápido

## Instalação e Execução

### 1. Instalar Dependências

```bash
cd xls-to-csv-converter
pip install -r requirements.txt
```

### 2. Executar a Aplicação

```bash
streamlit run app.py
```

A aplicação abrirá automaticamente no navegador em `http://localhost:8501`

## Como Usar

### Passo 1: Upload
Clique em **"Browse files"** e selecione seu arquivo XLS ou XLSX.

### Passo 2: Visualização
Confira os dados carregados na tabela. Você verá:
- Número total de linhas e colunas
- Uso de memória
- Tabela completa com todos os dados

### Passo 3: Metadados
Configure o tipo de dado para cada coluna:
- **varchar**: Texto (padrão para strings)
- **int**: Números inteiros
- **float**: Números decimais
- **bool**: Verdadeiro/Falso
- **datetime**: Datas e horários

Cada coluna mostra exemplos dos valores para ajudar na escolha.

### Passo 4: Seleção
Marque as colunas que deseja incluir no CSV final:
- Use **"✅ Selecionar Todas"** para marcar todas
- Use **"❌ Desselecionar Todas"** para desmarcar todas
- Ou marque individualmente cada coluna desejada

### Passo 5: Preview
Visualize como ficará o arquivo CSV final:
- Tabela com os dados que serão exportados
- Informações sobre os tipos de dados aplicados

### Passo 6: Download
Clique em **"⬇️ Baixar CSV"** para baixar o arquivo convertido.

O arquivo será salvo como `[nome_original]_convertido.csv`

## Exemplo Incluído

O projeto inclui um arquivo de exemplo: `exemplo_funcionarios.xlsx`

Este arquivo contém dados fictícios de funcionários com diferentes tipos de dados (texto, números, datas, booleanos) para você testar todas as funcionalidades.

## Dicas

💡 **Conversão de Tipos**: A aplicação tenta converter os dados automaticamente. Se houver valores incompatíveis (ex: texto em coluna numérica), eles serão tratados adequadamente.

💡 **Encoding**: O CSV é gerado com encoding UTF-8 com BOM, garantindo compatibilidade com Excel e outros programas.

💡 **Memória**: Para arquivos muito grandes, considere selecionar apenas as colunas necessárias para reduzir o tamanho do arquivo final.

## Estrutura do Projeto

```
xls-to-csv-converter/
├── app.py                          # Aplicação principal
├── requirements.txt                # Dependências Python
├── README.md                       # Documentação completa
├── INICIO_RAPIDO.md               # Este guia
├── TESTE_VALIDACAO.md             # Relatório de testes
├── create_sample.py               # Script para criar arquivo de exemplo
└── exemplo_funcionarios.xlsx      # Arquivo de exemplo
```

## Solução de Problemas

**A aplicação não inicia?**
- Verifique se instalou todas as dependências: `pip install -r requirements.txt`
- Confirme que está usando Python 3.8 ou superior

**Erro ao carregar arquivo?**
- Verifique se o arquivo está no formato XLS ou XLSX
- Tente abrir o arquivo no Excel para confirmar que não está corrompido

**Tipos de dados não aplicados corretamente?**
- Verifique o preview da saída antes de baixar
- Alguns valores podem não ser convertíveis (a aplicação trata esses casos automaticamente)

## Suporte

Para mais informações, consulte o arquivo `README.md` incluído no projeto.

