import sys
import os
import json


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from schedulers import run_fcfs
from memory import run_lru

def executar_testes():
    resultados_log = []
    
    # Carregar banco de dados
    with open('data/processes.json', 'r', encoding='utf-8') as f:
        processos = json.load(f)
        
    # TESTE 1: Validação do FCFS
    # O relatório exige que a espera média do FCFS seja exatamente 13,67 u.t.
    _, df_fcfs = run_fcfs(processos)
    espera_fcfs = round(df_fcfs['Espera'].mean(), 2)
    if espera_fcfs == 13.67:
        resultados_log.append("✅ [SUCESSO] Algoritmo FCFS validado. Espera Média == 13.67 u.t.")
    else:
        resultados_log.append(f"❌ [FALHA] Algoritmo FCFS. Esperado: 13.67, Recebido: {espera_fcfs}")

    # TESTE 2: Validação da Memória LRU
    # O relatório exige que o LRU com 4 frames gere 10 page faults
    sequencia = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5, 2, 1, 5, 3, 2]
    _, faults_lru, _ = run_lru(sequencia, 4)
    if faults_lru == 10:
        resultados_log.append("✅ [SUCESSO] Algoritmo LRU validado. Faltas de Página == 10")
    else:
        resultados_log.append(f"❌ [FALHA] Algoritmo LRU. Esperado: 10, Recebido: {faults_lru}")
        
    return resultados_log