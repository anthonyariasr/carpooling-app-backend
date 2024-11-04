from abc import ABC, abstractmethod

from app.tec_db.tec_db import check_existance_tec, validate_user_tec

class AuthProvider(ABC):
    
    @abstractmethod
    def authenticate(self, email: str, password: str) -> bool:
        pass

class TecAuthProvider(AuthProvider):
    def authenticate(self, email: str, password: str) -> bool:
        print("Authenticating with TEC")
        return validate_user_tec(email, password)  # Return True if authentication is successful, False otherwise
    def check_existance(self, email: str) -> bool:
        print("Checking existance with TEC")
        return check_existance_tec(email)

class Empresa2AuthProvider(AuthProvider):
    def authenticate(self, email: str, password: str) -> bool:
        # Add specific logic to authenticate Empresa 2 users here
        print("Authenticating with Empresa 2")
        return True  # Return True if authentication is successful, False otherwise
    def check_existance(self, email: str) -> bool:
        print("Checking existance with Empresa 2")
        return True

class ExampleAuthProvider(AuthProvider):
    def authenticate(self, email: str, password: str) -> bool:
        # Add specific logic to authenticate Empresa 2 users here
        print("Authenticating with Example")
        return True  # Return True if authentication is successful, False otherwise
    def check_existance(self, email: str) -> bool:
        print("Checking existance with Example")
        return True
