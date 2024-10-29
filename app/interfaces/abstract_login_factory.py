from abc import ABC, abstractmethod
from login_factory import LoginInterface, CompanyALogin, CompanyBLogin

class AbstractLoginFactory(ABC):
    
    @abstractmethod
    def create_login(self) -> LoginInterface:
        pass

class CompanyALoginFactory(AbstractLoginFactory):
    
    def create_login(self) -> LoginInterface:
        return CompanyALogin()

class CompanyBLoginFactory(AbstractLoginFactory):
    
    def create_login(self) -> LoginInterface:
        return CompanyBLogin()