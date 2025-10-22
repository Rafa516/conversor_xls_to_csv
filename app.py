import streamlit as st
import pandas as pd
import io
from typing import Dict, List

# Configuração da página
st.set_page_config(
    page_title="Conversor XLS para CSV",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título e descrição
st.title("📊 Conversor XLS para CSV")
st.markdown("""
Esta aplicação permite converter arquivos Excel (XLS/XLSX) para CSV com controle total sobre:
- **Visualização** dos dados de entrada e saída
- **Edição de metadados** das colunas (tipos e tamanhos)
- **Seleção de colunas** para exportação
""")

# Sidebar com instruções
with st.sidebar:
    st.header("📖 Como usar")
    st.markdown("""
    ### Passo 1: Upload
    Faça upload do seu arquivo XLS ou XLSX
    
    ### Passo 2: Visualização
    Confira os dados carregados na tabela
    
    ### Passo 3: Metadados
    Veja e edite os tipos de dados das colunas.
    - Se o tipo for `varchar`, defina o **Tamanho** máximo.
    
    ### Passo 4: Seleção
    Escolha quais colunas incluir no CSV
    
    ### Passo 5: Download
    Baixe o arquivo CSV convertido
    """)
    
    st.divider()
    st.markdown("""**💡 Dicas:**
    - Use **INT** para números pequenos (-2B a 2B)
    - Use **BIGINT** para números grandes
    - Use **VARCHAR** e defina o **Tamanho** para corresponder à sua tabela no banco (ex: 50 para `varchar(50)`).
    - A aplicação detecta e corrige automaticamente:
      - Inteiros fora do intervalo
      - Caracteres inválidos UTF-8
      - **Textos maiores que o limite (truncando)**
    """)

# Inicializar estado da sessão
if 'df' not in st.session_state:
    st.session_state.df = None
if 'column_types' not in st.session_state:
    st.session_state.column_types = {}
# NOVO: Estado para armazenar os tamanhos das colunas
if 'column_lengths' not in st.session_state:
    st.session_state.column_lengths = {}
if 'selected_columns' not in st.session_state:
    st.session_state.selected_columns = []

# Função para inferir tipo de dado
def infer_dtype(series):
    """Infere o tipo de dado de uma série pandas"""
    dtype = str(series.dtype)
    if 'int' in dtype:
        return 'int'
    elif 'float' in dtype:
        return 'float'
    elif 'bool' in dtype:
        return 'bool'
    elif 'datetime' in dtype:
        return 'datetime'
    else:
        return 'varchar'

# Função para validar e limitar valores inteiros
def validate_int_range(value, use_bigint=False):
    """Valida se o valor está dentro do intervalo de INTEGER ou BIGINT do PostgreSQL"""
    try:
        val = float(value)
        if pd.isna(val):
            return 0
        
        if use_bigint:
            # Limite do BIGINT no PostgreSQL: -9223372036854775808 a 9223372036854775807
            if val > 9223372036854775807:
                return 9223372036854775807
            elif val < -9223372036854775808:
                return -9223372036854775808
        else:
            # Limite do INTEGER no PostgreSQL: -2147483648 a 2147483647
            if val > 2147483647:
                return 2147483647
            elif val < -2147483648:
                return -2147483648
        
        return int(val)
    except:
        return 0

# Função para limpar strings com problemas de encoding
def clean_string(value):
    """Remove caracteres inválidos e garante encoding UTF-8 correto"""
    try:
        if pd.isna(value):
            return ''
        # Converter para string
        text = str(value)
        # Remover caracteres de controle e não-UTF-8
        text = text.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
        # Remover caracteres de controle exceto quebras de linha e tabs
        text = ''.join(char for char in text if char.isprintable() or char in '\n\r\t')
        return text.strip()
    except:
        return ''

# Função para converter tipo de dado
# MODIFICADO: Adicionado 'max_len' para truncar varchars
def convert_dtype(series, target_type, max_len=None):
    """Converte uma série para o tipo de dado especificado com tratamento robusto de erros"""
    try:
        if target_type == 'int':
            # Aplicar validação de intervalo para cada valor (INTEGER)
            return series.apply(lambda x: validate_int_range(x, use_bigint=False))
        elif target_type == 'bigint':
            # Aplicar validação de intervalo para cada valor (BIGINT)
            return series.apply(lambda x: validate_int_range(x, use_bigint=True))
        elif target_type == 'float':
            return pd.to_numeric(series, errors='coerce')
        elif target_type == 'bool':
            return series.astype(bool)
        elif target_type == 'datetime':
            return pd.to_datetime(series, errors='coerce')
        else:  # varchar
            # Limpar strings para garantir UTF-8 válido
            cleaned_series = series.apply(clean_string)
            
            # NOVO: Truncar a string se max_len for fornecido
            if max_len is not None and max_len > 0:
                return cleaned_series.str[:max_len]
            else:
                return cleaned_series
                
    except Exception as e:
        st.warning(f"Aviso ao converter coluna: {str(e)}")
        return series

# Upload do arquivo
st.header("1️⃣ Upload do Arquivo")
uploaded_file = st.file_uploader(
    "Escolha um arquivo XLS ou XLSX",
    type=['xls', 'xlsx'],
    help="Selecione o arquivo Excel que deseja converter para CSV"
)

if uploaded_file is not None:
    try:
        # Ler o arquivo Excel
        df = pd.read_excel(uploaded_file)
        st.session_state.df = df
        
        # Inicializar tipos de colunas se necessário
        if not st.session_state.column_types:
            st.session_state.column_types = {col: infer_dtype(df[col]) for col in df.columns}
        
        # NOVO: Inicializar tamanhos das colunas (default 255)
        if not st.session_state.column_lengths:
            st.session_state.column_lengths = {col: 255 for col in df.columns}
            
        # Inicializar colunas selecionadas se necessário
        if not st.session_state.selected_columns:
            st.session_state.selected_columns = list(df.columns)
        
        st.success(f"✅ Arquivo carregado com sucesso! {len(df)} linhas e {len(df.columns)} colunas")
        
        # Visualização dos dados de entrada
        st.header("2️⃣ Visualização dos Dados de Entrada")
        st.markdown(f"**Total de registros:** {len(df)}")
        
        # Mostrar estatísticas básicas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Linhas", len(df))
        with col2:
            st.metric("Colunas", len(df.columns))
        with col3:
            st.metric("Memória", f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB")
        
        # Tabela de dados
        st.dataframe(df, use_container_width=True, height=300)
        
        # Edição de metadados
        st.header("3️⃣ Metadados das Colunas")
        st.markdown("Configure o tipo de dado e o tamanho (para `varchar`) de cada coluna:")
        
        # Criar colunas para exibir metadados
        type_options = ['varchar', 'int', 'bigint', 'float', 'bool', 'datetime']
        
        # Dividir em 2 colunas para melhor layout
        cols_per_row = 2
        columns = list(df.columns)
        
        for i in range(0, len(columns), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, col_name in enumerate(columns[i:i+cols_per_row]):
                with cols[j]:
                    st.markdown(f"**{col_name}**")
                    
                    # Mostrar exemplo de dados
                    sample_values = df[col_name].dropna().head(3).tolist()
                    st.caption(f"Exemplo: {sample_values}")
                    
                    # Seletor de tipo
                    current_type = st.session_state.column_types.get(col_name, 'varchar')
                    new_type = st.selectbox(
                        "Tipo de dado",
                        options=type_options,
                        index=type_options.index(current_type),
                        key=f"type_{col_name}"
                    )
                    st.session_state.column_types[col_name] = new_type
                    
                    # NOVO: Campo de tamanho para Varchar
                    if new_type == 'varchar':
                        default_len = st.session_state.column_lengths.get(col_name, 255)
                        new_len = st.number_input(
                            "Tamanho (max)",
                            min_value=1,
                            value=default_len,
                            key=f"len_{col_name}",
                            help="Define o tamanho máximo para colunas de texto (varchar). Valores maiores serão truncados (cortados)."
                        )
                        st.session_state.column_lengths[col_name] = int(new_len)
                    
                    st.divider()
        
        # Seleção de colunas
        st.header("4️⃣ Seleção de Colunas para Exportação")
        st.markdown("Escolha quais colunas deseja incluir no arquivo CSV final:")
        
        # Opção de selecionar/desselecionar todas
        col_select_all, col_deselect_all = st.columns(2)
        with col_select_all:
            if st.button("✅ Selecionar Todas", use_container_width=True):
                st.session_state.selected_columns = list(df.columns)
                st.rerun()
        with col_deselect_all:
            if st.button("❌ Desselecionar Todas", use_container_width=True):
                st.session_state.selected_columns = []
                st.rerun()
        
        # Checkboxes para cada coluna
        selected_columns = []
        cols_per_row = 3
        for i in range(0, len(columns), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, col_name in enumerate(columns[i:i+cols_per_row]):
                with cols[j]:
                    # MODIFICADO: Mostra o tamanho do varchar no label
                    col_type = st.session_state.column_types[col_name]
                    if col_type == 'varchar':
                        col_len = st.session_state.column_lengths.get(col_name, 255)
                        label = f"{col_name} ({col_type}[{col_len}])"
                    else:
                        label = f"{col_name} ({col_type})"
                        
                    is_selected = st.checkbox(
                        label,
                        value=col_name in st.session_state.selected_columns,
                        key=f"select_{col_name}"
                    )
                    if is_selected:
                        selected_columns.append(col_name)
        
        st.session_state.selected_columns = selected_columns
        
        # Preview dos dados de saída
        if st.session_state.selected_columns:
            st.header("5️⃣ Preview dos Dados de Saída")
            st.markdown(f"**Colunas selecionadas:** {len(st.session_state.selected_columns)}")
            
            # Criar DataFrame de saída com tipos convertidos
            output_df = df[st.session_state.selected_columns].copy()
            
            # Aplicar conversões de tipo
            for col in st.session_state.selected_columns:
                target_type = st.session_state.column_types[col]
                
                # MODIFICADO: Passar o max_len para a função de conversão
                max_len = None
                if target_type == 'varchar':
                    max_len = st.session_state.column_lengths.get(col, 255)
                    
                output_df[col] = convert_dtype(output_df[col], target_type, max_len=max_len)
            
            # Mostrar preview
            st.dataframe(output_df, use_container_width=True, height=300)
            
            # Mostrar informações sobre os tipos finais
            st.subheader("Tipos de Dados Finais")
            type_info_list = []
            for col in output_df.columns:
                col_type = st.session_state.column_types[col]
                if col_type == 'varchar':
                    col_len = st.session_state.column_lengths.get(col, 255)
                    config_type = f"varchar[{col_len}]"
                else:
                    config_type = col_type
                
                type_info_list.append({
                    'Coluna': col,
                    'Tipo Configurado': config_type,
                    'Tipo Pandas': str(output_df[col].dtype)
                })
                
            type_info = pd.DataFrame(type_info_list)
            st.dataframe(type_info, use_container_width=True, hide_index=True)
            
            # Download do CSV
            st.header("6️⃣ Download do Arquivo CSV")
            
            # Detectar problemas antes da exportação
            st.subheader("⚠️ Validação de Dados")
            
            warnings = []
            
            # Verificar inteiros fora do intervalo
            for col in st.session_state.selected_columns:
                col_type = st.session_state.column_types[col]
                if col_type in ['int', 'bigint']:
                    original_values = df[col]
                    
                    try:
                        numeric_original = pd.to_numeric(original_values, errors='coerce')
                        
                        if col_type == 'int':
                            out_of_range = ((numeric_original > 2147483647) | (numeric_original < -2147483648)).sum()
                            if out_of_range > 0:
                                warnings.append(f"🔴 **{col}**: {out_of_range} valor(es) fora do intervalo INTEGER foram ajustados para o limite (-2147483648 a 2147483647). Considere usar BIGINT.")
                        elif col_type == 'bigint':
                            out_of_range = ((numeric_original > 9223372036854775807) | (numeric_original < -9223372036854775808)).sum()
                            if out_of_range > 0:
                                warnings.append(f"🔴 **{col}**: {out_of_range} valor(es) fora do intervalo BIGINT foram ajustados para o limite (-9223372036854775808 a 9223372036854775807)")
                    except:
                        pass
            
            # NOVO: Verificar truncamento de strings
            for col in st.session_state.selected_columns:
                if st.session_state.column_types[col] == 'varchar':
                    try:
                        max_len = st.session_state.column_lengths.get(col, 255)
                        # Compara o tamanho da string original (apenas limpando, sem truncar)
                        original_cleaned_len = df[col].apply(clean_string).str.len()
                        truncated_count = (original_cleaned_len > max_len).sum()
                        
                        if truncated_count > 0:
                            warnings.append(f"🟠 **{col}**: {truncated_count} valor(es) excederam o limite de {max_len} caracteres e foram **truncados**.")
                    except:
                        pass
                        
            # Verificar problemas de encoding
            for col in st.session_state.selected_columns:
                if st.session_state.column_types[col] == 'varchar':
                    try:
                        original_values = df[col].astype(str)
                        cleaned_count = 0
                        for val in original_values:
                            if val != clean_string(val):
                                cleaned_count += 1
                        if cleaned_count > 0:
                            warnings.append(f"🟡 **{col}**: {cleaned_count} valor(es) com caracteres inválidos foram limpos para garantir UTF-8 válido")
                    except:
                        pass
            
            if warnings:
                st.warning("🚨 **Atenção**: Alguns problemas foram detectados e corrigidos automaticamente:")
                for warning in warnings:
                    st.markdown(warning)
            else:
                st.success("✅ Nenhum problema detectado! Os dados estão prontos para exportação.")
            
            st.divider()
            
            # Opções de exportação
            st.subheader("⚙️ Opções de Exportação")
            
            col1, col2 = st.columns(2)
            with col1:
                encoding_option = st.selectbox(
                    "Encoding do CSV",
                    options=['utf-8-sig', 'utf-8', 'latin1', 'iso-8859-1'],
                    index=0,
                    help="UTF-8-sig é recomendado para compatibilidade com Excel e bancos de dados"
                )
            with col2:
                separator_option = st.selectbox(
                    "Separador",
                    options=[',', ';', '|', '\\t'],
                    index=0,
                    help="Vírgula é o padrão, mas ponto-e-vírgula pode ser necessário em algumas regiões"
                )
            
            # Converter separador
            sep = separator_option if separator_option != '\\t' else '\t'
            
            # Converter para CSV
            csv_buffer = io.StringIO()
            output_df.to_csv(csv_buffer, index=False, encoding=encoding_option, sep=sep)
            csv_data = csv_buffer.getvalue()
            
            # Botão de download
            st.download_button(
                label="⬇️ Baixar CSV",
                data=csv_data,
                file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}_convertido.csv",
                mime="text/csv",
                use_container_width=True
            )
            
            st.success("✅ Arquivo pronto para download!")
            
        else:
            st.warning("⚠️ Selecione pelo menos uma coluna para exportar.")
            
    except Exception as e:
        st.error(f"❌ Erro ao processar o arquivo: {str(e)}")
        st.info("Verifique se o arquivo está no formato correto (XLS ou XLSX) e não está corrompido.")

else:
    st.info("👆 Faça upload de um arquivo XLS ou XLSX para começar.")
    
    # Mostrar exemplo visual
    st.markdown("---")
    st.subheader("📸 Exemplo de Uso")
    st.markdown("""
    1. **Upload**: Clique no botão acima e selecione seu arquivo Excel
    2. **Visualize**: Confira os dados carregados na tabela
    3. **Configure**: Ajuste os tipos de dados e **tamanhos de varchar**
    4. **Selecione**: Marque as colunas que deseja exportar
    5. **Baixe**: Clique no botão de download para obter seu CSV
    """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Conversor XLS para CSV | Desenvolvido com Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)