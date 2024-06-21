import flet as ft
import re, os
from sistema import SistemaBliBank
from cliente import Cliente
from administrador import Administrador

class TelaInicial:
    def __init__(self, app):
        '''
        Inicializa a tela inicial do aplicativo.

        Parâmetros
        ----------
        app : BliBankApp
            Instância do aplicativo principal.
        '''
        self.app = app

    def mostrar(self, e=None):
        '''
        Exibe a tela inicial do aplicativo.
        '''
        self.app.pagina.controls.clear()

        def ao_clicar_login(e):
            '''
            Exibe a tela de login.
            '''
            self.app.tela_login.mostrar()

        def ao_clicar_cadastrar(e):
            '''
            Exibe a tela de cadastro.
            '''
            self.app.tela_cadastro.mostrar()

        def ao_clicar_sair(e):
            '''
            Fecha a janela do aplicativo.
            '''
            self.app.pagina.window_close()

        self.app.pagina.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Bem-vindo ao BliBank!", size=32, color=ft.colors.PINK, weight=ft.FontWeight.BOLD),
                        ft.ElevatedButton("Login", on_click=ao_clicar_login),
                        ft.ElevatedButton("Cadastrar", on_click=ao_clicar_cadastrar),
                        ft.ElevatedButton("Sair", on_click=ao_clicar_sair),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        )
        self.app.pagina.update()


class TelaLogin:
    def __init__(self, app):
        '''
        Inicializa a tela de login do aplicativo.

        Parâmetros
        ----------
        app : BliBankApp
            Instância do aplicativo principal.
        '''
        self.app = app

    def mostrar(self, e=None):
        '''
        Exibe a tela de login do aplicativo.
        '''
        self.app.pagina.controls.clear()

        email = ft.TextField(label="Email", autofocus=True, width=300)
        senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, width=300)

        def ao_clicar_entrar(e):
            '''
            Realiza o login do usuário.
            '''
            usuario = self.app.sistema.login(email.value, senha.value)
            if usuario:
                if isinstance(usuario, Cliente) and usuario.solicitar_encerramento:
                    self.app.mostrar_snackbar("Conta desativada. Ela será encerrada em breve.")
                    return
                
                if isinstance(usuario, Cliente):
                    self.app.menu_cliente.mostrar()
                elif isinstance(usuario, Administrador):
                    self.app.menu_admin.mostrar()
            else:
                self.app.mostrar_snackbar("Login falhou. Verifique suas credenciais.")

        self.app.pagina.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Login", size=24, color=ft.colors.PINK, weight=ft.FontWeight.BOLD),
                        email,
                        senha,
                        ft.ElevatedButton("Entrar", on_click=ao_clicar_entrar),
                        ft.ElevatedButton("Voltar", on_click=self.app.tela_inicial.mostrar),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        )
        self.app.pagina.update()


class TelaCadastro:
    def __init__(self, app):
        '''
        Inicializa a tela de cadastro do aplicativo.

        Parâmetros
        ----------
        app : BliBankApp
            Instância do aplicativo principal.
        '''
        self.app = app
        self.nome = ft.TextField(label="Nome", autofocus=True, width=300, on_change=self.validar_nome)
        self.sobrenome = ft.TextField(label="Sobrenome", width=300, on_change=self.validar_sobrenome)
        self.email = ft.TextField(label="Email", width=300, on_change=self.validar_email)
        self.cpf = ft.TextField(label="CPF", width=300, keyboard_type=ft.KeyboardType.NUMBER, on_change=self.formatar_cpf)
        self.senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, width=300, on_change=self.validar_senha)
        self.confirmacao_senha = ft.TextField(label="Confirmação de Senha", password=True, can_reveal_password=True, width=300, on_change=self.validar_confirmacao_senha)
        self.tipo_usuario = ft.Dropdown(
            label="Tipo de Usuário",
            options=[ft.dropdown.Option("Cliente"), ft.dropdown.Option("Administrador")],
            width=300,
            on_change=self.ao_mudar_tipo_usuario
        )
        self.token = ft.TextField(label="Token de Administrador", password=True, can_reveal_password=True, visible=False, width=300)
        self.registrar_button = ft.ElevatedButton("Registrar", on_click=self.ao_clicar_registrar)
        self.voltar_button = ft.ElevatedButton("Voltar", on_click=self.voltar)

    def mostrar(self):
        '''
        Exibe a tela de cadastro.
        '''
        self.app.pagina.controls.clear()
        self.app.pagina.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Cadastrar", size=24, color=ft.colors.PINK, weight=ft.FontWeight.BOLD),
                        self.nome,
                        self.sobrenome,
                        self.email,
                        self.cpf,
                        self.senha,
                        self.confirmacao_senha,
                        self.tipo_usuario,
                        self.token,
                        ft.Row([self.registrar_button, self.voltar_button], alignment=ft.MainAxisAlignment.CENTER),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        )
        self.app.pagina.update()

    def ao_mudar_tipo_usuario(self, e):
        '''
        Ajusta a visibilidade do campo de token de administrador com base no tipo de usuário selecionado.
        '''
        self.token.visible = self.tipo_usuario.value == "Administrador"
        self.app.pagina.update()

    def mostrar_snackbar(self, mensagem):
        '''
        Exibe uma mensagem temporária na parte inferior da tela.

        Parâmetros
        ----------
        mensagem : str
            Mensagem a ser exibida.
        '''
        self.app.pagina.snack_bar = ft.SnackBar(
            ft.Text(mensagem),
            duration=1000  
        )
        self.app.pagina.snack_bar.open = True
        self.app.pagina.update()

    def limpar_campos(self):
        '''
        Limpa todos os campos do formulário de cadastro.
        '''
        self.nome.value = ""
        self.sobrenome.value = ""
        self.email.value = ""
        self.cpf.value = ""
        self.senha.value = ""
        self.confirmacao_senha.value = ""
        self.tipo_usuario.value = None
        self.token.visible = False
        self.token.value = ""
        self.app.pagina.update()

    def validar_nome(self, e):
        '''
        Testes de validação o campo de nome.
        '''
        if self.nome.value:
            self.nome.value = self.nome.value.title()
            self.nome.update()
            if not re.match(r'^[A-Za-zÀ-ÿ]+$', self.nome.value.replace(" ", "")):
                self.mostrar_snackbar("Nome inválido. Use apenas letras sem espaços.")
        else:
            self.app.pagina.snack_bar.open = False
            self.app.pagina.update()

    def validar_sobrenome(self, e):
        '''
        Testes de validação o campo de sobrenome.
        '''
        if self.sobrenome.value:
            self.sobrenome.value = self.sobrenome.value.title()
            self.sobrenome.update()
            if not re.match(r'^[A-Za-zÀ-ÿ]+$', self.sobrenome.value.replace(" ", "")):
                self.mostrar_snackbar("Sobrenome inválido. Use apenas letras sem espaços.")
        else:
            self.app.pagina.snack_bar.open = False
            self.app.pagina.update()

    def validar_email(self, e):
        '''
        Testes de validação do campo de email.
        '''
        if self.email.value:
            self.email.value = self.email.value.strip().replace(" ", "").lower() 
            self.email.update()
            if not re.match(r'^[^@]+@[^@]+\.[^@]+$', self.email.value):
                self.mostrar_snackbar("Email inválido.")
            elif self.app.sistema.gerenciador.verificar_email_existente(self.email.value):
                self.mostrar_snackbar("Email já cadastrado.")
            else:
                self.app.pagina.snack_bar.open = False
                self.app.pagina.update()

    def formatar_cpf(self, e):
        '''
        Formatação e teste de validação o campo de CPF.
        '''
        cpf = re.sub(r'\D', '', self.cpf.value)
        
        if len(cpf) > 11:
            cpf = cpf[:11]
        
        if len(cpf) == 11:
            cpf = f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'

        self.cpf.value = cpf
        self.cpf.update()

        if len(cpf) == 14:
            if self.app.sistema.gerenciador.verificar_cpf_existente(cpf):
                self.mostrar_snackbar("CPF já cadastrado.")
            else:
                self.app.pagina.snack_bar.open = False
                self.app.pagina.update()
        else:
            self.mostrar_snackbar("CPF deve ter exatamente 11 dígitos NUMÉRICOS.")
        
    def validar_senha(self, e):
        '''
        Testes de validação do campo de senha.
        '''
        if self.senha.value and len(self.senha.value) < 8:
            self.mostrar_snackbar("A senha deve ter pelo menos 8 caracteres.")
        else:
            self.app.pagina.snack_bar.open = False
            self.app.pagina.update()

    def validar_confirmacao_senha(self, e):
        '''
        Testes de validação do campo de confirmação de senha.
        '''
        if self.confirmacao_senha.value and self.senha.value != self.confirmacao_senha.value:
            self.mostrar_snackbar("As senhas não coincidem.")
        else:
            self.app.pagina.snack_bar.open = False
            self.app.pagina.update()

    def ao_clicar_registrar(self, e):
        '''
        Realiza as validações finais e registra o usuário.
        '''
        if not all([self.nome.value, self.sobrenome.value, self.email.value, self.cpf.value, self.senha.value, self.confirmacao_senha.value]):
            self.mostrar_snackbar("Todos os campos são obrigatórios.")
            return

        if not re.match(r'^[A-Za-zÀ-ÿ]+$', self.nome.value.replace(" ", "")):
            self.mostrar_snackbar("Nome inválido. Use apenas letras sem espaços.")
            return

        if not re.match(r'^[A-Za-zÀ-ÿ]+$', self.sobrenome.value.replace(" ", "")):
            self.mostrar_snackbar("Sobrenome inválido. Use apenas letras sem espaços.")
            return

        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', self.email.value):
            self.mostrar_snackbar("Email inválido.")
            return

        if self.app.sistema.gerenciador.verificar_email_existente(self.email.value):
            self.mostrar_snackbar("Email já cadastrado.")
            return

        num_cpf = self.cpf.value
        if not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', num_cpf):
            self.mostrar_snackbar("CPF inválido.")
            return

        if self.app.sistema.gerenciador.verificar_cpf_existente(re.sub(r'\D', '', num_cpf)):
            self.mostrar_snackbar("CPF já cadastrado.")
            return

        if len(self.senha.value) < 8:
            self.mostrar_snackbar("A senha deve ter pelo menos 8 caracteres.")
            return

        if self.senha.value != self.confirmacao_senha.value:
            self.mostrar_snackbar("As senhas não coincidem.")
            return

        if self.tipo_usuario.value == "Administrador" and self.token.value != "adm123":
            self.mostrar_snackbar("Token de administrador inválido.")
            return

        self.app.sistema.gerenciador.cadastrar_usuario(
            nome=self.nome.value,
            sobrenome=self.sobrenome.value,
            email=self.email.value,
            senha=self.senha.value,
            cpf=num_cpf,
            tipo=self.tipo_usuario.value
        )

        self.mostrar_snackbar("Cadastro realizado com sucesso.")
        self.limpar_campos()
        self.app.tela_inicial.mostrar()

    def voltar(self, e):
        '''
        Retorna à tela inicial.
        '''
        self.limpar_campos()
        self.app.tela_inicial.mostrar()


class MenuCliente:
    def __init__(self, app):
        '''
        Inicializa o menu do cliente.

        Parâmetros
        ----------
        app : BliBankApp
            Instância do aplicativo principal.
        '''
        self.app = app

    def mostrar(self, e=None):
        '''
        Exibe o menu principal do cliente.
        '''
        self.app.pagina.controls.clear()

        if isinstance(self.app.sistema.sessao_atual, Cliente):
            saldo_formatado = f"{self.app.sistema.sessao_atual.get_saldo():,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            self.app.saldo_texto = ft.Text(
                f"Saldo: R${saldo_formatado}",
                size=18,
                color=ft.colors.WHITE,
                weight=ft.FontWeight.BOLD
            )
            self.app.pagina.add(
                ft.Container(
                    content=self.app.saldo_texto,
                    alignment=ft.alignment.top_right,
                    padding=10,
                )
            )

        def ao_clicar_operacao(e):
            '''
            Exibe o menu de operações financeiras.
            '''
            self.app.menu_operacoes.mostrar()

        def ao_clicar_cartao(e):
            '''
            Exibe o menu de gerenciamento de cartão de crédito.
            '''
            self.app.menu_cartao.mostrar()

        def ao_clicar_encerrar_conta(e):
            '''
            Verifica se a conta pode ser encerrada e exibe a confirmação de encerramento.
            '''
            saldo = self.app.sistema.sessao_atual.get_saldo()
            divida_cartao = self.app.sistema.sessao_atual.divida_cartao

            if abs(saldo) > 1e-2 or abs(divida_cartao) > 1e-2:
                mensagens = []
                if abs(saldo) > 1e-2:
                    saldo_formatado = f"{saldo:.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                    mensagens.append(f"Saldo na conta: R${saldo_formatado}")
                if abs(divida_cartao) > 1e-2:
                    divida_formatada = f"{divida_cartao:.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                    mensagens.append(f"Dívida no cartão de crédito: R${divida_formatada}")

                self.app.pagina.controls.clear()
                self.app.pagina.add(
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("Encerramento de Conta", size=24, color=ft.colors.PINK, weight=ft.FontWeight.BOLD),
                                ft.Text("Para encerrar a conta, o saldo deve ser zero e não pode haver pendências no cartão de crédito.", size=18, color=ft.colors.WHITE),
                                ft.Text("Não é possível encerrar a conta devido aos seguintes motivos:", size=16, color=ft.colors.RED),
                                *[
                                    ft.Text(mensagem, size=16, color=ft.colors.WHITE)
                                    for mensagem in mensagens
                                ],
                                ft.ElevatedButton("Voltar", on_click=self.mostrar),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20,
                        ),
                        alignment=ft.alignment.center,
                        expand=True,
                    )
                )
                self.app.pagina.update()
            else:
                self.mostrar_confirmacao_encerramento()

        def ao_clicar_logout(e):
            '''
            Realiza logout e retorna à tela inicial.
            '''
            mensagem_logout = self.app.sistema.logout()
            self.app.mostrar_snackbar(mensagem_logout)
            self.app.tela_inicial.mostrar()

        menu_items = [
            ft.Text("Menu Cliente", size=24, color=ft.colors.PINK, weight=ft.FontWeight.BOLD),
            ft.ElevatedButton("Realizar Operação", on_click=ao_clicar_operacao),
            ft.ElevatedButton("Cartão de Crédito", on_click=ao_clicar_cartao),
            ft.ElevatedButton("Encerrar Conta", on_click=ao_clicar_encerrar_conta),
            ft.ElevatedButton("Logout", on_click=ao_clicar_logout),
        ]

        self.app.pagina.add(
            ft.Container(
                content=ft.Column(
                    menu_items,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        )
        self.app.pagina.update()

    def mostrar_confirmacao_encerramento(self):
        '''
        Exibe a confirmação de encerramento da conta.
        '''
        self.app.pagina.controls.clear()
        self.app.pagina.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Tem certeza de que deseja solicitar o encerramento da sua conta? Esta ação não pode ser desfeita.", size=18, color=ft.colors.WHITE),
                        ft.ElevatedButton("Confirmar", on_click=self.confirmar_encerramento_conta),
                        ft.ElevatedButton("Cancelar", on_click=self.mostrar),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        )
        self.app.pagina.update()

    def confirmar_encerramento_conta(self, e):
        '''
        Confirma e solicita o encerramento da conta.
        '''
        self.app.sistema.sessao_atual.gestao_conta.solicitar_encerramento_conta()
        self.app.mostrar_snackbar("Sua solicitação de encerramento de conta foi recebida e será processada em breve. Sentiremos sua falta!")
        self.app.tela_inicial.mostrar()


class MenuOperacoes:
    def __init__(self, app):
        '''
        Inicializa o menu de operações financeiras.

        Parâmetros
        ----------
        app : BliBankApp
            Instância do aplicativo principal.
        '''
        self.app = app

    def mostrar(self, e=None):
        '''
        Exibe o menu de operações financeiras.
        '''
        self.app.pagina.controls.clear()
        self.app.pagina.add(
            ft.Container(
                content=self.app.saldo_texto,
                alignment=ft.alignment.top_right,
                padding=10,
            )
        )

        def ao_clicar_deposito(e):
            '''
            Exibe a tela de depósito.
            '''
            self.app.tela_valor.mostrar("Depósito", '1')

        def ao_clicar_saque(e):
            '''
            Exibe a tela de saque.
            '''
            self.app.tela_valor.mostrar("Saque", '2')

        def ao_clicar_transferencia(e):
            '''
            Exibe a tela de transferência.
            '''
            self.app.tela_transferencia.mostrar()

        def ao_clicar_investir(e):
            '''
            Exibe a tela de investimentos.
            '''
            self.app.tela_investimento.mostrar()

        self.app.pagina.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Operações Financeiras", size=24, color=ft.colors.PINK, weight=ft.FontWeight.BOLD),
                        ft.ElevatedButton("Depósito", on_click=ao_clicar_deposito),
                        ft.ElevatedButton("Saque", on_click=ao_clicar_saque),
                        ft.ElevatedButton("Transferência", on_click=ao_clicar_transferencia),
                        ft.ElevatedButton("Investir", on_click=ao_clicar_investir),
                        ft.ElevatedButton("Voltar", on_click=self.app.menu_cliente.mostrar),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        )
        self.app.atualizar_saldo()
        self.app.pagina.update()


class TelaValor:
    def __init__(self, app):
        '''
        Inicializa a tela para inserção de valores de operações financeiras.

        Parâmetros
        ----------
        app : BliBankApp
            Instância do aplicativo principal.
        '''
        self.app = app

    def mostrar(self, operacao, tipo_operacao, e=None):
        '''
        Exibe a tela para a operação financeira especificada.

        Parâmetros
        ----------
        operacao : str
            Nome da operação (ex.: 'Depósito', 'Saque').
        tipo_operacao : str
            Código do tipo de operação ('1' para depósito, '2' para saque, etc.).
        '''
        self.app.pagina.controls.clear()
        self.app.pagina.add(
            ft.Container(
                content=self.app.saldo_texto,
                alignment=ft.alignment.top_right,
                padding=10,
            )
        )

        valor = ft.TextField(label="Valor", autofocus=True, width=300, prefix_text="R$", value="0,00")

        def formatar_valor(e):
            '''
            Formata o valor inserido pelo usuário para o formato monetário.
            '''
            input_value = valor.value
            input_value = ''.join(filter(str.isdigit, input_value))  
            
            if not input_value:
                input_value = "0"
            
            while len(input_value) < 3:
                input_value = "0" + input_value

            formatted_value = f"{int(input_value[:-2]):,}.{input_value[-2:]}" 
            formatted_value = formatted_value.replace(",", "X").replace(".", ",").replace("X", ".")
            valor.value = formatted_value
            self.app.pagina.update()

        def ao_clicar_confirmar(e):
            '''
            Realiza a operação financeira ao clicar no botão confirmar.
            '''
            try:
                valor_formatado = valor.value.replace(".", "").replace(",", ".")
                valor_float = float(valor_formatado)
                
                if valor_float == 0:
                    self.app.mostrar_snackbar("Valor inválido.")
                    return
                
                # Atualiza o saldo antes de realizar a operação
                self.app.atualizar_saldo()
                
                if tipo_operacao == '2' and valor_float > self.app.sistema.sessao_atual.get_saldo():
                    self.app.mostrar_snackbar("Saldo insuficiente.")
                    return

                resultado = self.app.sistema.realizar_operacao_financeira(tipo_operacao, valor_float)
                self.app.atualizar_saldo()  # Atualiza o saldo após a operação
                
                saldo_atualizado = f"{self.app.sistema.sessao_atual.get_saldo():,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                valor_final_formatado = f"{valor_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ",")

                mensagem = f"{operacao} de R${valor_final_formatado} realizado com sucesso.\nSaldo atualizado: R${saldo_atualizado}"
                self.app.mostrar_resultado_operacao(mensagem)
            except ValueError:
                self.app.mostrar_snackbar("Por favor, insira um valor válido.")

        valor.on_change = formatar_valor

        self.app.pagina.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(f"{operacao}", size=24, color=ft.colors.PINK, weight=ft.FontWeight.BOLD),
                        valor,
                        ft.ElevatedButton("Confirmar", on_click=ao_clicar_confirmar),
                        ft.ElevatedButton("Voltar", on_click=self.app.menu_operacoes.mostrar),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        )
        self.app.atualizar_saldo()  # Atualiza o saldo quando a tela é exibida
        self.app.pagina.update()


class TelaTransferencia:
    def __init__(self, app):
        '''
        Inicializa a tela de transferência.

        Parâmetros
        ----------
        app : BliBankApp
            Instância do aplicativo principal.
        '''
        self.app = app

    def mostrar(self, e=None):
        '''
        Exibe a tela de transferência.
        '''
        self.app.pagina.controls.clear()
        self.app.pagina.add(
            ft.Container(
                content=self.app.saldo_texto,
                alignment=ft.alignment.top_right,
                padding=10,
            )
        )

        valor = ft.TextField(label="Valor", autofocus=True, width=300, prefix_text="R$", value="0,00")
        email_destinatario = ft.TextField(label="Email do Destinatário", width=300)

        def formatar_valor(e):
            '''
            Formata o valor inserido pelo usuário para o formato monetário.
            '''
            input_value = valor.value
            input_value = ''.join(filter(str.isdigit, input_value)) 

            if not input_value:
                input_value = "0"

            while len(input_value) < 3:
                input_value = "0" + input_value

            formatted_value = f"{int(input_value[:-2]):,}.{input_value[-2:]}" 
            formatted_value = formatted_value.replace(",", "X").replace(".", ",").replace("X", ".")
            valor.value = formatted_value
            self.app.pagina.update()

        def ao_clicar_confirmar(e):
            '''
            Realiza a transferência ao clicar no botão confirmar.
            '''
            try:
                valor_formatado = valor.value.replace(".", "").replace(",", ".")
                valor_float = float(valor_formatado)

                if valor_float == 0:
                    self.app.mostrar_snackbar("O valor da transferência não pode ser R$0,00.")
                    return

                if not email_destinatario.value:
                    self.app.mostrar_snackbar("O campo de e-mail do destinatário não pode estar vazio.")
                    return

                if not re.match(r"[^@]+@[^@]+\.[^@]+", email_destinatario.value):
                    self.app.mostrar_snackbar("Por favor, insira um e-mail válido.")
                    email_destinatario.value = ""
                    self.app.pagina.update()
                    return

                if email_destinatario.value == self.app.sistema.sessao_atual.get_email():
                    self.app.mostrar_snackbar("Você não pode transferir para o próprio e-mail.")
                    email_destinatario.value = ""
                    self.app.pagina.update()
                    return

                if valor_float > self.app.sistema.sessao_atual.get_saldo():
                    self.app.mostrar_snackbar("Saldo insuficiente.")
                    return

                resultado = self.app.sistema.realizar_operacao_financeira('3', valor_float, email_destinatario=email_destinatario.value)
                if resultado == "UsuarioNaoEncontrado":
                    self.app.mostrar_snackbar(f"Usuário com email {email_destinatario.value} não encontrado.")
                    email_destinatario.value = ""
                    self.app.pagina.update()
                    return

                self.app.atualizar_saldo()
                if isinstance(resultado, str):
                    self.app.mostrar_resultado_operacao(resultado)
                else:
                    saldo_atualizado = f"{self.app.sistema.sessao_atual.get_saldo():,.2f}".replace(",", "X").replace(".", ",").replace("X", ",")
                    valor_final_formatado = f"{valor_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ",")

                    mensagem = f"Transferência de R${valor_final_formatado} para {email_destinatario.value} realizada com sucesso.\nSaldo atualizado: R${saldo_atualizado}"
                    self.app.mostrar_resultado_operacao(mensagem)
            except ValueError:
                self.app.mostrar_snackbar("Por favor, insira um valor válido.")

        valor.on_change = formatar_valor

        self.app.pagina.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Transferência", size=24, color=ft.colors.PINK, weight=ft.FontWeight.BOLD),
                        valor,
                        email_destinatario,
                        ft.ElevatedButton("Confirmar", on_click=ao_clicar_confirmar),
                        ft.ElevatedButton("Voltar", on_click=self.app.menu_operacoes.mostrar),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        )
        self.app.atualizar_saldo()
        self.app.pagina.update()


class TelaInvestimento:
    def __init__(self, app):
        '''
        Inicializa a tela de investimento.

        Parâmetros
        ----------
        app : BliBankApp
            Instância do aplicativo principal.
        '''
        self.app = app

    def mostrar(self, e=None):
        '''
        Exibe a tela de investimento.
        '''
        self.app.pagina.controls.clear()
        self.app.pagina.add(
            ft.Container(
                content=self.app.saldo_texto,
                alignment=ft.alignment.top_right,
                padding=10,
            )
        )

        valor = ft.TextField(label="Valor", autofocus=True, width=300, prefix_text="R$", value="0,00")
        tipo_investimento = ft.Dropdown(
            label="Tipo de Investimento",
            options=[
                ft.dropdown.Option("Ações"),
                ft.dropdown.Option("FIIs"),
                ft.dropdown.Option("ETFs"),
                ft.dropdown.Option("Cripto"),
                ft.dropdown.Option("Renda Fixa"),
            ],
            width=300
        )

        confirmar_button = ft.ElevatedButton("Confirmar", disabled=True)

        def formatar_valor(e):
            '''
            Formata o valor inserido pelo usuário para o formato monetário.
            '''
            input_value = valor.value
            input_value = ''.join(filter(str.isdigit, input_value)) 
            
            if not input_value:
                input_value = "0"
            
            while len(input_value) < 3:
                input_value = "0" + input_value

            formatted_value = f"{int(input_value[:-2]):,}.{input_value[-2:]}"  
            formatted_value = formatted_value.replace(",", "X").replace(".", ",").replace("X", ".")
            valor.value = formatted_value
            self.app.pagina.update()

        def ao_selecionar_tipo(e):
            '''
            Habilita o botão confirmar quando um tipo de investimento é selecionado.
            '''
            confirmar_button.disabled = not tipo_investimento.value
            self.app.pagina.update()

        def ao_clicar_confirmar(e):
            '''
            Realiza o investimento ao clicar no botão confirmar.
            '''
            try:
                valor_formatado = valor.value.replace(".", "").replace(",", ".")
                valor_float = round(float(valor_formatado), 2)
                
                if valor_float == 0:
                    self.app.mostrar_snackbar("O valor do investimento não pode ser R$0,00.")
                    return
                
                if valor_float > self.app.sistema.sessao_atual.get_saldo():
                    self.app.mostrar_snackbar("Saldo insuficiente.")
                    return

                if not tipo_investimento.value:
                    self.app.mostrar_snackbar("Tipo de investimento inválido.")
                    return

                descricao_investimento = tipo_investimento.value.lower() 
                resultado = self.app.sistema.realizar_operacao_financeira('4', valor_float, descricao=descricao_investimento)
                self.app.atualizar_saldo()
                if isinstance(resultado, str):
                    self.app.resultado_operacao.mostrar(resultado)
                else:
                    rendimento_percentual, rendimento_valor, valor_final = resultado
                    mensagem = (
                        f"Investimento em {tipo_investimento.value} realizado com sucesso.\n"
                        f"Investimento de R${valor_float:.2f}.\n"
                        f"Rendimento de {rendimento_percentual:.2f}%, o que te retornou R${rendimento_valor:.2f}.\n"
                        f"Seu saldo atual é R${self.app.sistema.sessao_atual.get_saldo():.2f}"
                    )
                    self.app.resultado_operacao.mostrar(mensagem)
            except ValueError:
                self.app.mostrar_snackbar("Por favor, insira um valor válido.")

        valor.on_change = formatar_valor
        tipo_investimento.on_change = ao_selecionar_tipo
        confirmar_button.on_click = ao_clicar_confirmar

        self.app.pagina.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Investimento", size=24, color=ft.colors.PINK, weight=ft.FontWeight.BOLD),
                        valor,
                        tipo_investimento,
                        confirmar_button,
                        ft.ElevatedButton("Voltar", on_click=self.app.menu_operacoes.mostrar),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        )
        self.app.atualizar_saldo()
        self.app.pagina.update()


class ResultadoOperacao:
    def __init__(self, app):
        '''
        Inicializa a tela de resultado da operação.

        Parâmetros
        ----------
        app : BliBankApp
            Instância do aplicativo principal.
        '''
        self.app = app

    def mostrar(self, mensagem):
        '''
        Exibe o resultado de uma operação financeira.

        Parâmetros
        ----------
        mensagem : str
            Mensagem a ser exibida com o resultado da operação.
        '''
        self.app.pagina.controls.clear()

        self.app.pagina.add(
            ft.Container(
                content=self.app.saldo_texto,
                alignment=ft.alignment.top_right,
                padding=10,
            )
        )

        linhas = mensagem.split('\n')

        self.app.pagina.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Resultado da Operação", size=24, color=ft.colors.PINK, weight=ft.FontWeight.BOLD),
                        *[ft.Text(linha, size=18, color=ft.colors.WHITE) for linha in linhas],  
                        ft.ElevatedButton("Voltar", on_click=self.app.menu_operacoes.mostrar),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        )
        self.app.pagina.update()


class MenuCartao:
    def __init__(self, app):
        '''
        Inicializa a interface de gerenciamento de cartão de crédito.

        Parâmetros
        ----------
        app : BliBankApp
            Instância do aplicativo principal.
        '''
        self.app = app

    def mostrar(self, e=None):
        '''
        Exibe a interface de gerenciamento de cartão de crédito.
        '''
        self.app.pagina.controls.clear()
        self.app.pagina.add(
            ft.Container(
                content=self.app.saldo_texto,
                alignment=ft.alignment.top_right,
                padding=10,
            )
        )

        def ao_clicar_solicitar_cartao(e):
            '''
            Trata o clique no botão de solicitar cartão de crédito.
            '''
            if self.app.sistema.sessao_atual.cartao_credito.solicitar_cartao():
                self.app.mostrar_snackbar("Solicitação de cartão de crédito enviada.")
                self.mostrar()
            else:
                self.app.mostrar_snackbar("Solicitação já enviada. Seu cartão será aprovado em breve.")
                self.mostrar()

        def ao_clicar_detalhes_cartao(e):
            '''
            Trata o clique no botão de ver detalhes do cartão de crédito.
            '''
            self.exibir_detalhes_cartao()

        def ao_clicar_fazer_compra(e):
            '''
            Trata o clique no botão de fazer compra.
            '''
            self.mostrar_compra_interface()

        def ao_clicar_pagar_fatura(e):
            '''
            Trata o clique no botão de pagar fatura.
            '''
            self.mostrar_pagar_fatura_interface()

        def ao_clicar_aumento_limite(e):
            '''
            Trata o clique no botão de aumento de limite.
            '''
            self.mostrar_aumento_limite_interface()

        def ao_clicar_solicitar_aumento(e):
            '''
            Trata o clique no botão de solicitar aumento de limite.
            '''
            limite_requerido = self.app.sistema.sessao_atual.limite_requerido
            if limite_requerido != 0:
                self.app.mostrar_snackbar("Já tem uma solicitação pendente. Aguarde.")
            else:
                self.mostrar_aumento_limite_interface()

        status_cartao = self.app.sistema.sessao_atual.status_cartao
        mensagem_status = ""
        if status_cartao == 'pendente':
            mensagem_status = "Solicitação de cartão já enviada. Seu cartão será aprovado em breve."

        self.app.pagina.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Gerenciamento de Cartão de Crédito", size=24, color=ft.colors.PINK, weight=ft.FontWeight.BOLD),
                        ft.Text(mensagem_status, size=16, color=ft.colors.WHITE),
                        ft.ElevatedButton("Solicitar Cartão de Crédito", on_click=ao_clicar_solicitar_cartao, visible=status_cartao == 'nenhum'),
                        ft.ElevatedButton("Ver Detalhes do Cartão", on_click=ao_clicar_detalhes_cartao, visible=status_cartao == 'aprovado'),
                        ft.ElevatedButton("Fazer Compra", on_click=ao_clicar_fazer_compra, visible=status_cartao == 'aprovado'),
                        ft.ElevatedButton("Pagar Fatura", on_click=ao_clicar_pagar_fatura, visible=status_cartao == 'aprovado'),
                        ft.ElevatedButton("Solicitar Aumento de Limite", on_click=ao_clicar_solicitar_aumento, visible=status_cartao == 'aprovado'),
                        ft.ElevatedButton("Voltar", on_click=self.app.menu_cliente.mostrar),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        )
        self.app.atualizar_saldo()
        self.app.pagina.update()

    def mostrar_pagar_fatura_interface(self):
        '''
        Exibe a interface para pagar a fatura do cartão de crédito.
        '''
        self.app.pagina.controls.clear()

        cartao_credito = self.app.sistema.sessao_atual.cartao_credito
        divida_atual = self.app.sistema.sessao_atual.divida_cartao

        detalhes_fatura = [
            ft.Text(f"Valor da Fatura: R${divida_atual:.2f}", size=18, color=ft.colors.WHITE),
        ]

        pasta_faturas = "faturas"
        arquivo_fatura = os.path.join(pasta_faturas, f"fatura_{self.app.sistema.sessao_atual.get_email().replace('@', '_').replace('.', '_')}.txt")
        fatura_encontrada = False
        try:
            with open(arquivo_fatura, 'r') as fatura:
                compras = fatura.readlines()
                if compras:
                    detalhes_fatura.append(ft.Text("\nItens na Fatura:", size=18, color=ft.colors.WHITE))
                    for compra in compras:
                        detalhes_fatura.append(ft.Text(compra.strip(), size=16, color=ft.colors.WHITE))
                    fatura_encontrada = True
                else:
                    detalhes_fatura.append(ft.Text("Nenhuma fatura disponível.", size=18, color=ft.colors.WHITE))
        except FileNotFoundError:
            detalhes_fatura.append(ft.Text("Nenhuma fatura disponível.", size=18, color=ft.colors.WHITE))

        def ao_clicar_confirmar(e):
            '''
            Trata o clique no botão de confirmar pagamento da fatura.
            '''
            if divida_atual > self.app.sistema.sessao_atual.get_saldo():
                self.app.mostrar_snackbar("Saldo insuficiente.")
                return

            self.app.sistema.sessao_atual.cartao_credito.pagar_fatura()
            self.app.mostrar_snackbar("Fatura paga com sucesso.")
            self.mostrar()

        self.app.pagina.add(
            ft.Container(
                content=self.app.saldo_texto,
                alignment=ft.alignment.top_right,
                padding=10,
            )
        )

        self.app.pagina.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Pagar Fatura", size=24, color=ft.colors.PINK, weight=ft.FontWeight.BOLD),
                        *detalhes_fatura,
                        ft.ElevatedButton("Confirmar Pagamento", on_click=ao_clicar_confirmar, visible=fatura_encontrada),
                        ft.ElevatedButton("Voltar", on_click=self.mostrar),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        )
        self.app.pagina.update()

    def mostrar_compra_interface(self):
        '''
        Exibe a interface para realizar uma compra com o cartão de crédito.
        '''
        self.app.pagina.controls.clear()

        limite_disponivel = self.app.sistema.sessao_atual.limite_cartao - self.app.sistema.sessao_atual.divida_cartao

        valor_compra = ft.TextField(label="Valor da Compra", width=300, prefix_text="R$", value="0,00")
        loja = ft.TextField(label="Loja", width=300)
        descricao_item = ft.TextField(label="Descrição do Item", width=300)

        def formatar_valor(e):
            '''
            Formata o valor da compra para o padrão monetário.
            '''
            input_value = valor_compra.value
            input_value = ''.join(filter(str.isdigit, input_value))

            if not input_value:
                input_value = "0"

            while len(input_value) < 3:
                input_value = "0" + input_value

            formatted_value = f"{int(input_value[:-2]):,}.{input_value[-2:]}"
            formatted_value = formatted_value.replace(",", "X").replace(".", ",").replace("X", ".")
            valor_compra.value = formatted_value
            self.app.pagina.update()

        def formatar_texto(text):
            '''
            Formata o texto para título.
            '''
            return text.title()

        def ao_digitar_loja(e):
            '''
            Formata o texto do campo loja.
            '''
            loja.value = formatar_texto(loja.value)
            self.app.pagina.update()

        def ao_digitar_descricao(e):
            '''
            Formata o texto do campo descrição.
            '''
            descricao_item.value = formatar_texto(descricao_item.value)
            self.app.pagina.update()

        loja.on_change = ao_digitar_loja
        descricao_item.on_change = ao_digitar_descricao

        def ao_clicar_comprar(e):
            '''
            Trata o clique no botão de confirmar compra.
            '''
            try:
                valor_float = float(valor_compra.value.replace(".", "").replace(",", "."))
                if valor_float <= 0:
                    self.app.mostrar_snackbar("O valor da compra deve ser maior que zero.")
                    return

                if valor_float > limite_disponivel:
                    self.app.mostrar_snackbar("Valor da compra excede o limite disponível.")
                    return

                if not loja.value or not descricao_item.value:
                    self.app.mostrar_snackbar("Por favor, preencha todos os campos.")
                    return

                self.app.sistema.sessao_atual.cartao_credito.registrar_compra(valor_float, loja.value, descricao_item.value)
                self.app.mostrar_snackbar("Compra realizada com sucesso.")
                self.mostrar()
            except ValueError:
                self.app.mostrar_snackbar("Por favor, insira um valor válido.")

        valor_compra.on_change = formatar_valor

        self.app.pagina.add(
            ft.Container(
                content=self.app.saldo_texto,
                alignment=ft.alignment.top_right,
                padding=10,
            )
        )

        self.app.pagina.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Fazer Compra", size=24, color=ft.colors.PINK, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Limite Disponível: R${limite_disponivel:.2f}", size=18, color=ft.colors.WHITE),
                        valor_compra,
                        loja,
                        descricao_item,
                        ft.ElevatedButton("Confirmar Compra", on_click=ao_clicar_comprar),
                        ft.ElevatedButton("Voltar", on_click=self.mostrar),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        )
        self.app.atualizar_saldo()
        self.app.pagina.update()

    def mostrar_aumento_limite_interface(self):
        '''
        Exibe a interface para solicitar aumento de limite do cartão de crédito.
        '''
        self.app.pagina.controls.clear()

        limite_atual = self.app.sistema.sessao_atual.limite_cartao
        limite_formatado = f"{limite_atual:.2f}".replace(".", ",")

        valor_aumento = ft.TextField(label="Valor do Aumento", width=300, prefix_text="R$", value="0,00")

        def formatar_valor(e):
            '''
            Formata o valor do aumento de limite para o padrão monetário.
            '''
            input_value = valor_aumento.value
            input_value = ''.join(filter(str.isdigit, input_value))

            if not input_value:
                input_value = "0"

            while len(input_value) < 3:
                input_value = "0" + input_value

            formatted_value = f"{int(input_value[:-2]):,}.{input_value[-2:]}"
            formatted_value = formatted_value.replace(",", "X").replace(".", ",").replace("X", ".")
            valor_aumento.value = formatted_value
            self.app.pagina.update()

        def ao_clicar_solicitar(e):
            '''
            Trata o clique no botão de solicitar aumento de limite.
            '''
            try:
                valor_float = float(valor_aumento.value.replace(".", "").replace(",", "."))
                if valor_float <= limite_atual:
                    self.app.mostrar_snackbar(f"Solicitação de aumento recusada. O valor solicitado R${valor_aumento.value} deve ser maior que o limite atual de R${limite_formatado}.")
                else:
                    self.app.sistema.sessao_atual.cartao_credito.solicitar_aumento_limite(valor_float)
                    self.app.sistema.sessao_atual.limite_requerido = valor_float
                    self.app.mostrar_snackbar("Solicitação de aumento de limite enviada.")
                    self.mostrar()
            except ValueError:
                self.app.mostrar_snackbar("Por favor, insira um valor válido.")

        valor_aumento.on_change = formatar_valor

        self.app.pagina.add(
            ft.Container(
                content=self.app.saldo_texto,
                alignment=ft.alignment.top_right,
                padding=10,
            )
        )

        self.app.pagina.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Solicitar Aumento de Limite", size=24, color=ft.colors.PINK, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Limite Atual: R${limite_formatado}", size=18, color=ft.colors.WHITE),
                        ft.Text("O valor do aumento deve ser maior que o limite atual.", size=16, color=ft.colors.WHITE),
                        valor_aumento,
                        ft.ElevatedButton("Solicitar Aumento", on_click=ao_clicar_solicitar),
                        ft.ElevatedButton("Voltar", on_click=self.mostrar),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        )
        self.app.pagina.update()

    def exibir_detalhes_cartao(self):
        '''
        Exibe os detalhes do cartão de crédito do usuário.
        '''
        self.app.pagina.controls.clear()
        self.app.pagina.add(
            ft.Container(
                content=self.app.saldo_texto,
                alignment=ft.alignment.top_right,
                padding=10,
            )
        )

        cartao_credito = self.app.sistema.sessao_atual.cartao_credito
        limite_total = self.app.sistema.sessao_atual.limite_cartao
        limite_disponivel = self.app.sistema.sessao_atual.limite_cartao - self.app.sistema.sessao_atual.divida_cartao
        divida_atual = self.app.sistema.sessao_atual.divida_cartao

        detalhes_cartao = [
            ft.Text(f"Limite Total: R${limite_total:.2f}", size=18, color=ft.colors.WHITE),
            ft.Text(f"Limite Disponível: R${limite_disponivel:.2f}", size=18, color=ft.colors.WHITE),
            ft.Text(f"Dívida Atual: R${divida_atual:.2f}", size=18, color=ft.colors.WHITE),
        ]

        pasta_faturas = "faturas"
        arquivo_fatura = os.path.join(pasta_faturas, f"fatura_{self.app.sistema.sessao_atual.get_email().replace('@', '_').replace('.', '_')}.txt")
        try:
            with open(arquivo_fatura, 'r') as fatura:
                compras = fatura.readlines()
                if compras:
                    detalhes_cartao.append(ft.Text("\nItens na Fatura:", size=18, color=ft.colors.WHITE))
                    for compra in compras:
                        detalhes_cartao.append(ft.Text(compra.strip(), size=16, color=ft.colors.WHITE))
                else:
                    detalhes_cartao.append(ft.Text("Nenhuma fatura disponível.", size=18, color=ft.colors.WHITE))
        except FileNotFoundError:
            detalhes_cartao.append(ft.Text("Nenhuma fatura disponível.", size=18, color=ft.colors.WHITE))

        self.app.pagina.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Detalhes do Cartão de Crédito", size=24, color=ft.colors.PINK, weight=ft.FontWeight.BOLD),
                        *detalhes_cartao,
                        ft.ElevatedButton("Voltar", on_click=self.mostrar),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        )
        self.app.pagina.update()


class MenuAdmin:
    def __init__(self, app):
        '''
        Inicializa a interface de administração.
        
        Parâmetros
        ----------
        app : BliBankApp
            Instância do aplicativo principal.
        '''
        self.app = app

    def mostrar(self, e=None):
        '''
        Exibe a interface do menu do administrador.
        '''
        self.app.pagina.controls.clear()

        def ao_clicar_aprovar_cartoes(e):
            '''
            Trata o clique no botão de aprovar cartões de crédito.
            '''
            self.exibir_aprovacao_cartoes()

        def ao_clicar_ajustar_limites(e):
            '''
            Trata o clique no botão de ajustar limites de crédito.
            '''
            self.exibir_solicitacoes_aumento_limite()

        def ao_clicar_encerrar_contas(e):
            '''
            Trata o clique no botão de encerrar contas de clientes.
            '''
            self.exibir_solicitacoes_encerramento()

        def ao_clicar_visualizar_info(e):
            '''
            Trata o clique no botão de visualizar informações de clientes.
            '''
            self.exibir_lista_clientes()

        def ao_clicar_logout(e):
            '''
            Trata o clique no botão de logout.
            '''
            mensagem_logout = self.app.sistema.logout()
            self.app.mostrar_snackbar(mensagem_logout)
            self.app.tela_inicial.mostrar()

        self.app.pagina.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Menu Administrador", size=24, color=ft.colors.PINK, weight=ft.FontWeight.BOLD),
                        ft.ElevatedButton("Aprovar Cartões de Crédito", on_click=ao_clicar_aprovar_cartoes),
                        ft.ElevatedButton("Ajustar Limites de Crédito", on_click=ao_clicar_ajustar_limites),
                        ft.ElevatedButton("Encerrar Contas de Clientes", on_click=ao_clicar_encerrar_contas),
                        ft.ElevatedButton("Visualizar Informações de Clientes", on_click=ao_clicar_visualizar_info),
                        ft.ElevatedButton("Logout", on_click=ao_clicar_logout),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        )
        self.app.pagina.update()

    def exibir_aprovacao_cartoes(self):
        '''
        Exibe a interface para aprovação de cartões de crédito.
        '''
        self.app.pagina.controls.clear()
        pendentes = [cliente for cliente in self.app.sistema.gerenciador.usuarios if isinstance(cliente, Cliente) and cliente.status_cartao == 'pendente']

        if not pendentes:
            self.app.pagina.add(ft.Text("Nenhum cartão pendente para aprovação.", size=18, color=ft.colors.RED, text_align=ft.TextAlign.CENTER))
            self.app.pagina.add(ft.ElevatedButton("Voltar", on_click=self.mostrar))
            self.app.pagina.update()
            return

        radios = []
        for i, cliente in enumerate(pendentes, start=1):
            radios.append(ft.Radio(value=str(i), label=f"{cliente.get_nome()} (Email: {cliente.get_email()})"))

        grupo_opcoes = ft.RadioGroup(
            value="1",  
            content=ft.Column(radios, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

        limite_inicial = ft.TextField(label="Limite Inicial do Cartão", width=300, value="R$0,00")

        def ao_clicar_aprovar(e):
            '''
            Trata o clique no botão de aprovar cartão.
            '''
            selecao = grupo_opcoes.value
            if selecao is not None:
                indice = int(selecao) - 1
                cliente_selecionado = pendentes[indice]
                try:
                    limite_formatado = limite_inicial.value.replace("R$", "").replace(".", "").replace(",", ".").strip()
                    limite = float(limite_formatado)
                    cliente_selecionado.limite_cartao = limite
                    cliente_selecionado.divida_cartao = 0.0  
                    cliente_selecionado.status_cartao = 'aprovado'
                    self.app.sistema.gerenciador.salvar_usuarios()
                    self.app.mostrar_snackbar(f"Cartão de {cliente_selecionado.get_nome()} aprovado com sucesso.")
                    self.mostrar()
                except ValueError:
                    self.app.mostrar_snackbar("Por favor, insira um valor de limite válido.")
            else:
                self.app.mostrar_snackbar("Nenhum cliente selecionado.")

        def formatar_valor(e):
            '''
            Formata o valor do limite inicial do cartão.
            '''
            input_value = limite_inicial.value.replace("R$", "").strip()
            input_value = ''.join(filter(str.isdigit, input_value))

            if not input_value:
                input_value = "0"

            while len(input_value) < 3:
                input_value = "0" + input_value

            formatted_value = f"R${int(input_value[:-2]):,}.{input_value[-2:]}"
            formatted_value = formatted_value.replace(",", "X").replace(".", ",").replace("X", ".")
            limite_inicial.value = formatted_value
            self.app.pagina.update()

        limite_inicial.on_change = formatar_valor

        self.app.pagina.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Aprovação de Cartões de Crédito", size=24, color=ft.colors.PINK, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        grupo_opcoes,
                        limite_inicial,
                        ft.ElevatedButton("Aprovar", on_click=ao_clicar_aprovar),
                        ft.ElevatedButton("Voltar", on_click=self.mostrar),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        )
        self.app.pagina.update()

    def exibir_solicitacoes_aumento_limite(self):
        '''
        Exibe a interface para aprovação de solicitações de aumento de limite.
        '''
        self.app.pagina.controls.clear()
        solicitacoes = [cliente for cliente in self.app.sistema.gerenciador.usuarios if isinstance(cliente, Cliente) and cliente.limite_requerido > 0]

        if not solicitacoes:
            self.app.pagina.add(ft.Text("Não há solicitações de aumento de limite pendentes.", size=18, color=ft.colors.RED, text_align=ft.TextAlign.CENTER))
            self.app.pagina.add(ft.ElevatedButton("Voltar", on_click=self.mostrar))
            self.app.pagina.update()
            return

        radios = []
        for i, cliente in enumerate(solicitacoes, start=1):
            radios.append(ft.Radio(value=str(i), label=f"{cliente.get_nome()} (Email: {cliente.get_email()}, Solicitação: R${cliente.limite_requerido:.2f})"))

        grupo_opcoes = ft.RadioGroup(
            value="1", 
            content=ft.Column(radios, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

        def ao_clicar_aprovar_limite(e):
            '''
            Trata o clique no botão de aprovar limite.
            '''
            selecao = grupo_opcoes.value
            if selecao is not None:
                indice = int(selecao) - 1
                cliente_selecionado = solicitacoes[indice]
                cliente_selecionado.limite_cartao = cliente_selecionado.limite_requerido
                cliente_selecionado.limite_requerido = 0  
                self.app.sistema.gerenciador.salvar_usuarios() 
                self.app.mostrar_snackbar(f"Limite de {cliente_selecionado.get_nome()} aprovado com sucesso.")
                self.mostrar()
            else:
                self.app.mostrar_snackbar("Nenhum cliente selecionado.")

        self.app.pagina.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Aprovação de Aumento de Limite", size=24, color=ft.colors.PINK, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        grupo_opcoes,
                        ft.ElevatedButton("Aprovar Limite", on_click=ao_clicar_aprovar_limite),
                        ft.ElevatedButton("Voltar", on_click=self.mostrar),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        )
        self.app.pagina.update()

    def exibir_solicitacoes_encerramento(self):
        '''
        Exibe a interface para aprovação de solicitações de encerramento de contas.
        '''
        self.app.pagina.controls.clear()
        solicitacoes = [cliente for cliente in self.app.sistema.gerenciador.usuarios if isinstance(cliente, Cliente) and cliente.solicitar_encerramento]

        if not solicitacoes:
            self.app.pagina.add(ft.Text("Não há solicitações de encerramento pendentes.", size=18, color=ft.colors.RED, text_align=ft.TextAlign.CENTER))
            self.app.pagina.add(ft.ElevatedButton("Voltar", on_click=self.mostrar))
            self.app.pagina.update()
            return

        radios = []
        for i, cliente in enumerate(solicitacoes, start=1):
            radios.append(ft.Radio(value=str(i), label=f"{cliente.get_nome()} (Email: {cliente.get_email()})"))

        grupo_opcoes = ft.RadioGroup(
            value="1",  
            content=ft.Column(radios, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

        def ao_clicar_aprovar_encerramento(e):
            '''
            Trata o clique no botão de aprovar encerramento de conta.
            '''
            selecao = grupo_opcoes.value
            if selecao is not None:
                indice = int(selecao) - 1
                cliente_selecionado = solicitacoes[indice]
                cliente_selecionado.solicitar_encerramento = False
                self.app.sistema.gerenciador.usuarios.remove(cliente_selecionado)  
                self.app.sistema.gerenciador.salvar_usuarios()  
                self.app.mostrar_snackbar(f"Encerramento da conta de {cliente_selecionado.get_nome()} aprovado com sucesso.")
                self.mostrar()
            else:
                self.app.mostrar_snackbar("Nenhum cliente selecionado.")

        self.app.pagina.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Solicitações de Encerramento de Contas", size=24, color=ft.colors.PINK, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        grupo_opcoes,
                        ft.ElevatedButton("Aprovar Encerramento", on_click=ao_clicar_aprovar_encerramento),
                        ft.ElevatedButton("Voltar", on_click=self.mostrar),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        )
        self.app.pagina.update()

    def exibir_lista_clientes(self, e=None):
        '''
        Exibe a lista de clientes.
        '''
        self.app.pagina.controls.clear()
        clientes = [cliente for cliente in self.app.sistema.gerenciador.usuarios if isinstance(cliente, Cliente)]

        radios = []
        for i, cliente in enumerate(clientes, start=1):
            radios.append(ft.Radio(value=str(i), label=f"{cliente.get_nome()} {cliente.get_sobrenome()} (Email: {cliente.get_email()})"))

        grupo_opcoes = ft.RadioGroup(
            value="1", 
            content=ft.Column(radios, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

        def ao_clicar_ver_detalhes(e):
            '''
            Trata o clique no botão de ver detalhes do cliente.
            '''
            selecao = grupo_opcoes.value
            if selecao is not None:
                indice = int(selecao) - 1
                cliente_selecionado = clientes[indice]
                self.exibir_detalhes_cliente(cliente_selecionado)
            else:
                self.app.mostrar_snackbar("Nenhum cliente selecionado.")

        self.app.pagina.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Lista de Clientes", size=24, color=ft.colors.PINK, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        grupo_opcoes,
                        ft.ElevatedButton("Ver Detalhes", on_click=ao_clicar_ver_detalhes),
                        ft.ElevatedButton("Voltar", on_click=self.mostrar),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        )
        self.app.pagina.update()

    def exibir_detalhes_cliente(self, cliente):
        '''
        Exibe os detalhes de um cliente específico.
        
        Parâmetros
        ----------
        cliente : Cliente
            O cliente cujos detalhes serão exibidos.
        '''
        self.app.pagina.controls.clear()

        saldo_formatado = f"{cliente.get_saldo():,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        limite_cartao_formatado = f"{cliente.limite_cartao:.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        divida_cartao_formatada = f"{cliente.divida_cartao:.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        limite_requerido_formatado = f"{cliente.limite_requerido:.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        self.app.pagina.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(f"Nome: {cliente.get_nome()}", size=20, color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER),
                        ft.Text(f"Sobrenome: {cliente.get_sobrenome()}", size=20, color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER),
                        ft.Text(f"Email: {cliente.get_email()}", size=20, color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER),
                        ft.Text(f"CPF: {cliente.get_cpf()}", size=20, color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER),
                        ft.Text(f"Saldo Atual: R${saldo_formatado}", size=20, color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER),
                        ft.Text(f"Limite Cartão: R${limite_cartao_formatado}", size=20, color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER),
                        ft.Text(f"Status Cartão: {cliente.status_cartao}", size=20, color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER),
                        ft.Text(f"Dívida Cartão: R${divida_cartao_formatada}", size=20, color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER),
                        ft.Text(f"Requerimento de Aumento de Limite: R${limite_requerido_formatado}", size=20, color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER),
                        ft.Text(f"Solicitação de Encerramento de Conta: {'Sim' if cliente.solicitar_encerramento else 'Não'}", size=20, color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER),
                        ft.ElevatedButton("Voltar", on_click=self.exibir_lista_clientes),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        )
        self.app.pagina.update()


class BliBankApp:
    def __init__(self):
        '''
        Inicializa a aplicação BliBank.
        '''
        self.sistema = SistemaBliBank()
        self.saldo_texto = None
        self.tela_inicial = TelaInicial(self)
        self.tela_login = TelaLogin(self)
        self.tela_cadastro = TelaCadastro(self)
        self.menu_cliente = MenuCliente(self)
        self.menu_operacoes = MenuOperacoes(self)
        self.tela_valor = TelaValor(self)
        self.tela_transferencia = TelaTransferencia(self)
        self.tela_investimento = TelaInvestimento(self)
        self.resultado_operacao = ResultadoOperacao(self)
        self.menu_cartao = MenuCartao(self)
        self.menu_admin = MenuAdmin(self)

    def inicial(self, pagina: ft.Page):
        '''
        Inicializa a página principal do aplicativo.

        Parâmetros
        ----------
        pagina : ft.Page
            Página principal do aplicativo.
        '''
        self.pagina = pagina
        self.pagina.title = "BliBank"
        self.pagina.window_maximized = True
        self.pagina.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.pagina.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        saldo_inicial = self.sistema.sessao_atual.get_saldo() if self.sistema.sessao_atual else 0.0
        saldo_formatado = f"{saldo_inicial:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        self.saldo_texto = ft.Text(f"Saldo: R${saldo_formatado}", size=18, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD)
        self.pagina.add(self.saldo_texto)
        self.tela_inicial.mostrar()

    def atualizar_saldo(self):
        '''
        Atualiza o saldo exibido na interface.
        '''
        if self.sistema.sessao_atual:
            saldo_formatado = f"{self.sistema.sessao_atual.get_saldo():,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            self.saldo_texto.value = f"Saldo: R${saldo_formatado}"
            if self.saldo_texto.page:  
                self.saldo_texto.update()

    def mostrar_snackbar(self, mensagem):
        '''
        Exibe uma mensagem temporária na parte inferior da tela.

        Parâmetros
        ----------
        mensagem : str
            Mensagem a ser exibida.
        '''
        self.pagina.snack_bar = ft.SnackBar(ft.Text(mensagem), duration=2000)
        self.pagina.snack_bar.open = True
        self.pagina.update()

    def mostrar_resultado_operacao(self, mensagem):
        '''
        Exibe o resultado de uma operação.

        Parâmetros
        ----------
        mensagem : str
            Mensagem com o resultado da operação.
        '''
        self.resultado_operacao.mostrar(mensagem)
