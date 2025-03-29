from datetime import datetime

def formatar_data(data_str):
    try:
        return datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M")
    except:
        return data_str

def validar_campos_obrigatorios(dados, campos):
    return all(dados.get(campo) for campo in campos)