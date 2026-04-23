
import streamlit as st
import datetime
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# ============================================================
# CONFIGURAÇÃO DA PÁGINA E TEMA
# ============================================================
st.set_page_config(
    page_title="Sistema de RH - Cadastro de Funcionários",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://www.streamlit.io",
        "Report a bug": None,
        "About": "Sistema de Gestão de Pessoas v1.0"
    }
)

# ============================================================
# ESTILOS CSS CUSTOMIZADOS COM TEMA PROFISSIONAL
# ============================================================
st.markdown("""
<style>
    /* Fundo gradiente */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }

    /* Container principal */
    .main {
        background: transparent;
        padding: 30px !important;
    }

    /* Título principal */
    h1 {
        color: white !important;
        font-size: 2.8em !important;
        font-weight: 900 !important;
        text-align: center !important;
        margin-bottom: 15px !important;
        text-shadow: 0 2px 15px rgba(0, 0, 0, 0.3) !important;
        letter-spacing: -0.5px !important;
    }

    /* Subtítulo */
    .subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.2em;
        margin-bottom: 40px;
        font-weight: 500;
        letter-spacing: 0.3px;
    }

    /* Container do formulário - Glassmorphism Simples */
    .form-container {
        background: rgba(255, 255, 255, 0.96);
        border-radius: 18px;
        padding: 45px 40px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.4);
    }

    /* Abas */
    .stTabs [role="tablist"] {
        background: #f1f5f9;
        border-radius: 12px;
        padding: 12px;
        gap: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }

    .stTabs [role="tab"] {
        background-color: white !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        color: #475569 !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }

    .stTabs [role="tab"]:hover {
        background-color: #f8fafc !important;
        border-color: #667eea !important;
        color: #667eea !important;
    }

    .stTabs [role="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border-color: transparent !important;
        color: white !important;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.25) !important;
    }
    
    .stTabs [role="tabpanel"] {
        padding: 25px 0 !important;
    }

    /* Expandable containers */
    .stExpander {
        border: 2px solid #e2e8f0 !important;
        border-radius: 10px !important;
        background-color: #f8fafc !important;
    }
    
    .streamlit-expanderHeader {
        background-color: #f0f4f8 !important;
        border-radius: 8px !important;
    }

    /* Labels */
    label {
        color: #1e293b !important;
        font-weight: 600 !important;
        font-size: 1.02em !important;
        margin-bottom: 8px !important;
    }

    /* Input fields */
    .stTextInput input,
    .stNumberInput input,
    .stDateInput input {
        background-color: #f8fafc !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 10px !important;
        padding: 12px 14px !important;
        font-size: 1em !important;
        transition: all 0.3s ease !important;
    }

    .stTextInput input:focus,
    .stNumberInput input:focus,
    .stDateInput input:focus {
        border-color: #667eea !important;
        background-color: #ffffff !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }

    /* Selectbox */
    .stSelectbox [data-baseweb="select"] {
        background-color: #f8fafc !important;
        border-radius: 10px !important;
    }

    /* Botão de submit */
    .stForm .stFormSubmitButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        padding: 14px 40px !important;
        border: none !important;
        border-radius: 10px !important;
        font-size: 1.1em !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3) !important;
        width: 100% !important;
    }

    .stForm .stFormSubmitButton > button:hover {
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4) !important;
    }

    .stForm .stFormSubmitButton > button:active {
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2) !important;
    }

    /* Mensagens de sucesso */
    .stSuccess {
        background-color: #dcfce7 !important;
        border: 2px solid #16a34a !important;
        border-radius: 10px !important;
        padding: 16px !important;
        color: #15803d !important;
        box-shadow: 0 4px 12px rgba(22, 163, 74, 0.15) !important;
    }

    /* Mensagens de erro */
    .stError {
        background-color: #fee2e2 !important;
        border: 2px solid #dc2626 !important;
        border-radius: 10px !important;
        padding: 16px !important;
        color: #b91c1c !important;
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.15) !important;
    }

    /* Mensagens de info */
    .stInfo {
        background-color: #e0e7ff !important;
        border: 2px solid #4f46e5 !important;
        border-radius: 10px !important;
        padding: 16px !important;
        color: #3730a3 !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.15) !important;
    }

    /* Subheader */
    h3 {
        color: #1e293b !important;
        font-weight: 700 !important;
        font-size: 1.25em !important;
        margin-bottom: 20px !important;
        margin-top: 20px !important;
        padding-bottom: 10px !important;
        border-bottom: 3px solid #667eea !important;
    }

    /* Divider */
    hr {
        border: none !important;
        height: 1px !important;
        background: #e2e8f0 !important;
        margin: 25px 0 !important;
    }

    /* Sidebar */
    .stSidebar {
        background-color: #f8fafc !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.9em;
        margin-top: 40px;
        padding: 25px;
        border-top: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* Responsive */
    @media (max-width: 768px) {
        h1 {
            font-size: 1.8em !important;
        }
        
        .subtitle {
            font-size: 0.95em !important;
            margin-bottom: 25px !important;
        }

        .form-container {
            padding: 20px;
        }

        .stTabs [role="tab"] {
            padding: 8px 16px !important;
            font-size: 0.85em !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# BARRA LATERAL COM INFORMAÇÕES
# ============================================================
with st.sidebar:
    st.markdown("### 📊 Sistema de RH")
    st.markdown("""
    **Versão:** 1.0
    
    **Funcionalidades:**
    - ✅ Cadastro de funcionários
    - ✅ Dados pessoais
    - ✅ Informações corporativas
    - ✅ Contatos de emergência
    """)
    
    st.markdown("---")
    
    st.markdown("### 📈 Estatísticas")
    try:
        conn_sidebar = st.connection("gsheets", type=GSheetsConnection)
        dados_sidebar = conn_sidebar.read(worksheet="Dados", ttl=60)
        if dados_sidebar is not None and len(dados_sidebar) > 0:
            st.metric("👥 Total de Funcionários", len(dados_sidebar))
            if 'Departamento' in dados_sidebar.columns:
                st.metric("🏢 Departamentos Únicos", dados_sidebar['Departamento'].nunique())
    except:
        st.info("ℹ️ Conecte a planilha para ver estatísticas")

# ============================================================
# CONTEÚDO PRINCIPAL
# ============================================================
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("# 🏢 Sistema de Cadastro de Funcionários")
    st.markdown('<div class="subtitle">Gerencie os dados dos seus colaboradores de forma segura e organizada</div>', unsafe_allow_html=True)

# CONEXÃO COM O GOOGLE SHEETS
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error(f"❌ Erro ao conectar com Google Sheets: {e}")
    st.stop()

# ============================================================
# FORMULÁRIO PRINCIPAL
# ============================================================
with st.container():
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    
    with st.form("cadastro_form", border=False):
        
        # Abas
        aba1, aba2, aba3 = st.tabs(["👤 Dados Pessoais", "💼 Dados Corporativos", "🏥 Saúde e Emergência"])
        
        # ========== ABA 1: DADOS PESSOAIS ==========
        with aba1:
            st.subheader("📋 Informações Pessoais")
            
            col1, col2 = st.columns(2)
            
            with col1:
                nome = st.text_input(
                    "Nome completo",
                    placeholder="Ex: João da Silva",
                    help="Digite o nome completo do funcionário"
                )
            
            with col2:
                data_nascimento = st.date_input(
                    "Data de Nascimento",
                    format="DD/MM/YYYY",
                    min_value=datetime.date(1920, 1, 1),
                    max_value=datetime.date.today(),
                    help="Selecione a data de nascimento"
                )
            
            col3, col4 = st.columns(2)
            
            with col3:
                cpf = st.text_input(
                    "CPF",
                    placeholder="XXX.XXX.XXX-XX",
                    help="Digite o CPF"
                )
            
            with col4:
                sexo = st.selectbox(
                    "Sexo",
                    ["Selecione...", "Masculino", "Feminino", "Outro", "Prefiro não informar"],
                    help="Selecione o sexo"
                )
        
        # ========== ABA 2: DADOS CORPORATIVOS ==========
        with aba2:
            st.subheader("💼 Informações Profissionais")
            
            col1, col2 = st.columns(2)
            
            with col1:
                cargo = st.text_input(
                    "Cargo",
                    placeholder="Ex: Desenvolvedor",
                    help="Digite o cargo do funcionário"
                )
            
            with col2:
                departamento = st.selectbox(
                    "Departamento",
                    ["Selecione...", "TI", "RH", "Financeiro", "Operações", "Vendas", "Diretoria"],
                    help="Selecione o departamento"
                )
            
            col3, col4 = st.columns(2)
            
            with col3:
                escolaridade = st.selectbox(
                    "Escolaridade",
                    ["Selecione...", "Ensino Fundamental", "Ensino Médio", "Ensino Superior", "Pós-graduação"],
                    help="Selecione o nível de escolaridade"
                )
            
            with col4:
                salario = st.number_input(
                    "Salário Base (R$)",
                    min_value=0.0,
                    step=100.0,
                    format="%.2f",
                    help="Digite o salário base do funcionário"
                )
        
        # ========== ABA 3: SAÚDE E EMERGÊNCIA ==========
        with aba3:
            st.subheader("🏥 Informações de Saúde e Emergência")
            
            col1, col2 = st.columns(2)
            
            with col1:
                contato_emergencia = st.text_input(
                    "Nome do Contato de Emergência",
                    placeholder="Ex: Maria Silva",
                    help="Digite o nome do contato de emergência"
                )
            
            with col2:
                telefone_emergencia = st.text_input(
                    "Telefone de Emergência",
                    placeholder="(XX) XXXXX-XXXX",
                    help="Digite o telefone do contato de emergência"
                )
            
            col3, col4 = st.columns(2)
            
            with col3:
                tipo_sanguineo = st.selectbox(
                    "Tipo Sanguíneo",
                    ["Selecione...", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Não sei"],
                    help="Selecione o tipo sanguíneo"
                )
            
            with col4:
                st.info("ℹ️ Preencha todos os campos com informações de segurança importantes")
        
        # ========== BOTÃO DE ENVIO ==========
        st.markdown("---")
        col_botao = st.columns([1, 1, 1])
        with col_botao[1]:
            submit_button = st.form_submit_button(
                "✅ Salvar Cadastro Completo",
                use_container_width=True
            )
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# AÇÃO APÓS CLIQUE NO BOTÃO
# ============================================================
if submit_button:
    # Validações
    erros = []
    
    if not nome or nome.strip() == "":
        erros.append("❌ Nome completo é obrigatório")
    
    if sexo == "Selecione...":
        erros.append("❌ Sexo é obrigatório")
    
    if departamento == "Selecione...":
        erros.append("❌ Departamento é obrigatório")
    
    if escolaridade == "Selecione...":
        erros.append("❌ Escolaridade é obrigatória")
    
    if tipo_sanguineo == "Selecione...":
        erros.append("❌ Tipo sanguíneo é obrigatório")
    
    if not contato_emergencia or contato_emergencia.strip() == "":
        erros.append("❌ Contato de emergência é obrigatório")
    
    if not telefone_emergencia or telefone_emergencia.strip() == "":
        erros.append("❌ Telefone de emergência é obrigatório")
    
    # Se houver erros, mostrar
    if erros:
        st.error("⚠️ Por favor, corrija os seguintes erros:")
        for erro in erros:
            st.error(erro)
    else:
        # Criar dicionário com dados
        novo_funcionario = {
            "Nome": nome.strip(),
            "Nascimento": data_nascimento.strftime("%d/%m/%Y"),
            "CPF": cpf.strip(),
            "Sexo": sexo,
            "Cargo": cargo.strip(),
            "Departamento": departamento,
            "Escolaridade": escolaridade,
            "Salario": float(salario),
            "Contato_Emergencia": contato_emergencia.strip(),
            "Telefone_Emergencia": telefone_emergencia.strip(),
            "Tipo_Sanguineo": tipo_sanguineo,
            "Data_Cadastro": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        
        try:
            # Ler dados existentes
            dados_existentes = conn.read(worksheet="Dados", ttl=0)
            
            # Se a planilha está vazia, criar com headers
            if dados_existentes is None or len(dados_existentes) == 0:
                dados_existentes = pd.DataFrame()
            
            # Adicionar nova linha
            df_novo = pd.DataFrame([novo_funcionario])
            dados_atualizados = pd.concat([dados_existentes, df_novo], ignore_index=True)
            
            # Salvar de volta
            conn.update(worksheet="Dados", data=dados_atualizados)
            
            # Mensagem de sucesso
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.success(f"✅ Funcionário **{nome}** cadastrado com sucesso!")
                st.balloons()
            
            # Informações do cadastro
            with st.expander("📋 Ver Dados Cadastrados"):
                st.dataframe(df_novo, use_container_width=True)
            
        except Exception as e:
            st.error(f"❌ Erro ao guardar na planilha: {str(e)}")
            st.error("Verifique se a planilha 'Dados' existe e está acessível")

# ============================================================
# RODAPÉ
# ============================================================
st.markdown("""
<div class="footer">
    <p>© 2024 Sistema de Gestão de Pessoas | Versão 1.0 | Desenvolvido com ❤️ usando Streamlit</p>
</div>
""", unsafe_allow_html=True)
