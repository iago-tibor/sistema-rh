import streamlit as st
import datetime
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.title("Sistema de Cadastro de Funcionários 🏢")

# CONEXÃO COM O GOOGLE SHEETS
conn = st.connection("gsheets", type=GSheetsConnection)

# 1. Abrir o formulário principal
with st.form("cadastro_form"):
    
    # 2. Criar as abas e damos nomes a elas
    aba1, aba2, aba3 = st.tabs(["👤 Dados Pessoais", "💼 Dados Corporativos", "🏥 Saúde e Emergência"])
    
    # 3. Preencher a primeira aba com dados pessoais
    with aba1:
        st.subheader("Informações Pessoais")
        nome = st.text_input("Nome completo *")
        data_nascimento = st.date_input("Data de Nascimento", format="DD/MM/YYYY", min_value=datetime.date(1920, 1, 1))
        cpf = st.text_input("CPF")
        sexo = st.selectbox("Sexo", ["Masculino", "Feminino", "Outro", "Prefiro não informar"])
        
    # 4. Preencher a segunda aba com os dados profissionais
    with aba2:
        st.subheader("Informações Profissionais")
        cargo = st.text_input("Cargo")
        departamento = st.selectbox("Departamento", ["TI", "RH", "Financeiro", "Operações", "Vendas", "Diretoria"])
        escolaridade = st.selectbox("Escolaridade", ["Ensino Fundamental", "Ensino Médio", "Ensino Superior", "Pós-graduação"])
        salario = st.number_input("Salário Base (R$)", min_value=0.0, step=100.0)
        
    # 5. Preencher a terceira aba com dados da saúde
    with aba3:
        st.subheader("Informações de Saúde e Segurança")
        contato_emergencia = st.text_input("Nome do Contato de Emergência")
        telefone_emergencia = st.text_input("Telefone de Emergência")
        tipo_sanguineo = st.selectbox("Tipo Sanguíneo", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Não sei"])

    # 6. Eviar
    st.markdown("---")
    submit_button = st.form_submit_button("Salvar Cadastro Completo")

# AÇÃO QUE OCORRE APÓS O CLIQUE NO BOTÃO
if submit_button:
    if nome != "":
        # 1. Criamos um "dicionário" com os dados exatos que vão para a planilha
        novo_funcionario = {
            "Nome": nome,
            "Nascimento": data_nascimento.strftime("%d/%m/%Y"),
            "CPF": cpf,
            "Sexo": sexo,
            "Cargo": cargo,
            "Departamento": departamento,
            "Escolaridade": escolaridade,
            "Salario": float(salario),
            "Contato_Emergencia": contato_emergencia,
            "Telefone_Emergencia": telefone_emergencia,
            "Tipo_Sanguineo": tipo_sanguineo
        }
        
        try:
            # 2. Lemos a planilha atual
            dados_existentes = conn.read(worksheet="Dados", ttl=0)
            
            # 3. Adicionamos a nova linha aos dados
            df_novo = pd.DataFrame([novo_funcionario])
            dados_atualizados = pd.concat([dados_existentes, df_novo], ignore_index=True)
            
            # 4. Guardamos tudo de volta no Google Sheets
            conn.update(worksheet="Dados", data=dados_atualizados)
            
            st.success(f"Funcionário {nome} guardado na base de dados com sucesso! ✅")
            st.balloons() # Animação de balões na tela!
            
        except Exception as e:
            st.error(f"Erro ao guardar na planilha: {e}")
            
    else:
        st.error("Por favor, preencha o campo obrigatório de Nome completo.")
