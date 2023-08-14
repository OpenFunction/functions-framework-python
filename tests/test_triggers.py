# Copyright 2023 The OpenFunction Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import threading
import time
import unittest

from unittest.mock import MagicMock, Mock

from src.functions_framework.context.function_context import DaprTrigger
from src.functions_framework.context.runtime_context import RuntimeContext
from src.functions_framework.triggers.dapr_trigger.dapr import DaprTriggerHandler
from src.functions_framework.triggers.http_trigger import _http
from src.functions_framework.triggers.http_trigger.http import HTTPTriggerHandler


class TestHttpTrigger(unittest.TestCase):
    def test_http_server_creation(self):
        app = MagicMock()
        server = _http.create_server(app, debug=True)
        self.assertIsNotNone(server)

    def test_http_trigger_handler_start(self):
        trigger = HTTPTriggerHandler(port=0, trigger=MagicMock(), user_function=MagicMock())
        context = MagicMock()
        with self.assertRaises(Exception):
            trigger.start(context)


class TestDaprTrigger(unittest.TestCase):
    def test_dapr_trigger_handler(self):
        # Create a mock RuntimeContext and logger
        context = Mock(spec=RuntimeContext)
        logger = Mock()

        # Create an example DaprTrigger
        dapr_trigger = DaprTrigger(
            name="example",
            component_type="pubsub.redis",
            topic="example-topic",
        )

        # Create an instance of DaprTriggerHandler and start it
        dapr_handler = DaprTriggerHandler(port=50055, triggers=[dapr_trigger])

        # Start the Dapr trigger handler in a separate thread
        dapr_thread = threading.Thread(target=dapr_handler.start, args=(context, logger))
        dapr_thread.start()

        # Wait for 5 seconds
        time.sleep(5)

        # Stop the Dapr trigger handler
        dapr_handler.app.stop()

        # Wait for the Dapr trigger handler thread to finish
        dapr_thread.join()


if __name__ == '__main__':
    unittest.main()
