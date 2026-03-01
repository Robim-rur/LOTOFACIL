import streamlit as st
import random
import pandas as pd

# --- CONFIGURAÇÃO DA SENHA DIÁRIA ---
# Você pode mudar essa senha aqui no código sempre que quiser
SENHA_CORRETA = "1234" 

st.set_page_config(page_title="Lotofácil Fácil", layout="wide")

# --- LOGIN ---
st.sidebar.title("🔐 Acesso Restrito")
senha_digitada = st.sidebar.text_input("Digite a senha do dia:", type="password")

if senha_digitada != SENHA_CORRETA:
    st.error("Por favor, digite a senha correta na lateral para acessar o sistema.")
    st.stop()

# --- DADOS FINANCEIROS (PREÇOS REAIS) ---
PRECO_JOGO = 3.00
PREMIOS = {11: 6, 12: 12, 13: 30, 14: 1500, 15: 1500000}

# --- TÍTULO ---
st.title("🍀 Gerador de Jogos: Lucro & Proteção")
st.write("Este sistema cria 21 jogos focados em recuperar seu dinheiro e buscar o prêmio.")

# --- ENTRADA DE DADOS SIMPLIFICADA ---
st.divider()
st.subheader("1️⃣ Escolha os números")
col_a, col_b, col_c = st.columns(3)

with col_a:
    quentes = st.multiselect("Números Fortes (que saíram muito):", range(1, 26), default=[1,2,3,4,5,6,7,8,9,10])
with col_b:
    atrasados = st.multiselect("Números de Proteção (que sumiram):", range(1, 26), default=[11,12,13,14,15,16])
with col_c:
    neutros = st.multiselect("Números de Equilíbrio:", range(1, 26), default=[17,18,19,20,21,22,23,24,25])

if st.button("📊 GERAR MEUS 21 JOGOS E VER RESULTADO"):
    
    # Gerar os 21 jogos
    meus_jogos = []
    for _ in range(21):
        # 9 fortes + 4 proteção + 2 equilíbrio = 15 números
        jogo = random.sample(quentes, 9) + random.sample(atrasados, 4) + random.sample(neutros, 2)
        meus_jogos.append(sorted(jogo))

    # --- SIMULAÇÃO DE BACKTEST (O QUE TERIA ACONTECIDO NO ÚLTIMO MÊS) ---
    st.divider()
    st.subheader("2️⃣ Teste de Lucro (Últimos 30 dias)")
    
    investimento_total = 21 * 30 * PRECO_JOGO # 21 jogos x 30 dias
    retorno_total = 0
    
    # Simula 30 sorteios para ver como a estratégia se comporta
    for _ in range(30):
        sorteio_simulado = random.sample(range(1, 26), 15)
        for j in meus_jogos:
            acertos = len(set(j) & set(sorteio_simulado))
            if acertos in PREMIOS:
                retorno_total += PREMIOS[acertos]

    saldo_final = retorno_total - investimento_total
    
    # Painel Visual de Resultados
    res1, res2, res3 = st.columns(3)
    res1.metric("Dinheiro Investido", f"R$ {investimento_total:.2f}")
    res2.metric("Dinheiro de Prêmios", f"R$ {retorno_total:.2f}")
    
    if saldo_final > 0:
        res3.metric("LUCRO NO BOLSO", f"R$ {saldo_final:.2f}", delta="POSITIVO")
    else:
        res3.metric("PREJUÍZO ACUMULADO", f"R$ {saldo_final:.2f}", delta="NEGATIVO", delta_color="inverse")

    # --- LISTA DE JOGOS PRONTOS ---
    st.divider()
    st.subheader("3️⃣ Seus Jogos para Copiar e Jogar:")
    st.info("Copie os números abaixo e passe para o volante da Lotofácil.")
    
    for i, jogo in enumerate(meus_jogos, 1):
        texto_jogo = " - ".join(f"{n:02d}" for n in jogo)
        st.code(f"JOGO {i:02d}:    {texto_jogo}", language="")

st.sidebar.markdown("---")
st.sidebar.caption("Para mudar a senha, você deve editar a linha 7 do código no GitHub.")
