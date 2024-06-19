import re

def validar_cpf(cpf):
    # Remove caracteres especiais
    cpf = re.sub(r'\D', '', cpf)

    # Verifica se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return False

    # Verifica se todos os dígitos são iguais (CPFs inválidos conhecidos)
    if cpf == cpf[0] * 11:
        return False

    # Validação do CPF
    for i in range(9, 11):
        soma = sum(int(cpf[num]) * (i + 1 - num) for num in range(0, i))
        digito = (soma * 10 % 11) % 10
        if digito != int(cpf[i]):
            return False
    return True
