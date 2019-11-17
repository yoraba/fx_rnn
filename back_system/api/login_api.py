from back_system.shared import SharedContext


class Login_API:

    def on_login(self, password) -> bool:
        try:
            SharedContext(password)
            return True
        except Exception as e:
            print(e)
            return False

    def get_context(self, password) -> SharedContext:
        context = SharedContext(password)
        context.initialize_db()
        return context
