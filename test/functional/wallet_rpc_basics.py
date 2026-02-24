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
# Imports should be in PEP8 ordering (std library first, then third party
# libraries then local imports).
from collections import defaultdict
from decimal import Decimal

# Avoid wildcard * imports
# Use lexicographically sorted multi-line imports
from test_framework.blocktools import (
    create_block,
    create_coinbase,
)
from test_framework.messages import (
    CInv,
    MSG_BLOCK,
)
from test_framework.p2p import (
    P2PInterface,
    msg_block,
    msg_getdata,
    p2p_lock,
)
from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import (
    assert_equal,
)

# P2PInterface is a class containing callbacks to be executed when a P2P
# message is received from the node-under-test. Subclass P2PInterface and
# override the on_*() methods if you need custom behaviour.
class BaseNode(P2PInterface):
    def __init__(self):
        """Initialize the P2PInterface

        Used to initialize custom properties for the Node that aren't
        included by default in the base class. Be aware that the P2PInterface
        base class already stores a counter for each P2P message type and the
        last received message of each type, which should be sufficient for the
        needs of most tests.

        Call super().__init__() first for standard initialization and then
        initialize custom properties."""
        super().__init__()
        # Stores a dictionary of all blocks received
        self.block_receive_map = defaultdict(int)

    def on_block(self, message):
        """Override the standard on_block callback

        Store the hash of a received block in the dictionary."""
        self.block_receive_map[message.block.hash_int] += 1

    def on_inv(self, message):
        """Override the standard on_inv callback"""
        pass

def custom_function():
    """Do some custom behaviour

    If this function is more generally useful for other tests, consider
    moving it to a module in test_framework."""
    # self.log.info("running custom_function")  # Oops! Can't run self.log outside the BitcoinTestFramework
    pass


class ExampleTest(BitcoinTestFramework):
    # Each functional test is a subclass of the BitcoinTestFramework class.

    # Override the set_test_params(), skip_test_if_missing_module(), add_options(), setup_chain(), setup_network()
    # and setup_nodes() methods to customize the test setup as required.

    def set_test_params(self):
        """Override test parameters for your individual test.
        This method must be overridden and num_nodes must be explicitly set."""
        self.setup_clean_chain = True
        self.num_nodes = 2


    # Use skip_test_if_missing_module() to skip the test if your test requires certain modules to be present.
    # This test uses generate which requires wallet to be compiled
    def skip_test_if_missing_module(self):
        self.skip_if_no_wallet()

    # Use add_options() to add specific command-line options for your test.
    # In practice this is not used very much, since the tests are mostly written
    # to be run in automated environments without command-line options.
    # def add_options()
    #     pass

    # Use setup_chain() to customize the node data directories. In practice
    # this is not used very much since the default behaviour is almost always
    # fine
    # def setup_chain():
    #     pass

    def setup_network(self):
        """Setup the test network topology

        Often you won't need to override this, since the standard network topology
        (linear: node0 <-> node1 <-> node2 <-> ...) is fine for most tests.

        If you do override this method, remember to start the nodes, assign
        them to self.nodes, connect them and then sync."""

        self.setup_nodes()
        self.connect_nodes(0, 1)
        self.sync_all(self.nodes[0:2])

    # Use setup_nodes() to customize the node start behaviour (for example if
    # you don't want to start all nodes at the start of the test).
    # def setup_nodes():
    #     pass

    def custom_method(self):
        """Do some custom behaviour for this test

        Define it in a method here because you're going to use it repeatedly.
        If you think it's useful in general, consider moving it to the base
        BitcoinTestFramework class so other tests can use it."""

        self.log.info("Running custom_method")

    def run_test(self):
        """Main test logic"""
        self.log.info("Setup wallets...")
        self.nodes[0].createwallet(wallet_name="w1")
        w1 = self.nodes[0].get_wallet_rpc("w1")
        addr_w1 = w1.getnewaddress()
        self.nodes[1].createwallet(wallet_name="w2")
        w2 = self.nodes[1].get_wallet_rpc("w2")
        self.log.info("Wallets connected")

        # Generate 101 blocks and reward to w1
        self.generatetoaddress(self.nodes[0], 101, addr_w1)
        assert_equal(w1.getbalance(), Decimal("50.00000000"))
        self.log.info("Wallet 1 with balance")
        
        # Send to addr from w2
        addr_w2 = w2.getnewaddress()
        txid = w1.sendtoaddress(addr_w2, 1)
        self.log.info("BTC sended to w1")

        # Check mempools
        self.sync_mempools()
        entry = self.nodes[0].getmempoolentry(txid)
        assert entry is not None
        assert_equal(self.nodes[1].getrawmempool(), self.nodes[0].getrawmempool())
        self.log.info("Mempool ok")

        assert w1.getbalance() <= Decimal("49.00000000")

        self.generate(self.nodes[0], 1)

        self.sync_mempools()
        mempool_length = len(self.nodes[0].getrawmempool())
        assert mempool_length == 0
        self.log.info("Mempool 2 ok")

        assert_equal(w2.getbalance(), Decimal("1.00000000"))
        

if __name__ == '__main__':
    ExampleTest(__file__).main()
