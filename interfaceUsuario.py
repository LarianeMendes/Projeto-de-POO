from abc import ABC, abstractmethod

class Usuario(ABC):
    def __init__(self, nome: str, sobrenome: str, email: str, senha: str, cpf: int) -> None:
        self.__nome = nome
        self.__sobrenome = sobrenome
        self.__email = email.lower().strip()
        self.__senha = senha
        self.__cpf = cpf

    def get_nome(self) -> str:
        return self.__nome

    def get_sobrenome(self) -> str:
        return self.__sobrenome

    def get_email(self) -> str:
        return self.__email

    def get_senha(self) -> str:
        return self.__senha

    def get_cpf(self) -> int:
        return self.__cpf

    def get_cpf_formatado(self) -> str:
        cpf = str(self.__cpf).zfill(11)
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

    @abstractmethod
    def cadastrar(self) -> None:
        pass
    
    @abstractmethod
    def to_dict(self) -> dict:
        pass
