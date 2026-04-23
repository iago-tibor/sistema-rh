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
# ESTILOS CSS
# ============================================================
st.markdown("""
<style>
    /* Fundo gradiente */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    .main { background: transparent; padding: 30px 20px !important; }

    /* Título */
    h1 {
        color: white !important;
        font-size: 2.8em !important;
        font-weight: 900 !important;
        text-align: center !important;
        text-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
        letter-spacing: -1px !important;
        margin-bottom: 8px !important;
    }
    .subtitle {
        text-align: center;
        color: rgba(255,255,255,0.92);
        font-size: 1.1em;
        margin-bottom: 35px;
        font-weight: 400;
    }

    /* Card branco */
    .card {
        background: rgba(255,255,255,0.98);
        border-radius: 20px;
        padding: 50px 45px;
        box-shadow: 0 25px 80px rgba(0,0,0,0.25);
    }

    /* Abas */
    .stTabs [role="tablist"] {
        background: rgba(255,255,255,0.6);
        border-radius: 14px;
        padding: 14px;
        gap: 12px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    }
    .stTabs [role="tab"] {
        background: white !important;
        border: 2px solid rgba(102,126,234,0.2) !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        color: #475569 !important;
        font-weight: 700 !important;
        transition: all 0.3s ease !important;
    }
    .stTabs [role="tab"]:hover {
        border-color: #667eea !important;
        color: #667eea !important;
    }
    .stTabs [role="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border-color: #667eea !important;
        color: white !important;
        box-shadow: 0 8px 25px rgba(102,126,234,0.35) !important;
    }
    .stTabs [role="tabpanel"] { padding: 30px 0 !important; }

    /* Labels */
    label {
        color: #1a202c !important;
        font-weight: 700 !important;
        font-size: 0.95em !important;
        letter-spacing: 0.3px !important;
    }

    /* Inputs */
    .stTextInput input,
    .stNumberInput input,
    .stDateInput input {
        background: #f8fafc !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 10px !important;
        padding: 14px 16px !important;
        font-size: 1em !important;
        font-weight: 500 !important;
        color: #1a202c !important;
        transition: all 0.3s ease !important;
    }
    .stTextInput input:focus,
    .stNumberInput input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102,126,234,0.12) !important;
        background: white !important;
    }
    .stTextInput input::placeholder { color: #94a3b8 !important; }

    /* Selectbox */
    .stSelectbox [data-baseweb="select"] > div {
        background: #f8fafc !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 10px !important;
    }

    /* Botão submit */
    .stForm .stFormSubmitButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-weight: 800 !important;
        padding: 16px 40px !important;
        border: none !important;
        border-radius: 10px !important;
        font-size: 1.05em !important;
        width: 100% !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 10px 30px rgba(102,126,234,0.35) !important;
        transition: all 0.3s ease !important;
    }
    .stForm .stFormSubmitButton > button:hover {
        box-shadow: 0 16px 45px rgba(102,126,234,0.5) !important;
        transform: translateY(-2px) !important;
    }

    /* Subheader */
    h3 {
        color: #1a202c !important;
        font-weight: 800 !important;
        font-size: 1.25em !important;
        margin-bottom: 24px !important;
        padding-bottom: 12px !important;
        border-bottom: 3px solid #667eea !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%) !important;
    }
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown li {
        color: #334155 !important;
        font-size: 0.95em !important;
    }
    [data-testid="stSidebar"] h3 {
        color: #1e293b !important;
        border-bottom: 2px solid #667eea !important;
        font-size: 1.1em !important;
    }

    /* Métricas */
    [data-testid="metric-container"] {
        background: white !important;
        border-radius: 12px !important;
        padding: 16px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06) !important;
        border: 1px solid #e2e8f0 !important;
    }

    /* Mensagens */
    .stSuccess { border-radius: 10px !important; font-weight: 600 !important; }
    .stError   { border-radius: 10px !important; font-weight: 600 !important; }
    .stInfo    { border-radius: 10px !important; font-weight: 600 !important; }
    .stWarning { border-radius: 10px !important; font-weight: 600 !important; }

    /* Rodapé */
    .footer {
        text-align: center;
        color: rgba(255,255,255,0.85);
        font-size: 0.9em;
        margin-top: 50px;
        padding: 25px 0;
        border-top: 1px solid rgba(255,255,255,0.15);
    }

    /* Tabela de dados */
    .dataframe { border-radius: 10px !important; }

    @media (max-width: 768px) {
        h1 { font-size: 2em !important; }
        .card { padding: 25px 16px; border-radius: 16px; }
        .stTabs [role="tab"] { padding: 10px 14px !important; font-size: 0.85em !important; }
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================
def formatar_cpf(cpf: str) -> str:
    """Remove tudo que não for dígito e formata como XXX.XXX.XXX-XX"""
    digits = re.sub(r"\D", "", cpf)
    if len(digits) == 11:
        return f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}"
    return cpf

def validar_cpf(cpf: str) -> bool:
    digits = re.sub(r"\D", "", cpf)
    if len(digits) != 11 or len(set(digits)) == 1:
        return False
    # Primeiro dígito verificador
    soma = sum(int(d) * (10 - i) for i, d in enumerate(digits[:9]))
    r1 = (soma * 10 % 11) % 10
    if r1 != int(digits[9]):
        return False
    # Segundo dígito verificador
    soma = sum(int(d) * (11 - i) for i, d in enumerate(digits[:10]))
    r2 = (soma * 10 % 11) % 10
    return r2 == int(digits[10])


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


# ============================================================
# FUNÇÃO: LER DADOS
# ============================================================
def ler_dados():
    try:
        df = conn.read(worksheet="Dados", ttl=30)
        if df is None or df.empty:
            return pd.DataFrame()
        # Remove linhas totalmente vazias
        return df.dropna(how="all").reset_index(drop=True)
    except Exception:
        return pd.DataFrame()


# ============================================================
# BARRA LATERAL
# ============================================================
with st.sidebar:
    st.markdown("### 📊 Sistema de RH")
    st.markdown("**Versão 2.0**")
    st.markdown("---")

    st.markdown("### 🔧 Funcionalidades")
    st.markdown("""
- ✅ Cadastro de funcionários  
- ✅ Dados pessoais e corporativos  
- ✅ Contatos de emergência  
- ✅ Consulta e filtros  
- ✅ Exportação de dados  
""")
    st.markdown("---")

    st.markdown("### 📈 Estatísticas")
    df_sidebar = ler_dados()
    if not df_sidebar.empty:
        st.metric("👥 Funcionários", len(df_sidebar))
        if "Departamento" in df_sidebar.columns:
            st.metric("🏢 Departamentos", df_sidebar["Departamento"].nunique())
        if "Cargo" in df_sidebar.columns:
            st.metric("💼 Cargos distintos", df_sidebar["Cargo"].nunique())
    else:
        st.info("Nenhum funcionário cadastrado ainda.")

    st.markdown("---")
    st.caption("© 2024 Gestão de Pessoas")


# ============================================================
# CABEÇALHO
# ============================================================
col_h1, col_h2, col_h3 = st.columns([1, 3, 1])
with col_h2:
    st.markdown("# 🏢 Sistema de Cadastro de Funcionários")
    st.markdown('<div class="subtitle">Gerencie os dados dos seus colaboradores de forma segura e organizada</div>',
                unsafe_allow_html=True)

# ============================================================
# ABAS PRINCIPAIS (fora do form, para incluir Consulta)
# ============================================================
tab_cadastro, tab_consulta = st.tabs(["➕ Novo Cadastro", "🔍 Consultar Funcionários"])


# ──────────────────────────────────────────────────────────
# ABA 1 — CADASTRO
# ──────────────────────────────────────────────────────────
with tab_cadastro:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    with st.form("cadastro_form", border=False):
        secao1, secao2, secao3 = st.tabs(["👤 Dados Pessoais", "💼 Dados Corporativos", "🏥 Saúde e Emergência"])

        # ---------- DADOS PESSOAIS ----------
        with secao1:
            st.subheader("📋 Informações Pessoais")
            c1, c2 = st.columns(2)
            with c1:
                nome = st.text_input("Nome completo *", placeholder="Ex: João da Silva")
            with c2:
                data_nascimento = st.date_input(
                    "Data de Nascimento *",
                    format="DD/MM/YYYY",
                    min_value=datetime.date(1924, 1, 1),
                    max_value=datetime.date.today(),
                )

            c3, c4 = st.columns(2)
            with c3:
                cpf = st.text_input("CPF *", placeholder="000.000.000-00",
                                    help="Somente números ou no formato XXX.XXX.XXX-XX")
            with c4:
                sexo = st.selectbox("Sexo *",
                                    ["Selecione...", "Masculino", "Feminino", "Outro", "Prefiro não informar"])

            c5, c6 = st.columns(2)
            with c5:
                telefone = st.text_input("Telefone pessoal", placeholder="(XX) XXXXX-XXXX")
            with c6:
                email = st.text_input("E-mail", placeholder="joao@email.com")

        # ---------- DADOS CORPORATIVOS ----------
        with secao2:
            st.subheader("💼 Informações Profissionais")
            c1, c2 = st.columns(2)
            with c1:
                cargo = st.text_input("Cargo *", placeholder="Ex: Analista de TI")
            with c2:
                departamento = st.selectbox(
                    "Departamento *",
                    ["Selecione...", "TI", "RH", "Financeiro", "Operações",
                     "Vendas", "Marketing", "Jurídico", "Diretoria"]
                )

            c3, c4 = st.columns(2)
            with c3:
                escolaridade = st.selectbox(
                    "Escolaridade *",
                    ["Selecione...", "Ensino Fundamental", "Ensino Médio",
                     "Ensino Técnico", "Ensino Superior", "Pós-graduação", "Mestrado", "Doutorado"]
                )
            with c4:
                data_admissao = st.date_input(
                    "Data de Admissão",
                    format="DD/MM/YYYY",
                    min_value=datetime.date(2000, 1, 1),
                    max_value=datetime.date.today(),
                )

            c5, c6 = st.columns(2)
            with c5:
                salario = st.number_input("Salário Base (R$)", min_value=0.0, step=100.0, format="%.2f")
            with c6:
                regime = st.selectbox("Regime de Trabalho",
                                      ["Selecione...", "CLT", "PJ", "Estágio", "Temporário", "Freelancer"])

        # ---------- SAÚDE E EMERGÊNCIA ----------
        with secao3:
            st.subheader("🏥 Saúde e Emergência")
            c1, c2 = st.columns(2)
            with c1:
                contato_emergencia = st.text_input("Contato de Emergência *", placeholder="Nome completo")
            with c2:
                telefone_emergencia = st.text_input("Telefone de Emergência *", placeholder="(XX) XXXXX-XXXX")

            c3, c4 = st.columns(2)
            with c3:
                tipo_sanguineo = st.selectbox(
                    "Tipo Sanguíneo *",
                    ["Selecione...", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Não sei"]
                )
            with c4:
                plano_saude = st.selectbox("Plano de Saúde",
                                           ["Selecione...", "Sim – pela empresa", "Sim – particular", "Não possui"])

            alergias = st.text_area("Alergias / Observações médicas",
                                    placeholder="Deixe em branco se não houver", height=80)

        # ---------- BOTÃO ----------
        st.markdown("---")
        st.caption("*Campos obrigatórios")
        submit = st.form_submit_button("✅ Salvar Cadastro Completo", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Processar envio ──
    if submit:
        erros = []
        if not nome.strip():
            erros.append("Nome completo é obrigatório")
        if sexo == "Selecione...":
            erros.append("Sexo é obrigatório")
        if not cpf.strip():
            erros.append("CPF é obrigatório")
        elif not validar_cpf(cpf):
            erros.append("CPF inválido — verifique os dígitos informados")
        if departamento == "Selecione...":
            erros.append("Departamento é obrigatório")
        if not cargo.strip():
            erros.append("Cargo é obrigatório")
        if escolaridade == "Selecione...":
            erros.append("Escolaridade é obrigatória")
        if tipo_sanguineo == "Selecione...":
            erros.append("Tipo sanguíneo é obrigatório")
        if not contato_emergencia.strip():
            erros.append("Contato de emergência é obrigatório")
        if not telefone_emergencia.strip():
            erros.append("Telefone de emergência é obrigatório")

        if erros:
            st.error("⚠️ Corrija os seguintes erros antes de salvar:")
            for e in erros:
                st.error(f"• {e}")
        else:
            novo = {
                "Nome":                 nome.strip(),
                "Data_Nascimento":      data_nascimento.strftime("%d/%m/%Y"),
                "CPF":                  formatar_cpf(cpf),
                "Sexo":                 sexo,
                "Telefone":             telefone.strip(),
                "Email":                email.strip(),
                "Cargo":                cargo.strip(),
                "Departamento":         departamento,
                "Escolaridade":         escolaridade,
                "Data_Admissao":        data_admissao.strftime("%d/%m/%Y"),
                "Salario":              float(salario),
                "Regime":               regime if regime != "Selecione..." else "",
                "Contato_Emergencia":   contato_emergencia.strip(),
                "Telefone_Emergencia":  telefone_emergencia.strip(),
                "Tipo_Sanguineo":       tipo_sanguineo,
                "Plano_Saude":          plano_saude if plano_saude != "Selecione..." else "",
                "Alergias":             alergias.strip(),
                "Data_Cadastro":        datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
            }

            try:
                df_atual = ler_dados()
                df_novo_row = pd.DataFrame([novo])
                df_final = pd.concat([df_atual, df_novo_row], ignore_index=True)
                conn.update(worksheet="Dados", data=df_final)

                col_s1, col_s2, col_s3 = st.columns([1, 2, 1])
                with col_s2:
                    st.success(f"✅ **{nome}** cadastrado com sucesso!")
                    st.balloons()

                with st.expander("📋 Ver dados cadastrados"):
                    st.dataframe(df_novo_row, use_container_width=True)

            except Exception as ex:
                st.error(f"❌ Erro ao salvar na planilha: {ex}")
                st.error("Verifique se a aba 'Dados' existe e está acessível.")


# ──────────────────────────────────────────────────────────
# ABA 2 — CONSULTA
# ──────────────────────────────────────────────────────────
with tab_consulta:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🔍 Consultar Funcionários Cadastrados")

    df_todos = ler_dados()

    if df_todos.empty:
        st.info("Nenhum funcionário cadastrado ainda.")
    else:
        # Filtros
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            busca_nome = st.text_input("🔎 Buscar por nome", placeholder="Digite um nome...")
        with col_f2:
            opcoes_dept = ["Todos"] + (sorted(df_todos["Departamento"].dropna().unique().tolist())
                                       if "Departamento" in df_todos.columns else [])
            filtro_dept = st.selectbox("🏢 Departamento", opcoes_dept)
        with col_f3:
            opcoes_cargo = ["Todos"] + (sorted(df_todos["Cargo"].dropna().unique().tolist())
                                        if "Cargo" in df_todos.columns else [])
            filtro_cargo = st.selectbox("💼 Cargo", opcoes_cargo)

        df_filtrado = df_todos.copy()
        if busca_nome:
            df_filtrado = df_filtrado[
                df_filtrado["Nome"].str.contains(busca_nome, case=False, na=False)
            ]
        if filtro_dept != "Todos":
            df_filtrado = df_filtrado[df_filtrado["Departamento"] == filtro_dept]
        if filtro_cargo != "Todos":
            df_filtrado = df_filtrado[df_filtrado["Cargo"] == filtro_cargo]

        st.markdown(f"**{len(df_filtrado)} funcionário(s) encontrado(s)**")
        st.dataframe(df_filtrado, use_container_width=True, hide_index=True)

        # Exportar CSV
        csv_data = df_filtrado.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
        st.download_button(
            label="⬇️ Exportar CSV",
            data=csv_data,
            file_name=f"funcionarios_{datetime.date.today().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )

    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# RODAPÉ
# ============================================================
st.markdown("""
<div class="footer">
    © 2024 Sistema de Gestão de Pessoas &nbsp;|&nbsp; Versão 2.0 &nbsp;|&nbsp; Desenvolvido com ❤️ usando Streamlit
</div>
""", unsafe_allow_html=True)
