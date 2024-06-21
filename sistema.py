from gerenciadorUsuario import GerenciadorUsuarios
from cliente import Cliente
from administrador import Administrador

class SistemaBliBank:
    def __init__(self) -> None:
        '''
        Inicializa o sistema BliBank, criando um gerenciador de usuários e configurando a sessão atual como None.
        '''
        self.gerenciador = GerenciadorUsuarios()
        self.sessao_atual = None

    def login(self, email: str, senha: str)-> None:
        '''
        Realiza o login de um usuário no sistema.

        Parâmetros
        ----------
        email : str
            Email do usuário.
        senha : str
            Senha do usuário.

        Retorna
        -------
        Cliente ou Administrador
            O usuário logado, ou None se o login falhar.
        '''
        usuario = self.gerenciador.login(email, senha)
        if usuario:
            self.sessao_atual = usuario
            return usuario
        return None

    def logout(self) -> str:
        '''
        Realiza o logout do usuário atual.

        Retorna
        -------
        str
            Mensagem de sucesso ou aviso se não houver usuário logado.
        '''
        if self.sessao_atual:
            nome_usuario = self.sessao_atual.get_nome()
            self.sessao_atual = None
            return f"Logout realizado com sucesso. Até logo, {nome_usuario}."
        return "Nenhum usuário logado atualmente."
    
    def realizar_operacao_financeira(self, tipo: str, valor: float, email_destinatario: str = None, descricao: str = None):
        '''
        Realiza operações financeiras como depósito, saque, transferência e investimento.

        Parâmetros
        ----------
        tipo : str
            Tipo de operação financeira ('1' para depósito, '2' para saque, '3' para transferência, '4' para investimento).
        valor : float
            Valor da operação.
        email_destinatario : str, opcional
            Email do destinatário da transferência (necessário para tipo '3').
        descricao : str, opcional
            Descrição do investimento (necessário para tipo '4').

        Retorna
        -------
        str
            Mensagem indicando o resultado da operação.
        '''
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
                        saldo_atual = round(self.sessao_atual.get_saldo(), 2)
                        return f"Transferência de R${round(valor, 2)} realizada com sucesso. Seu saldo atual é R${saldo_atual}."
                    else:
                        return "UsuarioNaoEncontrado"
                elif tipo == '4':
                    try:
                        rendimento_percentual, rendimento_valor, valor_final = operacao(valor)
                        saldo_atual = round(self.sessao_atual.get_saldo(), 2)
                        return f"Investimento de R${round(valor, 2)} realizado com sucesso com rendimento de {round(rendimento_percentual, 2)}%. Valor após rendimento: R${round(valor_final, 2)}. Seu saldo atual é R${saldo_atual}."
                    except ValueError as ve:
                        return str(ve)
                else:
                    operacao(valor)
                    saldo_atual = round(self.sessao_atual.get_saldo(), 2)
                    return f"{'Depósito' if tipo == '1' else 'Saque'} de R${round(valor, 2)} realizado com sucesso. Seu saldo atual é R${saldo_atual}."
            else:
                return "Operação inválida."
        else:
            return "Operação não permitida. Faça login como cliente."
