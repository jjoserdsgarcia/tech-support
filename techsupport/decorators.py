"""
decorators.py

Este arquivo reúne decoradores personalizados do projeto.

Decoradores são funções que adicionam uma camada de verificação
antes da execução de uma view.

Neste projeto utilizamos um decorador para permitir acesso
somente a usuários autenticados e marcados como "staff".
"""

from django.contrib.auth.decorators import user_passes_test


def staff_required(view_func):
    """
    Restringe o acesso da view apenas para usuários do tipo Staff.

    O usuário deve atender às duas condições:
    - Estar autenticado (is_authenticated)
    - Possuir is_staff = True

    Caso contrário, será redirecionado para a tela de login.
    """

    return user_passes_test(
        # Verifica se o usuário está logado e é membro da equipe
        lambda user: user.is_authenticated and user.is_staff,

        # Página para onde o usuário será enviado caso não tenha acesso
        login_url='loginscreen'

    )(view_func)