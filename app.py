
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
    /* Fundo gradiente premium */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }

    /* Container principal */
    .main {
        background: transparent;
        padding: 40px 20px !important;
    }

    /* Título principal */
    h1 {
        color: white !important;
        font-size: 3em !important;
        font-weight: 900 !important;
        text-align: center !important;
        margin-bottom: 12px !important;
        text-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
        letter-spacing: -1px !important;
    }

    /* Subtítulo */
    .subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.25em;
        margin-bottom: 45px;
        font-weight: 400;
        letter-spacing: 0.5px;
    }

    /* Container do formulário - Premium Card */
    .form-container {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 25px;
        padding: 60px 50px;
        box-shadow: 0 25px 80px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.5);
    }

    /* Abas - Design Premium */
    .stTabs [role="tablist"] {
        background: linear-gradient(90deg, rgba(255,255,255,0.7) 0%, rgba(255,255,255,0.5) 100%);
        border-radius: 15px;
        padding: 18px;
        gap: 15px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(8px);
    }

    .stTabs [role="tab"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(248,250,252,0.9) 100%) !important;
        border: 2px solid rgba(102, 126, 234, 0.2) !important;
        border-radius: 12px !important;
        padding: 14px 28px !important;
        color: #475569 !important;
        font-weight: 700 !important;
        transition: all 0.35s ease !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
    }

    .stTabs [role="tab"]:hover {
        background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.08) 100%) !important;
        border-color: #667eea !important;
        color: #667eea !important;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.2) !important;
    }

    .stTabs [role="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border-color: #667eea !important;
        color: white !important;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stTabs [role="tabpanel"] {
        padding: 35px 0 !important;
    }

    /* Labels melhorados */
    label {
        color: #1a202c !important;
        font-weight: 700 !important;
        font-size: 1.05em !important;
        margin-bottom: 12px !important;
        letter-spacing: 0.3px !important;
        display: block !important;
    }

    /* Input fields - Premium Design */
    .stTextInput input,
    .stNumberInput input,
    .stDateInput input {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 16px 18px !important;
        font-size: 1.02em !important;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1) !important;
        font-weight: 500 !important;
        color: #1a202c !important;
    }

    .stTextInput input::placeholder,
    .stNumberInput input::placeholder,
    .stDateInput input::placeholder {
        color: #94a3b8 !important;
    }

    .stTextInput input:focus,
    .stNumberInput input:focus,
    .stDateInput input:focus {
        border-color: #667eea !important;
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15), 0 10px 30px rgba(102, 126, 234, 0.1) !important;
    }

    /* Selectbox - Premium */
    .stSelectbox [data-baseweb="select"] {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
        border-radius: 12px !important;
        border: 2px solid #e2e8f0 !important;
        transition: all 0.35s ease !important;
    }
    
    .stSelectbox [data-baseweb="select"]:hover {
        border-color: #667eea !important;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.15) !important;
    }

    /* Botão de submit - Premium */
    .stForm .stFormSubmitButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-weight: 800 !important;
        padding: 18px 50px !important;
        border: none !important;
        border-radius: 12px !important;
        font-size: 1.12em !important;
        transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.35) !important;
        width: 100% !important;
        letter-spacing: 0.6px !important;
        cursor: pointer !important;
    }

    .stForm .stFormSubmitButton > button:hover {
        box-shadow: 0 18px 50px rgba(102, 126, 234, 0.5), 0 0 40px rgba(102, 126, 234, 0.2) !important;
        transform: translateY(-2px) !important;
    }

    .stForm .stFormSubmitButton > button:active {
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3) !important;
        transform: translateY(0) !important;
    }

    /* Mensagens de sucesso */
    .stSuccess {
        background: linear-gradient(135deg, #dcfce7 0%, #c6f6d5 100%) !important;
        border: 2px solid #22c55e !important;
        border-radius: 12px !important;
        padding: 18px !important;
        color: #166534 !important;
        box-shadow: 0 8px 25px rgba(34, 197, 94, 0.2) !important;
        font-weight: 600 !important;
    }

    /* Mensagens de erro */
    .stError {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%) !important;
        border: 2px solid #ef4444 !important;
        border-radius: 12px !important;
        padding: 18px !important;
        color: #991b1b !important;
        box-shadow: 0 8px 25px rgba(239, 68, 68, 0.2) !important;
        font-weight: 600 !important;
    }

    /* Mensagens de info */
    .stInfo {
        background: linear-gradient(135deg, #e0e7ff 0%, #ddd6fe 100%) !important;
        border: 2px solid #6366f1 !important;
        border-radius: 12px !important;
        padding: 18px !important;
        color: #3730a3 !important;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.2) !important;
        font-weight: 600 !important;
    }

    /* Subheader */
    h3 {
        color: #1a202c !important;
        font-weight: 800 !important;
        font-size: 1.35em !important;
        margin-bottom: 28px !important;
        margin-top: 28px !important;
        padding-bottom: 15px !important;
        border-bottom: 3px solid #667eea !important;
    }

    /* Divider */
    hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent, #e2e8f0 20%, #e2e8f0 80%, transparent) !important;
        margin: 35px 0 !important;
    }

    /* Expandable containers */
    .stExpander {
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
    }
    
    .streamlit-expanderHeader {
        background: linear-gradient(90deg, #f0f4f8 0%, #e8ecf1 100%) !important;
        border-radius: 10px !important;
    }

    /* Sidebar */
    .stSidebar {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%) !important;
        box-shadow: 2px 0 15px rgba(0, 0, 0, 0.08) !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: rgba(255, 255, 255, 0.95);
        font-size: 0.95em;
        margin-top: 60px;
        padding: 30px 40px;
        border-top: 2px solid rgba(255, 255, 255, 0.15);
        font-weight: 500;
        letter-spacing: 0.3px;
    }

    /* Responsive */
    @media (max-width: 768px) {
        h1 {
            font-size: 2.2em !important;
        }
        
        .subtitle {
            font-size: 1em !important;
            margin-bottom: 30px !important;
        }

        .form-container {
            padding: 30px 20px;
            border-radius: 20px;
        }

        .stTabs [role="tab"] {
            padding: 10px 18px !important;
            font-size: 0.9em !important;
        }

        .stTabs [role="tablist"] {
            padding: 12px;
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
