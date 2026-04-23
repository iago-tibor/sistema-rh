import streamlit as st
import datetime
import re
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================
st.set_page_config(
    page_title="Sistema de RH - Cadastro de Funcionários",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Sistema de Gestão de Pessoas v2.0"
    }
)

# ============================================================
# ESTILOS CSS (COM IMAGEM DE FUNDO)
# ============================================================
# URL de uma imagem profissional de escritório (Unsplash)
background_image_url = "https://images.unsplash.com/photo-1497366216548-37526070297c?q=80&w=2069&auto=format&fit=crop"

st.markdown(f"""
<style>
    /* Fundo com Imagem e Overlay */
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), 
                    url("{background_image_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    .main {{ background: transparent; padding: 30px 20px !important; }}

    /* Título */
    h1 {{
        color: white !important;
        font-size: 2.8em !important;
        font-weight: 900 !important;
        text-align: center !important;
        text-shadow: 0 4px 15px rgba(0,0,0,0.4) !important;
        margin-bottom: 8px !important;
    }}
    .subtitle {{
        text-align: center;
        color: rgba(255,255,255,0.95);
        font-size: 1.1em;
        margin-bottom: 35px;
        font-weight: 400;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
    }}

    /* Card branco com leve transparência */
    .card {{
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 50px 45px;
        box-shadow: 0 25px 80px rgba(0,0,0,0.4);
        backdrop-filter: blur(5px);
    }}

    /* Abas Customizadas */
    .stTabs [role="tablist"] {{
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        border-radius: 14px;
        padding: 10px;
        gap: 12px;
    }}
    .stTabs [role="tab"] {{
        background: rgba(255,255,255,0.8) !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        color: #1e293b !important;
    }}
    .stTabs [role="tab"][aria-selected="true"] {{
        background: #4f46e5 !important;
        color: white !important;
    }}

    /* Inputs e Labels */
    label {{ color: #1e293b !important; font-weight: 700 !important; }}
    .stTextInput input, .stNumberInput input, .stDateInput input {{
        background: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
    }}

    /* Botão Principal */
    .stForm .stFormSubmitButton > button {{
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        color: white !important;
        font-weight: 800 !important;
        border: none !important;
        height: 3em;
    }}

    /* Rodapé */
    .footer {{
        text-align: center;
        color: white;
        font-size: 0.9em;
        margin-top: 50px;
        padding: 20px;
        background: rgba(0,0,0,0.3);
        border-radius: 10px;
    }}
</style>
""", unsafe_allow_html=True)

# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================
def formatar_cpf(cpf: str) -> str:
    digits = re.sub(r"\D", "", cpf)
    if len(digits) == 11:
        return f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}"
    return cpf

def validar_cpf(cpf: str) -> bool:
    digits = re.sub(r"\D", "", cpf)
    if len(digits) != 11 or len(set(digits)) == 1:
        return False
    for i in range(9, 11):
        soma = sum(int(digits[num]) * ((i + 1) - num) for num in range(i))
        valor = (soma * 10 % 11) % 10
        if valor != int(digits[i]):
            return False
    return True

# ============================================================
# CONEXÃO COM GOOGLE SHEETS
# ============================================================
@st.cache_resource
def get_connection():
    return st.connection("gsheets", type=GSheetsConnection)

try:
    conn = get_connection()
except Exception as e:
    st.error(f"❌ Erro ao conectar com Google Sheets: {e}")
    st.stop()

def ler_dados():
    try:
        df = conn.read(worksheet="Dados", ttl=30)
        if df is None or df.empty:
            return pd.DataFrame()
        return df.dropna(how="all").reset_index(drop=True)
    except Exception:
        return pd.DataFrame()

# ============================================================
# BARRA LATERAL
# ============================================================
with st.sidebar:
    st.markdown("### 📊 Gestão de Pessoas")
    st.info("Painel de Controle v2.0")
    df_sidebar = ler_dados()
    if not df_sidebar.empty:
        st.metric("👥 Total Colaboradores", len(df_sidebar))
    st.markdown("---")
    st.markdown("🔒 **Acesso Seguro**")

# ============================================================
# CABEÇALHO
# ============================================================
st.markdown("# 🏢 Sistema de Gestão de RH")
st.markdown('<div class="subtitle">Cadastro e consulta centralizada de colaboradores</div>', unsafe_allow_html=True)

tab_cadastro, tab_consulta = st.tabs(["➕ Novo Cadastro", "🔍 Consultar Base"])

# ──────────────────────────────────────────────────────────
# ABA 1 — CADASTRO
# ──────────────────────────────────────────────────────────
with tab_cadastro:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    with st.form("cadastro_form", border=False):
        sec1, sec2, sec3 = st.tabs(["👤 Pessoal", "💼 Profissional", "🏥 Saúde"])
        
        with sec1:
            c1, c2 = st.columns(2)
            nome = c1.text_input("Nome completo *")
            data_nascimento = c2.date_input("Data de Nascimento *", min_value=datetime.date(1940, 1, 1))
            
            c3, c4 = st.columns(2)
            cpf = c3.text_input("CPF *", help="Apenas números")
            sexo = c4.selectbox("Sexo *", ["Selecione...", "Masculino", "Feminino", "Outro"])

        with sec2:
            c1, c2 = st.columns(2)
            cargo = c1.text_input("Cargo *")
            departamento = c2.selectbox("Departamento *", ["Selecione...", "TI", "RH", "Vendas", "Financeiro", "Operações"])
            
            c3, c4 = st.columns(2)
            salario = c3.number_input("Salário (R$)", min_value=0.0)
            data_admissao = c4.date_input("Data de Admissão")

        with sec3:
            c1, c2 = st.columns(2)
            contato_emergencia = c1.text_input("Contato de Emergência *")
            telefone_emergencia = c2.text_input("Telefone Emergência *")
            tipo_sanguineo = st.selectbox("Tipo Sanguíneo *", ["Selecione...", "A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])

        st.markdown("---")
        submit = st.form_submit_button("✅ FINALIZAR CADASTRO", use_container_width=True)

    if submit:
        if "Selecione..." in [sexo, departamento, tipo_sanguineo] or not nome or not validar_cpf(cpf):
            st.error("⚠️ Verifique os campos obrigatórios e a validade do CPF.")
        else:
            novo_func = {
                "Nome": nome, "CPF": formatar_cpf(cpf), "Cargo": cargo,
                "Departamento": departamento, "Salario": salario,
                "Data_Cadastro": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            }
            try:
                df_atual = ler_dados()
                df_final = pd.concat([df_atual, pd.DataFrame([novo_func])], ignore_index=True)
                conn.update(worksheet="Dados", data=df_final)
                st.success(f"Funcionário {nome} cadastrado!")
                st.balloons()
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────
# ABA 2 — CONSULTA
# ──────────────────────────────────────────────────────────
with tab_consulta:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    df_busca = ler_dados()
    if not df_busca.empty:
        busca = st.text_input("Filtrar por nome...")
        if busca:
            df_busca = df_busca[df_busca["Nome"].str.contains(busca, case=False)]
        st.dataframe(df_busca, use_container_width=True)
    else:
        st.info("Nenhum dado encontrado.")
    st.markdown('</div>', unsafe_allow_html=True)

# Rodapé
st.markdown('<div class="footer">© 2026 HR Solutions Int. - Gestão de Ativos Humanos</div>', unsafe_allow_html=True)
