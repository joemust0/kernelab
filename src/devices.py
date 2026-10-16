import pandas as pd

def get_matriz_acesso():
    data = [
        {"Processo": "P1 Monitoramento", "Disco": "-", "Rede": "R, W, U", "Áudio": "-", "Log": "W"},
        {"Processo": "P2 Telemetria", "Disco": "-", "Rede": "R, W, U", "Áudio": "-", "Log": "W"},
        {"Processo": "P3 Relatórios", "Disco": "R, W, U", "Rede": "-", "Áudio": "-", "Log": "R, W"},
        {"Processo": "P4 Alarme crítico", "Disco": "-", "Rede": "W, U, E", "Áudio": "W, U, E", "Log": "W"},
        {"Processo": "P5 Backup", "Disco": "R, W, U, E", "Rede": "-", "Áudio": "-", "Log": "W"},
        {"Processo": "P6 Atualização", "Disco": "R, W, X, U", "Rede": "R, W, U", "Áudio": "-", "Log": "W"},
    ]
    return pd.DataFrame(data)

def simular_concorrencia():
    return [
        "[0ms] P1 solicitou acesso à REDE -> Lock Concedido",
        "[2ms] P2 solicitou acesso à REDE -> Bloqueado (Aguardando Mutex de P1)",
        "[3ms] P4 solicitou acesso exclusivo à REDE -> Bloqueado na Fila (Prioridade Alta)",
        "[8ms] P1 liberou acesso à REDE",
        "[8ms] Sistema aplicou Herança de Prioridade -> Mutex concedido a P4",
        "[10ms] P4 liberou acesso à REDE -> Mutex concedido a P2",
        "[14ms] P2 liberou acesso à REDE"
    ]