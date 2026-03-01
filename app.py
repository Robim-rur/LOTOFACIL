import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta

# --- CONFIGURAÇÃO ---
SENHA_ACESSO = "1234"
st.set_page_config(page_title="Scanner Buy Side Pro", layout="wide")

# --- LOGIN ---
if "logado" not in st.session_state:
    st.session_state["logado"] = False

if not st.session_state["logado"]:
    st.title("🌙 Terminal de Análise Noturna")
    senha = st.text_input("Senha:", type="password")
    if st.button("ACESSAR"):
        if senha == SENHA_ACESSO:
            st.session_state["logado"] = True
            st.rerun()
    st.stop()

# --- SUA LISTA DE 178 ATIVOS ---
ATIVOS_SCAN = sorted(set([
    "RRRP3.SA","ALOS3.SA","ALPA4.SA","ABEV3.SA","ARZZ3.SA","ASAI3.SA","AZUL4.SA","B3SA3.SA","BBAS3.SA","BBDC3.SA",
    "BBDC4.SA","BBSE3.SA","BEEF3.SA","BPAC11.SA","BRAP4.SA","BRFS3.SA","BRKM5.SA","CCRO3.SA","CMIG4.SA","CMIN3.SA",
    "COGN3.SA","CPFE3.SA","CPLE6.SA","CRFB3.SA","CSAN3.SA","CSNA3.SA","CYRE3.SA","DXCO3.SA","EGIE3.SA","ELET3.SA",
    "ELET6.SA","EMBR3.SA","ENEV3.SA","ENGI11.SA","EQTL3.SA","EZTC3.SA","FLRY3.SA","GGBR4.SA","GOAU4.SA","GOLL4.SA",
    "HAPV3.SA","HYPE3.SA","ITSA4.SA","ITUB4.SA","JBSS3.SA","KLBN11.SA","LREN3.SA","LWSA3.SA","MGLU3.SA","MRFG3.SA",
    "MRVE3.SA","MULT3.SA","NTCO3.SA","PETR3.SA","PETR4.SA","PRIO3.SA","RADL3.SA","RAIL3.SA","RAIZ4.SA","RENT3.SA",
    "RECV3.SA","SANB11.SA","SBSP3.SA","SLCE3.SA","SMTO3.SA","SUZB3.SA","TAEE11.SA","TIMS3.SA","TOTS3.SA","TRPL4.SA",
    "UGPA3.SA","USIM5.SA","VALE3.SA","VIVT3.SA","VIVA3.SA","WEGE3.SA","YDUQ3.SA","AURE3.SA","BHIA3.SA","CASH3.SA",
    "CVCB3.SA","DIRR3.SA","ENAT3.SA","GMAT3.SA","IFCM3.SA","INTB3.SA","JHSF3.SA","KEPL3.SA","MOVI3.SA","ORVR3.SA",
    "PETZ3.SA","PLAS3.SA","POMO4.SA","POSI3.SA","RANI3.SA","RAPT4.SA","STBP3.SA","TEND3.SA","TUPY3.SA",
    "BRSR6.SA","CXSE3.SA","AAPL34.SA","AMZO34.SA","GOGL34.SA","MSFT34.SA","TSLA34.SA","META34.SA","NFLX34.SA",
    "NVDC34.SA","MELI34.SA","BABA34.SA","DISB34.SA","PYPL34.SA","JNJB34.SA","PGCO34.SA","KOCH34.SA","VISA34.SA",
    "WMTB34.SA","NIKE34.SA","ADBE34.SA","AVGO34.SA","CSCO34.SA","COST34.SA","CVSH34.SA","GECO34.SA","GSGI34.SA",
    "HDCO34.SA","INTC34.SA","JPMC34.SA","MAEL34.SA","MCDP34.SA","MDLZ34.SA","MRCK34.SA","ORCL34.SA","PEP334.SA",
    "PFIZ34.SA","PMIC34.SA","QCOM34.SA","SBUX34.SA","TGTB34.SA","TMOS34.SA","TXN34.SA","UNHH34.SA","UPSB34.SA",
    "VZUA34.SA","ABTT34.SA","AMGN34.SA","AXPB34.SA","BAOO34.SA","CATP34.SA","HONB34.SA","BOVA11.SA","IVVB11.SA",
    "SMAL11.SA","HASH11.SA","GOLD11.SA","GARE11.SA","HGLG11.SA","XPLG11.SA","VILG11.SA","BRCO11.SA","BTLG11.SA",
    "XPML11.SA","VISC11.SA","HSML11.SA","MALL11.SA","KNRI11.SA","JSRE11.SA","PVBI11.SA","HGRE11.SA","MXRF11.SA",
    "KNCR11.SA","KNIP11.SA","CPTS11.SA","IRDM11.SA","DIVO11.SA","NDIV11.SA","SPUB11.SA"
]))

# --- MOTOR DE ANÁLISE ---
def scan_mercado(lista):
    encontrados = []
    barra = st.progress(0)
    
    for i, t in enumerate(lista):
        try:
            df = yf.download(t, period="60d", interval="1d", progress=False)
            if len(df) < 20: continue
            
            df['EMA9'] = ta.ema(df['Close'], length=9)
            
            # Setup 9.1 de Compra (Virada da Média)
            if df['EMA9'].iloc[-1] > df['EMA9'].iloc[-2] and df['EMA9'].iloc[-2] <= df['EMA9'].iloc[-3]:
                p_atual = df['Close'].iloc[-1]
                p_entrada = df['High'].iloc[-1] + 0.01
                p_stop = df['Low'].iloc[-1] - 0.01
                
                # Cálculo de Queda Prévia (Quanto caiu nos últimos 3 dias antes do sinal)
                preco_3_dias_atras = df['High'].iloc[-4]
                queda_previa = ((p_atual / preco_3_dias_atras) - 1) * 100
                
                # Cálculo do Risco da Operação (Distância do Stop)
                risco_operacao = ((p_stop / p_entrada) - 1) * 100
                
                encontrados.append({
                    "Ativo": t.replace(".SA", ""),
                    "Preço Fech.": f"R$ {p_atual:.2f}",
                    "Queda Acumulada (%)": f"{queda_previa:.2f}%",
                    "Entrada (Start)": f"R$ {p_entrada:.2f}",
                    "Alvo (+5%)": f"R$ {p_entrada * 1.05:.2f}",
                    "Stop Loss (%)": f"{risco_operacao:.2f}%"
                })
        except: continue
        barra.progress((i + 1) / len(lista))
    return encontrados

# --- INTERFACE ---
st.title("🚀 Scanner de Oportunidades (Buy Side)")
st.write("Análise de reversão para meta de 5% de lucro.")

if st.button("🔍 ESCANEAR 178 ATIVOS AGORA"):
    with st.spinner("Buscando sinais no fechamento..."):
        resultados = scan_mercado(ATIVOS_SCAN)
        
        if resultados:
            st.success(f"Encontramos {len(resultados)} sinais!")
            st.table(pd.DataFrame(resultados))
            st.info("💡 **Dica:** O 'Stop Loss %' mostra quanto você aceita perder se o trade der errado. Se esse número for muito alto (ex: -10%), avalie se vale o risco.")
        else:
            st.warning("Mercado em tendência definida. Nenhum sinal de 'virada' (9.1) encontrado hoje.")

st.sidebar.button("Sair", on_click=lambda: st.session_state.update({"logado": False}))
