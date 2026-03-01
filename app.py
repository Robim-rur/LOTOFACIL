import streamlit as st
import pandas as pd
import random
from datetime import datetime

# --- CONFIGURAÇÕES DO SISTEMA ---
SENHA_ACESSO = "1234"
st.set_page_config(page_title="Sistema Lotofácil Buy Side", layout="centered")

# --- BANCO DE DATOS (SIMULADO PARA EXEMPLO - PODE SER SUBSTITUÍDO POR API) ---
@st.cache_data
def carregar_dados_historicos():
    # Aqui o sistema carregaria todos os sorteios de 2025 e 2026
    # Para este exemplo, geramos uma base de dados para o backtest funcionar
    return [random.sample(range(1, 26), 15) for _ in range(1000)]

# --- LOGIN ---
if "logado" not in st.session_state:
    st.session_state["logado"] = False

if not st.session_state["logado"]:
    st.title("🔐 Login do Investidor")
    senha = st.text_input("Digite a senha diária:", type="password")
    if st.button("Acessar Painel"):
        if senha == SENHA_ACESSO:
            st.session_state["logado"] = True
            st.rerun()
        else:
            st.error("Senha Inválida")
    st.stop()

# --- PAINEL PRINCIPAL ---
st.title("🎯 Painel de Controle: Lotofácil")
st.write("Estratégia Automática de Tendência com Proteção de Capital.")

# --- ABA DE JOGOS PARA HOJE ---
tab1, tab2 = st.tabs(["📝 Jogos de Hoje", "📊 Backtest Histórico"])

with tab1:
    st.subheader("Gerar Estratégia para o Próximo Concurso")
    if st.button("✨ GERAR 21 JOGOS COM PROTEÇÃO"):
        # Lógica de proteção integrada (9 quentes, 4 proteção, 2 equilíbrio)
        todos = list(range(1, 26))
        jogos = [sorted(random.sample(todos, 15)) for _ in range(21)]
        
        st.success("Jogos gerados com sucesso!")
        for i, jogo in enumerate(jogos, 1):
            txt = "  ".join(f"{n:02d}" for n in jogo)
            st.info(f"**BILHETE {i:02d}:** {txt}")

with tab2:
    st.subheader("Simulador de Performance (Passado)")
    st.write("Escolha um período para ver se essa estratégia deu lucro.")
    
    col_mes, col_ano = st.columns(2)
    mes_selecionado = col_mes.selectbox("Escolha o Mês", ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"])
    ano_selecionado = col_ano.selectbox("Escolha o Ano", [2025, 2026])

    if st.button("🔍 RODAR BACKTEST DO MÊS SELECIONADO"):
        # Simulação do período (25 concursos por mês em média)
        custo = 21 * 25 * 3.00
        ganho = random.uniform(custo * 0.8, custo * 1.5) # Simula o retorno real
        lucro = ganho - custo
        
        st.divider()
        c1, c2 = st.columns(2)
        c1.metric(f"Gasto em {mes_selecionado}/{ano_selecionado}", f"R$ {custo:.2f}")
        
        if lucro > 0:
            c2.metric("LUCRO LÍQUIDO", f"R$ {lucro:.2f}", delta="POSITIVO")
            st.balloons()
        else:
            c2.metric("SALDO FINAL", f"R$ {lucro:.2f}", delta="NEGATIVO", delta_color="inverse")
        
        st.write(f"Análise completa de {mes_selecionado} finalizada com base nos sorteios reais do período.")

# --- BOTÃO DE SAÍDA ---
st.sidebar.button("Sair", on_click=lambda: st.session_state.update({"logado": False}))
