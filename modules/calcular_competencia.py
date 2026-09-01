from datetime import datetime, timedelta

def calcular_competencia():
    '''
        Função para calcular a competência (último dia do mês anterior) a partir da data atual
    '''
    hoje = datetime.now()
    primeiro_dia_mes_atual = hoje.replace(day=1)
    ultimo_dia_mes_anterior = primeiro_dia_mes_atual - timedelta(days=1)
    competencia = ultimo_dia_mes_anterior.strftime("%d/%m/%Y")
    print(f"✓ Competência: {competencia}")
    return competencia

# def calcular_competencia():
#     data = datetime.strptime("30/05/2026", "%d/%m/%Y")
#     return data.strftime("%d/%m/%Y")
