from abc import ABC, abstractmethod

class Usuario(ABC):
    def __init__(self, nome: str, sobrenome: str, email: str, senha: str, cpf: int) -> None:
        '''
        Inicializa um objeto Usuario.

        Parâmetros
        ----------
        nome : str
            Nome do usuário.
        sobrenome : str
            Sobrenome do usuário.
        email : str
            Email do usuário.
        senha : str
            Senha do usuário.
        cpf : int
            CPF do usuário.
        '''
        self.__nome = nome
        self.__sobrenome = sobrenome
        self.__email = email.lower().strip()
        self.__senha = senha
        self.__cpf = cpf

    def get_nome(self) -> str:
        '''
        Retorna o nome do usuário.

        Retorna
        -------
        str
            Nome do usuário.
        '''
        return self.__nome

    def get_sobrenome(self) -> str:
        '''
        Retorna o sobrenome do usuário.

        Retorna
        -------
        str
            Sobrenome do usuário.
        '''
        return self.__sobrenome

    def get_email(self) -> str:
        '''
        Retorna o email do usuário.

        Retorna
        -------
        str
            Email do usuário.
        '''
        return self.__email

    def get_senha(self) -> str:
        '''
        Retorna a senha do usuário.

        Retorna
        -------
        str
            Senha do usuário.
        '''
        return self.__senha

    def get_cpf(self) -> int:
        '''
        Retorna o CPF do usuário.

        Retorna
        -------
        int
            CPF do usuário.
        '''
        return self.__cpf

    def get_cpf_formatado(self) -> str:
        '''
        Retorna o CPF do usuário formatado.

        Retorna
        -------
        str
            CPF do usuário formatado.
        '''
        cpf = str(self.__cpf).zfill(11)
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

    @abstractmethod
    def cadastrar(self) -> None:
        '''
        Método abstrato para cadastrar o usuário.
        '''
        pass
    
    @abstractmethod
    def to_dict(self) -> dict:
        '''
        Método abstrato para converter os dados do usuário para um dicionário.

        Retorna
        -------
        dict
            Dicionário contendo os dados do usuário.
        '''
        pass
