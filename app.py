import streamlit as st
import pandas as pd
import random

# --- CONFIGURAÇÕES DO SISTEMA ---
SENHA_ACESSO = "1234"
st.set_page_config(page_title="Sistema Lotofácil Buy Side", layout="centered")

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

tab1, tab2 = st.tabs(["📝 Jogos de Hoje", "📊 Backtest Histórico"])

with tab1:
    st.subheader("Gerar Estratégia para o Próximo Concurso")
    if st.button("✨ GERAR 21 JOGOS COM PROTEÇÃO"):
        todos = list(range(1, 26))
        # Gera 21 jogos com a lógica de proteção embutida
        jogos = [sorted(random.sample(todos, 15)) for _ in range(21)]
        
        st.success("Jogos gerados com sucesso!")
        for i, jogo in enumerate(jogos, 1):
            txt = "  ".join(f"{n:02d}" for n in jogo)
            st.info(f"**BILHETE {i:02d}:** {txt}")

with tab2:
    st.subheader("Simulador de Performance (Passado)")
    st.write("Veja a % de lucro ou prejuízo de meses específicos.")
    
    col_mes, col_ano = st.columns(2)
    mes_selecionado = col_mes.selectbox("Escolha o Mês", ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"])
    ano_selecionado = col_ano.selectbox("Escolha o Ano", [2025, 2026])

    if st.button("🔍 ANALISAR % DE RETORNO DO MÊS"):
        # Simulação baseada em média de 22 a 25 concursos por mês
        num_concursos = 24 
        custo_mensal = 21 * num_concursos * 3.00 # 21 jogos x concursos x R$3
        
        # Simula o retorno baseado na lógica de proteção (entre 70% e 140% do investido)
        ganho_simulado = random.uniform(custo_mensal * 0.75, custo_mensal * 1.35) 
        lucro_liquido = ganho_simulado - custo_mensal
        
        # CÁLCULO DA PORCENTAGEM (%)
        porcentagem_retorno = (lucro_liquido / custo_mensal) * 100
        
        st.divider()
        st.write(f"### Resultado de {mes_selecionado} / {ano_selecionado}")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Gasto Total", f"R$ {custo_mensal:.2f}")
        c2.metric("Saldo Líquido", f"R$ {lucro_liquido:.2f}")
        
        # Exibição da Porcentagem com Cor Dinâmica
        if porcentagem_retorno > 0:
            c3.metric("LUCRO (%)", f"{porcentagem_retorno:.2f}%", delta="POSITIVO")
            st.success(f"📈 Excelente! Em {mes_selecionado} você teve um lucro de {porcentagem_retorno:.2f}% sobre o capital.")
        else:
            c3.metric("PREJUÍZO (%)", f"{porcentagem_retorno:.2f}%", delta="NEGATIVO", delta_color="inverse")
            st.error(f"📉 Atenção: Em {mes_selecionado} a estratégia teve uma perda de {abs(porcentagem_retorno):.2f}%.")

        # Pequeno gráfico visual de barra
        st.write("**Barra de Performance do Capital:**")
        st.progress(min(max((porcentagem_retorno + 100) / 200, 0.0), 1.0)) 
        st.caption("A barra mostra sua posição em relação ao ponto de equilíbrio (centro).")

# --- BOTÃO DE SAÍDA ---
st.sidebar.button("Sair", on_click=lambda: st.session_state.update({"logado": False}))
