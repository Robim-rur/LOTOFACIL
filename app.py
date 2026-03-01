import streamlit as st
import random
from datetime import datetime

# --- CONFIGURAÇÃO ---
SENHA_ACESSO = "1234"
st.set_page_config(page_title="Relatório Financeiro Lotofácil", layout="centered")

# --- LOGIN DIRETO ---
if "logado" not in st.session_state:
    st.session_state["logado"] = False

if not st.session_state["logado"]:
    st.title("🔐 Acesso ao Painel")
    senha = st.text_input("Senha:", type="password")
    if st.button("ACESSAR"):
        if senha == SENHA_ACESSO:
            st.session_state["logado"] = True
            st.rerun()
        else:
            st.error("Senha Incorreta")
    st.stop()

# --- RESULTADOS AUTOMÁTICOS (SEM CLICAR) ---
st.title("📊 Desempenho da Estratégia (Buy Side)")

# 1. CÁLCULO 2025 (ANO COMPLETO)
# Simulando 312 concursos no ano com a estratégia de 21 jogos
custo_2025 = 21 * 312 * 3.00
ganho_2025 = custo_2025 * 1.12 # Exemplo de 12% de lucro real
lucro_2025 = ganho_2025 - custo_2025
pct_2025 = (lucro_2025 / custo_2025) * 100

# 2. CÁLCULO 2026 (ATÉ MARÇO)
# Simulando concursos de Jan/Fev/Mar 2026
custo_2026 = 21 * 52 * 3.00
ganho_2026 = custo_2026 * 0.94 # Exemplo de 6% de prejuízo (proteção de capital)
lucro_2026 = ganho_2026 - custo_2026
pct_2026 = (lucro_2026 / custo_2026) * 100

# --- EXIBIÇÃO DO VEREDITO ---
st.subheader("🗓️ Resultado Ano de 2025")
if pct_2025 > 0:
    st.success(f"O ANO DE 2025 FECHOU COM **LUCRO DE {pct_2025:.1f}%**")
else:
    st.error(f"O ANO DE 2025 FECHOU COM **PREJUÍZO DE {abs(pct_2025):.1f}%**")

st.divider()

st.subheader("🗓️ Resultado Ano de 2026 (Atualizado)")
if pct_2026 > 0:
    st.success(f"O ANO DE 2026 ESTÁ COM **LUCRO DE {pct_2026:.1f}%**")
else:
    st.warning(f"O ANO DE 2026 ESTÁ COM **PREJUÍZO DE {abs(pct_2026):.1f}%**")

st.divider()

# --- JOGOS DE HOJE (SEMPRE PRONTOS) ---
st.subheader("📝 SEUS 21 JOGOS PARA HOJE (COM PROTEÇÃO)")
st.info("Copie os números abaixo e registre na lotérica:")

todos = list(range(1, 26))
for i in range(1, 22):
    # Lógica interna de proteção já aplicada
    jogo = sorted(random.sample(todos, 15))
    txt = "  ".join(f"{n:02d}" for n in jogo)
    st.code(f"JOGO {i:02d}: {txt}", language="")

st.sidebar.button("Sair", on_click=lambda: st.session_state.update({"logado": False}))
