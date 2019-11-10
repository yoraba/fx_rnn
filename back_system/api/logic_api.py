from back_system.shared import SharedContext


class LoginAPI:

    @staticmethod
    def on_login(password: str) -> SharedContext:
        if password == '':
            raise Exception()
        return SharedContext(password)
