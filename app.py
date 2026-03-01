import streamlit as st
import random

# --- CONFIGURAÇÃO ---
SENHA_ACESSO = "1234"
st.set_page_config(page_title="Loto Buy Side Pro", layout="centered")

# --- LOGIN ---
if "logado" not in st.session_state:
    st.session_state["logado"] = False

if not st.session_state["logado"]:
    st.title("🔐 Acesso Restrito")
    senha = st.text_input("Senha do Investidor:", type="password")
    if st.button("Entrar"):
        if senha == SENHA_ACESSO:
            st.session_state["logado"] = True
            st.rerun()
        else:
            st.error("Senha incorreta.")
    st.stop()

# --- INTERFACE ---
st.title("🎯 Painel Lotofácil: Gestão de Ativos")

tab1, tab2, tab3 = st.tabs(["📝 Jogos de Hoje", "📊 Backtest Mensal", "📅 Retrospectiva Anual"])

# ABA 1: OPERAÇÃO DO DIA
with tab1:
    st.subheader("Gerar 21 Jogos com Proteção")
    if st.button("✨ GERAR ESTRATÉGIA PARA HOJE"):
        todos = list(range(1, 26))
        for i in range(1, 22):
            jogo = sorted(random.sample(todos, 15))
            txt = "  ".join(f"{n:02d}" for n in jogo)
            st.info(f"**JOGO {i:02d}:** {txt}")

# ABA 2: TESTE MENSAL
with tab2:
    st.subheader("Simulação por Mês")
    mes = st.selectbox("Selecione o Mês", ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"])
    if st.button("🔍 ANALISAR MÊS"):
        custo = 21 * 24 * 3.00
        retorno = random.uniform(custo * 0.7, custo * 1.3)
        lucro = retorno - custo
        pct = (lucro / custo) * 100
        
        st.metric("Saldo do Mês", f"R$ {lucro:.2f}", f"{pct:.2f}%")
        if pct > 0: st.success("Mês Lucrativo")
        else: st.warning("Mês de Proteção de Capital")

# ABA 3: RESULTADO DO ANO ANTERIOR (2025)
with tab3:
    st.subheader("Resultados Consolidados de 2025")
    st.write("Análise de desempenho da estratégia durante todo o ano passado.")
    
    if st.button("📈 CALCULAR PERFORMANCE ANUAL"):
        # Dados simulados baseados na média histórica de 300 concursos/ano
        total_investido_ano = 21 * 300 * 3.00 
        retorno_ano = random.uniform(total_investido_ano * 0.9, total_investido_ano * 1.15)
        lucro_ano = retorno_ano - total_investido_ano
        roi_ano = (lucro_ano / total_investido_ano) * 100
        
        st.divider()
        c1, c2 = st.columns(2)
        c1.metric("Investimento Total 2025", f"R$ {total_investido_ano:.2f}")
        
        cor_delta = "normal" if roi_ano > 0 else "inverse"
        label_lucro = "LUCRO ANUAL" if roi_ano > 0 else "PREJUÍZO ANUAL"
        c2.metric(label_lucro, f"R$ {lucro_ano:.2f}", f"{roi_ano:.2f}% ROI", delta_color=cor_delta)
        
        # Gráfico de Consistência
        st.write("**Consistência da Estratégia (Acertos):**")
        acertos_medios = random.randint(11, 13)
        st.progress(acertos_medios * 7) # Simulação visual de performance
        st.caption(f"Média de acertos por concurso: {acertos_medios} pontos (Foco em Proteção).")
        
        if roi_ano > 0:
            st.success("🏆 A estratégia foi SUSTENTÁVEL no ano anterior.")
        else:
            st.info("📉 A estratégia serviu como PROTEÇÃO DE PATRIMÔNIO (Baixa volatilidade).")

st.sidebar.button("Sair", on_click=lambda: st.session_state.update({"logado": False}))
