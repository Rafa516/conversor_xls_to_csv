# 📊 Conversor XLS para CSV

Aplicação web desenvolvida com Streamlit para converter arquivos Excel (XLS/XLSX) em CSV com controle total sobre metadados e seleção de colunas.

## 🎯 Funcionalidades

- **Upload de arquivos**: Suporte para formatos XLS e XLSX
- **Visualização de dados**: Preview completo dos dados de entrada e saída
- **Edição de metadados**: Configure o tipo de dado de cada coluna (varchar, int, float, bool, datetime)
- **Seleção de colunas**: Escolha quais colunas incluir no arquivo CSV final
- **Interface intuitiva**: Design limpo e fácil de usar com instruções passo a passo
- **Download direto**: Baixe o arquivo CSV convertido com um clique

## 🚀 Como Executar

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. Clone ou baixe este repositório
2. Navegue até o diretório do projeto:
   ```bash
   cd xls-to-csv-converter
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

### Executar a Aplicação

Execute o seguinte comando no terminal:

```bash
streamlit run app.py
```

A aplicação será aberta automaticamente no seu navegador padrão em `http://localhost:8501`

## 📖 Como Usar

### Passo 1: Upload do Arquivo
- Clique no botão de upload
- Selecione seu arquivo XLS ou XLSX
- Aguarde o carregamento

### Passo 2: Visualização dos Dados
- Confira os dados carregados na tabela
- Veja estatísticas básicas (número de linhas, colunas, memória)

### Passo 3: Configuração de Metadados
- Para cada coluna, você verá:
  - Nome da coluna
  - Exemplos de valores
  - Seletor de tipo de dado
- Escolha o tipo apropriado:
  - **varchar**: Texto/string
  - **int**: Números inteiros
  - **float**: Números decimais
  - **bool**: Valores booleanos (True/False)
  - **datetime**: Datas e horários

### Passo 4: Seleção de Colunas
- Marque as colunas que deseja incluir no CSV final
- Use os botões "Selecionar Todas" ou "Desselecionar Todas" para facilitar
- Cada checkbox mostra o nome da coluna e seu tipo configurado

### Passo 5: Preview da Saída
- Visualize como ficará o arquivo CSV final
- Confira os tipos de dados aplicados
- Veja a tabela com informações detalhadas sobre cada coluna

### Passo 6: Download
- Clique no botão "Baixar CSV"
- O arquivo será salvo com o nome original + "_convertido.csv"

## 🎨 Características da Interface

- **Layout responsivo**: Funciona em diferentes tamanhos de tela
- **Sidebar com instruções**: Guia passo a passo sempre visível
- **Feedback visual**: Mensagens de sucesso, erro e avisos
- **Métricas em destaque**: Estatísticas importantes em cards
- **Organização por seções**: Cada etapa claramente separada

## 🔧 Tecnologias Utilizadas

- **Streamlit**: Framework para criação de aplicações web
- **Pandas**: Manipulação e análise de dados
- **OpenPyXL**: Leitura de arquivos XLSX
- **XLRD**: Leitura de arquivos XLS

## 📝 Notas Importantes

- A aplicação mantém o estado durante a sessão usando `st.session_state`
- Conversões de tipo são feitas com tratamento de erros para evitar falhas
- O encoding do CSV é UTF-8 com BOM para compatibilidade com Excel
- Valores inválidos em conversões numéricas são tratados automaticamente

## 🐛 Solução de Problemas

**Erro ao carregar arquivo:**
- Verifique se o arquivo está no formato XLS ou XLSX
- Certifique-se de que o arquivo não está corrompido
- Tente abrir o arquivo no Excel primeiro para validar

**Tipos de dados não aplicados corretamente:**
- Alguns valores podem não ser convertíveis (ex: texto para número)
- Verifique o preview da saída para confirmar as conversões
- Ajuste os tipos conforme necessário

**Aplicação não inicia:**
- Verifique se todas as dependências foram instaladas
- Confirme que está usando Python 3.8 ou superior
- Execute `pip install -r requirements.txt` novamente

## 📄 Licença

Este projeto é de código aberto e está disponível para uso livre.

## 🤝 Contribuições

Sugestões e melhorias são bem-vindas!

