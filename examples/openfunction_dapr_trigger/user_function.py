from datetime import datetime

from functions_framework.context.user_context import UserContext


def user_function(context: UserContext):
    print(context.get_binding_request().metadata, flush=True)
    print(context.get_binding_request().text(), flush=True)

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

    # 调用 FunctionContext 实例的方法
    # context.dapr_client.invoke_method(...)

    # 用户函数处理逻辑
    output_data = "hahahahaha"
    return output_data
