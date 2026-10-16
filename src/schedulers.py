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

def run_prioridade(processos):
    tempo_atual = 0
    processos_restantes = processos.copy()
    gantt = []
    resultados = []
    
    while processos_restantes:
        prontos = [p for p in processos_restantes if p['chegada'] <= tempo_atual]
        if not prontos:
            tempo_atual += 1
            continue
            
        # Ordena por prioridade (menor número = maior) e depois por ordem de chegada
        prontos.sort(key=lambda x: (x['prioridade'], x['chegada']))
        p = prontos[0]
        processos_restantes.remove(p)
        
        inicio = tempo_atual
        termino = inicio + p['burst']
        espera = inicio - p['chegada']
        
        gantt.append({"Tarefa": p['id'], "Início": inicio, "Término": termino})
        resultados.append({"ID": p['id'], "Espera": espera, "Retorno": termino - p['chegada'], "Resposta": espera})
        tempo_atual = termino
        
    return gantt, pd.DataFrame(resultados)

def run_rr(processos, quantum=3):
    tempo_atual = 0
    fila = []
    processos_restantes = sorted(processos, key=lambda x: x['chegada'])
    tempos_restantes = {p['id']: p['burst'] for p in processos}
    chegadas = {p['id']: p['chegada'] for p in processos}
    primeira_exec = {}
    terminos = {}
    gantt = []

    while processos_restantes and processos_restantes[0]['chegada'] <= tempo_atual:
        fila.append(processos_restantes.pop(0))

    while fila or processos_restantes:
        if not fila:
            tempo_atual = processos_restantes[0]['chegada']
            while processos_restantes and processos_restantes[0]['chegada'] <= tempo_atual:
                fila.append(processos_restantes.pop(0))

        p = fila.pop(0)
        pid = p['id']
        
        if pid not in primeira_exec:
            primeira_exec[pid] = tempo_atual

        execucao = min(quantum, tempos_restantes[pid])
        inicio = tempo_atual
        termino = tempo_atual + execucao

        gantt.append({"Tarefa": pid, "Início": inicio, "Término": termino})
        tempo_atual = termino
        tempos_restantes[pid] -= execucao

        while processos_restantes and processos_restantes[0]['chegada'] <= tempo_atual:
            fila.append(processos_restantes.pop(0))

        if tempos_restantes[pid] > 0:
            fila.append(p)
        else:
            terminos[pid] = tempo_atual

    resultados = []
    for p in processos:
        pid = p['id']
        ret = terminos[pid] - chegadas[pid]
        esp = ret - p['burst']
        resp = primeira_exec[pid] - chegadas[pid]
        resultados.append({"ID": pid, "Espera": esp, "Retorno": ret, "Resposta": resp})

    return gantt, pd.DataFrame(resultados)