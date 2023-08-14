from functions_framework.context.user_context import UserContext


def test_function(context: UserContext):
    return "hello world"
