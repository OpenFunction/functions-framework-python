Follow [this guide](https://github.com/OpenFunction/samples/blob/main/Prerequisites.md#kafka) to install a Kafka server named `kafka-server` and a Topic named `sample-topic`.

Follow [this guide](https://docs.dapr.io/getting-started/) to install DAPR.

Use kubectl to apply the [manifests](./manifests.yaml), then connect the container via [nocalhost](https://nocalhost.dev/).

Create a DAPR Component:

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-binding
spec:
  type: bindings.kafka
  version: v1
  metadata:
  - name: topics
    value: "sample-topic"
  - name: brokers
    value: "kafka-server:9092"
  - name: consumerGroup
    value: "group1"
  - name: publishTopic
    value: "sample-topic"
  - name: authRequired
    value: "false"
```

FUNC_CONTEXT example:


```json
{
  "name": "ff-python",
  "version": "v1",
  "triggers": {
    "dapr": [
      {
        "name": "kafka-binding",
        "type": "bindings.kafka"
      }
    ]
  },
  "port": 50055
}
```

After logging into the container terminal, export `FUNC_CONTEXT`:

```shell
export FUNC_CONTEXT='{"name":"ff-python","version":"v1","triggers":{"dapr":[{"name":"kafka-binding","type":"bindings.kafka"}]},"port":50055}'
```

Run function:

```shell
ff --source examples/openfunction_dapr_trigger/user_function.py --target user_function
```

Use the DAPR client to call function or you can apply the [caller](caller)

```python
import json
import time

from dapr.clients import DaprClient

with DaprClient() as d:
    n = 0
    while True:
        n += 1
        req_data = {
            'id': n,
            'message': 'hello world'
        }

        print(f'Sending message id: {req_data["id"]}, message "{req_data["message"]}"', flush=True)

        # Create a typed message with content type and body
        _ = d.invoke_binding('kafka-binding', 'create', json.dumps(req_data))

        time.sleep(2)
```
