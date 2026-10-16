import streamlit as st
import pandas as pd
import json
import plotly.express as px
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tests')))
from test_algo import executar_testes
from schedulers import run_fcfs, run_sjf, run_prioridade, run_rr
from memory import run_fifo, run_lru, run_optimal
from devices import get_matriz_acesso, simular_concorrencia

st.set_page_config(page_title="KernelLab", layout="wide")
st.title("🔬 KernelLab - MedControl Systems")

@st.cache_data
def load_data():
    with open('data/processes.json', 'r', encoding='utf-8') as f:
        return json.load(f)

processos = load_data()

st.sidebar.header("Painel de Controle")

# Corrigido o erro de digitação e quebra de linha que havia aqui
etapa = st.sidebar.radio("Selecione a Etapa", ["1. Escalonamento CPU", "2. Memória Virtual", "3. Dispositivos e E/S", "4. Testes Automatizados"])

if etapa == "1. Escalonamento CPU":
    st.subheader("Processos (Prontos)")
    st.dataframe(pd.DataFrame(processos), use_container_width=True)
    
    # Corrigida a indentação que estava quebrando o código
    algoritmo = st.selectbox("Algoritmo", ["FCFS", "SJF (Shortest Job First)", "Prioridade", "Round Robin (q=3)"])
    if st.button("Executar Simulação"):
        if algoritmo == "FCFS": 
            gantt_data, df_resultados = run_fcfs(processos)
        elif algoritmo == "SJF (Shortest Job First)": 
            gantt_data, df_resultados = run_sjf(processos)
        elif algoritmo == "Prioridade": 
            gantt_data, df_resultados = run_prioridade(processos)
        else: 
            gantt_data, df_resultados = run_rr(processos, quantum=3)
            
        c1, c2, c3 = st.columns(3)
        c1.success(f"Espera Média: {df_resultados['Espera'].mean():.2f} u.t.")
        c2.info(f"Retorno Médio: {df_resultados['Retorno'].mean():.2f} u.t.")
        c3.warning(f"Resposta Média: {df_resultados['Resposta'].mean():.2f} u.t.")
        
        st.write("### Diagrama de Gantt")
        df_g = pd.DataFrame(gantt_data)
        df_g['Início'] = pd.to_datetime(df_g['Início'], unit='ms')
        df_g['Término'] = pd.to_datetime(df_g['Término'], unit='ms')
        fig = px.timeline(df_g, x_start="Início", x_end="Término", y="Tarefa", color="Tarefa")
        fig.update_yaxes(autorange="reversed")
        fig.layout.xaxis.type = 'linear'
        for d in fig.data:
            d.x = df_g['Término'].dt.microsecond / 1000 - df_g['Início'].dt.microsecond / 1000
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df_resultados, use_container_width=True)

elif etapa == "2. Memória Virtual":
    st.subheader("Substituição de Páginas")
    frames = st.slider("Quantidade de Frames Físicos", 3, 5, 4)
    sequencia = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5, 2, 1, 5, 3, 2]
    st.write(f"**Sequência de Referências:** {sequencia}")
    
    # Adicionada a terceira coluna para exibir o algoritmo Optimal exigido no edital
    col1, col2, col3 = st.columns(3)
    
    hits_fifo, faults_fifo, taxa_fifo = run_fifo(sequencia, frames)
    col1.metric("FIFO - Faltas", faults_fifo, f"Taxa: {taxa_fifo:.1f}%", delta_color="inverse")
    
    hits_lru, faults_lru, taxa_lru = run_lru(sequencia, frames)
    col2.metric("LRU - Faltas", faults_lru, f"Taxa: {taxa_lru:.1f}%", delta_color="inverse")

    hits_opt, faults_opt, taxa_opt = run_optimal(sequencia, frames)
    col3.metric("Optimal - Faltas", faults_opt, f"Taxa: {taxa_opt:.1f}%", delta_color="inverse")

elif etapa == "3. Dispositivos e E/S":
    st.subheader("Matriz de Controle de Acesso")
    st.dataframe(get_matriz_acesso(), use_container_width=True)
    
    st.subheader("Simulação de Concorrência (Mutex em Rede)")
    for log in simular_concorrencia():
        st.code(log, language="bash")

elif etapa == "4. Testes Automatizados":
    st.subheader("Bateria de Testes (TDD)")
    st.write("Esta rotina valida se os algoritmos estão retornando os valores exatos documentados no Relatório Técnico.")
    
    if st.button("Executar Bateria de Testes"):
        with st.spinner('Rodando validações...'):
            logs = executar_testes()
            for log in logs:
                if "✅" in log:
                    st.success(log)
                else:
                    st.error(log)