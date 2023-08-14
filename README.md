# Functions Framework for Python

[![PyPI version](https://badge.fury.io/py/ofn-functions-framework.svg)](https://badge.fury.io/py/ofn-functions-framework)

This project is inspired by [GCP functions-framework-python](https://github.com/GoogleCloudPlatform/functions-framework-python) .

An open source FaaS (Function as a service) framework for writing portable Python functions.

The Functions Framework lets you write lightweight functions that run in many different environments, including:

*   [OpenFunction](https://github.com/OpenFunction/OpenFunction)
*   [Knative](https://github.com/knative/)-based environments
*   [Dapr](https://dapr.io/)-based environments
*   Your local development machine

The framework allows you to go from:

```python
from functions_framework.context.user_context import UserContext

def hello(context: UserContext):
    return "Hello world!"
```

To:

```sh
curl http://my-url
# Output: Hello world!
```

All without needing to worry about writing an HTTP server or complicated request handling logic.

## Features

*   Spin up a local development server for quick testing
*   Invoke a function in response to a request
*   Portable between serverless platforms
*   Can integrate various data middlewares

## Installation

Install the Functions Framework via `pip`:

```sh
pip install ofn-functions-framework
```

Or, for deployment, add the Functions Framework to your `requirements.txt` file:

```
ofn-functions-framework==0.2.0
```

## Quickstarts

### Quickstart: HTTP Function (Hello World)

Create an `main.py` file with the following contents:

```python
from functions_framework.context.user_context import UserContext


def hello(context: UserContext):
    # context.get_http_request()
    return "Hello world!"
```

Export Function Context:

```shell
export FUNC_CONTEXT='{"name":"function_name","version":"v1","triggers":{"http":{"port":8080}}}'
```

Run the following command:

```sh
ff --source hello_world.py --target hello
```

Open http://localhost:8080/ in your browser and see *Hello world!*.

Or send requests to this function using `curl` from another terminal window:

```sh
curl localhost:8080
# Output: Hello world!
```

## Run your function on OpenFunction

![OpenFunction Platform Overview](https://openfunction.dev/openfunction-0.5-architecture.png)

Besides Knative function support, one notable feature of OpenFunction is embracing Dapr system, so far Dapr pub/sub and bindings have been support.

Dapr bindings allows you to trigger your applications or services with events coming in from external systems, or interface with external systems. OpenFunction [0.6.0 release](https://openfunction.dev/blog/2022/03/25/announcing-openfunction-0.6.0-faas-observability-http-trigger-and-more/) adds Dapr output bindings to its synchronous functions which enables HTTP triggers for asynchronous functions. For example, synchronous functions backed by the Knative runtime can now interact with middlewares defined by Dapr output binding or pub/sub, and an asynchronous function will be triggered by the events sent from the synchronous function.

Asynchronous function introduces Dapr pub/sub to provide a platform-agnostic API to send and receive messages. A typical use case is that you can leverage synchronous functions to receive an event in plain JSON or Cloud Events format, and then send the received event to a Dapr output binding or pub/sub component, most likely a message queue (e.g. Kafka, NATS Streaming, GCP PubSub, MQTT). Finally, the asynchronous function could be triggered from the message queue.

More details would be brought up to you in some quickstart samples, stay tuned.

## Configure the Functions Framework

You can configure the Functions Framework using command-line flags or environment variables. If you specify both, the environment variable will be ignored.

| Command-line flag | Environment variable | Description                                                  |
| ----------------- | -------------------- | ------------------------------------------------------------ |
| `--host`          | `HOST`               | The host on which the Functions Framework listens for requests. Default: `0.0.0.0` |
| `--port`          | `PORT`               | The port on which the Functions Framework listens for requests. Default: `8080` |
| `--target`        | `FUNCTION_TARGET`    | The name of the exported function to be invoked in response to requests. Default: `function` |
| `--source`        | `FUNCTION_SOURCE`    | The path to the file containing your function. Default: `main.py` (in the current working directory) |
| `--debug`         | `DEBUG`              | A flag that allows to run functions-framework to run in debug mode, including live reloading. Default: `False` |
| `--dry-run`       | `DRY_RUN`            | A flag that allows for testing the function build from the configuration without creating a server. Default: `False` |

## Advanced Examples

More advanced guides can be found in the [`examples/`](examples/) directory.
