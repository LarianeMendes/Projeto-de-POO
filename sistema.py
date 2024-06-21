from gerenciadorusuario import GerenciadorUsuarios
from cliente import Cliente
from administrador import Administrador

class SistemaBliBank:
    def __init__(self) -> None:
        self.gerenciador = GerenciadorUsuarios()
        self.sessao_atual = None

    def login(self, email: str, senha: str):
        usuario = self.gerenciador.login(email, senha)
        if usuario:
            self.sessao_atual = usuario
            return usuario
        return None

    def logout(self) -> str:
        if self.sessao_atual:
            nome_usuario = self.sessao_atual.get_nome()
            self.sessao_atual = None
            return f"Logout realizado com sucesso. Até logo, {nome_usuario}."
        return "Nenhum usuário logado atualmente."
    
    def realizar_operacao_financeira(self, tipo: str, valor: float, email_destinatario: str = None, descricao: str = None):
        try:
            valor = float(valor)
        except ValueError:
            return "Valor inválido. Por favor, insira um número."

        if isinstance(self.sessao_atual, Cliente):
            operacoes = {
                '1': self.sessao_atual.gestao_conta.depositar,
                '2': self.sessao_atual.gestao_conta.sacar,
                '3': lambda v: self.sessao_atual.gestao_conta.transferir(v, email_destinatario),
                '4': lambda v: self.sessao_atual.investimentos.investir(v, descricao)
            }

            operacao = operacoes.get(tipo)
            if operacao:
                if tipo == '3':
                    destinatario = next((usuario for usuario in self.gerenciador.usuarios if usuario.get_email() == email_destinatario), None)
                    if destinatario:
                        if isinstance(destinatario, Administrador):
                            return "Não é possível realizar transferências para administradores."
                        operacao(valor)
                        saldo_atual = self.sessao_atual.get_saldo()
                        return f"Transferência de R${valor:.2f} realizada com sucesso. Seu saldo atual é R${saldo_atual:.2f}."
                    else:
                        return "UsuarioNaoEncontrado"
                elif tipo == '4':
                    try:
                        rendimento_percentual, rendimento_valor, valor_final = operacao(valor)
                        saldo_atual = self.sessao_atual.get_saldo()
                        return f"Investimento de R${valor:.2f} realizado com sucesso com rendimento de {rendimento_percentual:.2f}%. Valor após rendimento: R${valor_final:.2f}. Seu saldo atual é R${saldo_atual:.2f}."
                    except ValueError as ve:
                        return str(ve)
                else:
                    operacao(valor)
                    saldo_atual = self.sessao_atual.get_saldo()
                    return f"{'Depósito' if tipo == '1' else 'Saque'} de R${valor:.2f} realizado com sucesso. Seu saldo atual é R${saldo_atual:.2f}."
            else:
                return "Operação inválida."
        else:
            return "Operação não permitida. Faça login como cliente."
