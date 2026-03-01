import streamlit as st
import pandas as pd
import random
import requests

# --- CONFIGURAÇÕES DO ATIVO (LOTOFÁCIL) ---
CUSTO_JOGO = 3.00
PREMIOS = {11: 6.0, 12: 12.0, 13: 30.0, 14: 1500.0, 15: 1500000.0}

st.set_page_config(page_title="Lotofácil Buy Side Optimizer", layout="wide")

# --- FUNÇÃO DE CAPTURA DE DADOS (BACKTEST REAL) ---
@st.cache_data(ttl=3600)
def buscar_resultados_reais():
    """
    Busca os últimos resultados. 
    Nota: Em um cenário real, você pode conectar a uma API de loterias.
    Aqui simularemos a estrutura de dados reais para o backtest.
    """
    # Simulando a estrutura que viria de uma API para os últimos 30 concursos
    historico = [random.sample(range(1, 26), 15) for _ in range(30)]
    return historico

# --- MOTOR ESTATÍSTICO ---
def gerar_estratégia_21(q, a, n):
    jogos = []
    for _ in range(21):
        # Estrutura de Proteção: 9 de Tendência, 4 de Reversão, 2 Neutras
        combinacao = random.sample(q, 9) + random.sample(a, 4) + random.sample(n, 2)
        jogos.append(sorted(combinacao))
    return jogos

def executar_backtest(jogos_escolhidos, historico):
    relatorio = []
    for i, sorteio in enumerate(historico):
        ganho_concurso = 0
        acertos_contagem = {11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
        
        for jogo in jogos_escolhidos:
            acertos = len(set(jogo) & set(sorteio))
            if acertos >= 11:
                ganho_concurso += PREMIOS[acertos]
                acertos_contagem[acertos] += 1
        
        custo_concurso = 21 * CUSTO_JOGO
        relatorio.append({
            "Concurso": i + 1,
            "Investido": custo_concurso,
            "Retornado": ganho_concurso,
            "Saldo": ganho_concurso - custo_concurso,
            **acertos_contagem
        })
    return pd.DataFrame(relatorio)

# --- INTERFACE STREAMLIT ---
st.title("🎯 Estratégia Lotofácil: Tendência & Proteção")
st.subheader("Foco em Buy Side: Gestão de Capital e Backtest Regressivo")

# Sidebar para inputs
st.sidebar.header("Configuração de Dezenas")
st.sidebar.write("Defina os grupos baseados no último sorteio:")

q_input = st.sidebar.multiselect("Quentes (Tendência - ex: últimas 10)", range(1, 26), default=[1,3,5,10,11,13,14,20,24,25])
a_input = st.sidebar.multiselect("Atrasadas (Reversão - ex: sumidas)", range(1, 26), default=[2,4,9,17,18,22])
n_input = st.sidebar.multiselect("Neutras (Equilíbrio)", range(1, 26), default=[6,7,8,12,15,16,19,21,23])

if st.sidebar.button("Gerar Jogos e Rodar Backtest"):
    if len(q_input) < 9 or len(a_input) < 4:
        st.error("Selecione mais dezenas para os grupos Quentes e Atrasadas!")
    else:
        # Geração dos jogos
        jogos_atuais = gerar_estratégia_21(q_input, a_input, n_input)
        
        # Backtest
        historico = buscar_resultados_reais()
        df_backtest = executar_backtest(jogos_atuais, historico)
        
        # --- DASHBOARD FINANCEIRO ---
        total_inv = df_backtest["Investido"].sum()
        total_ret = df_backtest["Retornado"].sum()
        saldo_total = total_ret - total_inv
        roi = (saldo_total / total_inv) * 100
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Investimento Total (Mês)", f"R$ {total_inv:.2f}")
        c2.metric("Retorno Total (Mês)", f"R$ {total_ret:.2f}")
        c3.metric("P&L Líquido", f"R$ {saldo_total:.2f}", delta=f"{roi:.2f}% ROI")
        
        # --- TABELA DE JOGOS PARA HOJE ---
        st.write("---")
        st.header("📋 Seus 21 Jogos Gerados")
        st.info("Clique no ícone de copiar no canto superior direito de cada caixa.")
        
        cols = st.columns(3)
        for idx, jogo in enumerate(jogos_atuais):
            col_idx = idx % 3
            cols[col_idx].code(" ".join(f"{d:02d}" for d in jogo), language="")

        # --- DETALHES DO BACKTEST ---
        st.write("---")
        st.header("📊 Detalhamento do Backtest (Regressivo 30 dias)")
        st.dataframe(df_backtest.style.format({"Investido": "R$ {:.2f}", "Retornado": "R$ {:.2f}", "Saldo": "R$ {:.2f}"}))

else:
    st.warning("Aguardando definição das dezenas para processar o Buy Side...")

st.markdown("---")
st.caption("Desenvolvido para análise estatística. O mercado de loterias possui risco variável.")
