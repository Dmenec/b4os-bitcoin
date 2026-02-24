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

from test_framework.util import assert_greater_than
from test_framework.wallet import MiniWallet
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

        # Create a MiniWallet bound to node 0
        wallet = MiniWallet(self.nodes[0])

        # MiniWallet usually starts with mature UTXOs from the cached chain
        assert_greater_than(wallet.get_balance(), 0)

        # Build + broadcast a simple self-transfer transaction
        wallet.send_self_transfer(from_node=self.nodes[0])

        assert len(self.nodes[0].getrawmempool()) == 1

        self.generate(self.nodes[0], 1)

        mempool_length = len(self.nodes[0].getrawmempool())
        assert mempool_length == 0
        self.log.info("Mempool ok")

if __name__ == '__main__':
    ExampleTest(__file__).main()
