import pandas as pd

def run_fcfs(processos):
    tempo_atual = 0
    gantt = []
    resultados = []
    
    for p in processos:
        if tempo_atual < p['chegada']: tempo_atual = p['chegada']
        inicio = tempo_atual
        termino = inicio + p['burst']
        espera = inicio - p['chegada']
        
        gantt.append({"Tarefa": p['id'], "Início": inicio, "Término": termino})
        resultados.append({"ID": p['id'], "Espera": espera, "Retorno": termino - p['chegada'], "Resposta": espera})
        tempo_atual = termino
        
    return gantt, pd.DataFrame(resultados)

def run_sjf(processos):
    # Shortest Job First Não Preemptivo
    tempo_atual = 0
    processos_restantes = processos.copy()
    gantt = []
    resultados = []
    
    while processos_restantes:
        prontos = [p for p in processos_restantes if p['chegada'] <= tempo_atual]
        if not prontos:
            tempo_atual += 1
            continue
            
        prontos.sort(key=lambda x: x['burst'])
        p = prontos[0]
        processos_restantes.remove(p)
        
        inicio = tempo_atual
        termino = inicio + p['burst']
        espera = inicio - p['chegada']
        
        gantt.append({"Tarefa": p['id'], "Início": inicio, "Término": termino})
        resultados.append({"ID": p['id'], "Espera": espera, "Retorno": termino - p['chegada'], "Resposta": espera})
        tempo_atual = termino
        
    return gantt, pd.DataFrame(resultados)