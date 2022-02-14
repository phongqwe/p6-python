import unittest

from jupyter_client import KernelClient


class Bench(unittest.TestCase):
    def test_z(self):
        client = KernelClient()
        client.shell_channel
