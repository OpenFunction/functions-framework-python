from datetime import datetime

from functions_framework.context.user_context import UserContext


def user_function(context: UserContext):
    # context.get_http_request() is a flask request object
    print(context.get_http_request())

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    output_data = "hello world"
    return output_data
