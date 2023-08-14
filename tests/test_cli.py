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
import pathlib
import unittest

from unittest import mock

from functions_framework._cli import _cli


class TestCLI(unittest.TestCase):
    TEST_FUNCTIONS_DIR = pathlib.Path(__file__).resolve().parent / "test_data"
    source = TEST_FUNCTIONS_DIR / "test_source.py"

    args = [
        "--target", "test_function",
        "--source", source,
        "--host", "localhost",
        "--port", "8081",
        "--debug"
    ]

    @mock.patch('sys.argv', ['functions-framework'] + args)
    def test_main_with_function(self):
        with self.assertRaises(SystemExit) as cm:
            _cli()

        self.assertEqual(cm.exception.code, 0)

    @mock.patch('sys.argv', ['functions-framework'])
    def test_main_without_function(self):
        with self.assertRaises(SystemExit) as cm:
            _cli()

        self.assertEqual(cm.exception.code, 2)


if __name__ == '__main__':
    unittest.main()

