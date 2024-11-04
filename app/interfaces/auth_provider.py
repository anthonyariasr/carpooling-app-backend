from abc import ABC, abstractmethod

class AuthProvider(ABC):
    
    @abstractmethod
    def authenticate(self, email: str, password: str) -> bool:
        pass

class TecAuthProvider(AuthProvider):
    def authenticate(self, email: str, password: str) -> bool:
        # Add specific logic to authenticate TEC users here
        print("Authenticating with TEC")
        return True  # Return True if authentication is successful, False otherwise

class Empresa2AuthProvider(AuthProvider):
    def authenticate(self, email: str, password: str) -> bool:
        # Add specific logic to authenticate Empresa 2 users here
        print("Authenticating with Empresa 2")
        return True  # Return True if authentication is successful, False otherwise

class ExampleAuthProvider(AuthProvider):
    def authenticate(self, email: str, password: str) -> bool:
        # Add specific logic to authenticate Empresa 2 users here
        print("Authenticating with Example")
        return True  # Return True if authentication is successful, False otherwise
