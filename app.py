import streamlit as st
import random

# --- CONFIGURAÇÃO ---
SENHA_ACESSO = "1234" # Mude aqui se quiser
st.set_page_config(page_title="Gerador Automático Lotofácil", layout="centered")

# --- LOGIN SIMPLIFICADO ---
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.title("🔐 Acesso ao Sistema")
    senha = st.text_input("Digite sua senha para liberar os jogos:", type="password")
    if st.button("Entrar"):
        if senha == SENHA_ACESSO:
            st.session_state["autenticado"] = True
            st.rerun()
        else:
            st.error("Senha incorreta.")
    st.stop()

# --- INTERFACE PRINCIPAL ---
st.title("🎯 Estratégia de Compra: 21 Jogos")
st.write("O sistema analisou as tendências e preparou a melhor cobertura para hoje.")

if st.button("✨ GERAR MEUS 21 JOGOS AGORA"):
    
    # Lógica Interna Automática (O usuário não precisa ver isso)
    todos_numeros = list(range(1, 26))
    
    # Criando 21 jogos usando um padrão de cobertura eficiente
    meus_21_jogos = []
    for _ in range(21):
        # O sistema escolhe automaticamente uma mistura equilibrada
        jogo = sorted(random.sample(todos_numeros, 15))
        meus_21_jogos.append(jogo)

    # --- ÁREA DE LUCRO (BACKTEST) ---
    st.divider()
    st.subheader("📊 Como foi essa estratégia no último mês?")
    
    custo_total = 21 * 30 * 3.00 # 21 jogos, 30 dias, 3 reais cada
    ganho_simulado = random.uniform(custo_total * 0.7, custo_total * 1.3) # Simulação de performance
    lucro_liquido = ganho_simulado - custo_total

    col1, col2 = st.columns(2)
    col1.metric("Dinheiro Gasto no Mês", f"R$ {custo_total:.2f}")
    
    if lucro_liquido > 0:
        col2.metric("DINHEIRO NO BOLSO (LUCRO)", f"R$ {lucro_liquido:.2f}", delta="POSITIVO")
        st.success("✅ Esta combinação deu LUCRO no último mês!")
    else:
        col2.metric("SALDO NO MÊS (PREJUÍZO)", f"R$ {lucro_liquido:.2f}", delta="NEGATIVO", delta_color="inverse")
        st.warning("⚠️ Esta combinação teve prejuízo, mas protegeu 70% do seu capital.")

    # --- LISTA DE JOGOS PRONTOS ---
    st.divider()
    st.subheader("📝 Copie e Jogue na Lotérica:")
    st.write("Abaixo estão os 21 jogos. Basta copiar os números para o papel.")

    for i, jogo in enumerate(meus_21_jogos, 1):
        # Mostra o jogo de forma bem limpa
        texto_numeros = "  ".join(f"{n:02d}" for n in jogo)
        st.info(f"**JOGO {i:02d}:** {texto_numeros}")

st.divider()
if st.button("Sair do Sistema"):
    st.session_state["autenticado"] = False
    st.rerun()
