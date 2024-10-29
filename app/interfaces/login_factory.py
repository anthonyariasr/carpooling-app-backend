from abc import ABC, abstractmethod

class LoginInterface(ABC):
    
    @abstractmethod
    def login(self, username: str, password: str) -> bool:
        pass
    
    @abstractmethod
    def logout(self) -> bool:
        pass

class CompanyALogin(LoginInterface):
    
    def login(self, username: str, password: str) -> bool:
        # Lógica específica para el login de la empresa A
        print("Logging into Company A")
        return True
    
    def logout(self) -> bool:
        # Lógica para cerrar sesión en la empresa A
        print("Logging out of Company A")
        return True


class CompanyBLogin(LoginInterface):
    
    def login(self, username: str, password: str) -> bool:
        # Lógica específica para el login de la empresa B
        print("Logging into Company B")
        return True
    
    def logout(self) -> bool:
        # Lógica para cerrar sesión en la empresa B
        print("Logging out of Company B")
        return True