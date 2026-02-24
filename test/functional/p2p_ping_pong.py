#!/usr/bin/env python3
# Copyright (c) 2017-present The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""An example functional test

The module-level docstring should include a high-level description of
what the test is doing. It's the first thing people see when they open
the file and should give the reader information about *what* the test
is testing and *how* it's being tested
"""

from test_framework.util import assert_equal
from test_framework.messages import msg_ping
from test_framework.p2p import P2PInterface
from test_framework.test_framework import BitcoinTestFramework

class ExampleTest(BitcoinTestFramework):
    # Each functional test is a subclass of the BitcoinTestFramework class.

    # Override the set_test_params(), skip_test_if_missing_module(), add_options(), setup_chain(), setup_network()
    # and setup_nodes() methods to customize the test setup as required.

    def set_test_params(self):
        """Override test parameters for your individual test.

        This method must be overridden and num_nodes must be explicitly set."""
        self.num_nodes = 1

    def run_test(self):
        """Main test logic"""

        p2p_conn = self.nodes[0].add_p2p_connection(P2PInterface())
        p2p_conn.send_without_ping(msg_ping(nonce = 1))
        p2p_conn.wait_until(lambda: "pong" in p2p_conn.last_message, timeout=5)
        assert_equal(p2p_conn.last_message['pong'].nonce, 1)

if __name__ == '__main__':
    ExampleTest(__file__).main()
