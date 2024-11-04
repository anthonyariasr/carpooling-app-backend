# interfaces/auth_factory.py
from .auth_provider import AuthProvider, TecAuthProvider, Empresa2AuthProvider, ExampleAuthProvider

class AuthFactory:
    # Define a mapping of email domains to their respective authentication providers
    _providers = {
        'tec.cr': TecAuthProvider,
        'estudiantec.cr': TecAuthProvider,
        'empresa2.com': Empresa2AuthProvider,
        'example.com': ExampleAuthProvider,
    }
    
    @staticmethod
    def get_auth_provider(email: str) -> AuthProvider:
        # Extract the domain from the email
        domain = email.split('@')[-1]
        
        # Look up the provider in the mapping dictionary
        provider_class = AuthFactory._providers.get(domain)
        if provider_class is None:
            raise ValueError(f"Email domain '{domain}' not supported.")
        
        # Return an instance of the provider class
        return provider_class()
