Use kubectl to apply the [manifests](./manifests.yaml), then connect the container via [nocalhost](https://nocalhost.dev/).

FUNC_CONTEXT example:


```json
{
  "name": "ff-python",
  "version": "v1",
  "triggers": {
    "http": {
      "port": 8080
    }
  }
}
```

After logging into the container terminal, export `FUNC_CONTEXT`:

```shell
export FUNC_CONTEXT='{"name":"ff-python","version":"v1","triggers":{"http":{"port":8080}}}'
```

Run function:

```shell
ff --source examples/openfunction_http_trigger/user_function.py --target user_function
```

Start a curl pod to access the function:

```shell
~ $ curl ff-python-http-service

hello world
```

