from iota import AsyncIota, Seed, ProposedTransaction
from iota.types import Address
from typing import List
import asyncio
import time


class Node():
    """
    Basic function of a Node including:
        1. generate a new seed
        2. generate a specific number(default 1) of new Tangle addresses
        3. send a list of transactions(target address is included in transaction)
        4. fetch message from a specific Tangle address

    Important attributions:
        self.addresses: list of Address, store all generated addresses
        self.bundles: list of tail_transaction hashes in str type
    Method Call Example:
        # define event loop
        loop = asyncio.get_event_loop()

        # transfer coroutine object into task object
        task = loop.create_task(coroutine object)

        # trigger the task in event loop
        loop.run_until_complete(task)
    """
    def __init__(self, **kwargs):
        self.seed = None  # iota.Seed object
        self.adapter = 'https://nodes.devnet.iota.org:443'  # url str
        self.devnet = True  # Bool

        self.addresses = []  # List[Address]
        self.index = 0  # int
        self.sent_tx_hashes = []  # list of Bundles
        self.bundles = []  # list of Bundles
        self.elapsed = 0
        self.timeout = 120
        self.polling_interval = 5

        # overwrite if the attributions are provided
        for key, value in kwargs.items():
            exec('self.{}={}'.format(key, value))

        # generate a specific seed for the instance
        if self.seed is None:
            self.seed_gen()

        # construct a node connected to the Tangle
        self.api = AsyncIota(
            adapter=self.adapter,
            seed=self.seed,
            devnet=self.devnet,
        )

    def seed_gen(self):
        self.seed = Seed.random()
        assert self.seed is not None, 'fail to generate seed'

    async def address_gen(self, count=1):
        """generate one address from seed by default"""
        response = await self.api.get_new_addresses(index=self.index, count=count)  # Dict
        self.index += 1
        adds = response['addresses']  # list of addresses
        self.addresses.extend(adds)
        return adds  # coroutine object[list of address]

    async def send(self, transactions: List[ProposedTransaction]) -> bool:
        """
        Send a list of transactions as a bundle and monitor their confirmation
        by the network.
        """
        print('Sending bundle...')
        st_response = await self.api.send_transfer(transactions)
        tx_hashes = [tx.hash for tx in st_response['bundle']]
        self.sent_tx_hashes.extend(tx_hashes)
        self.bundles.extend(tx_hashes)

        print('Sent bundle with transactions: ')
        print(*tx_hashes, sep='\n')

        print('Checking confirmation...')
        while len(self.sent_tx_hashes) > 0:
            # Determine if transactions are confirmed
            gis_response = await self.api.get_inclusion_states(self.sent_tx_hashes)

            for i, (tx, is_confirmed) in enumerate(zip(self.sent_tx_hashes, gis_response['states'])):
                if is_confirmed:
                    print('Transaction %s is confirmed.' % tx)
                    # No need to check for this any more
                    del self.sent_tx_hashes[i]
                    del gis_response['states'][i]

            if len(self.sent_tx_hashes) > 0:
                if self.timeout <= self.elapsed:
                    # timeout reached, terminate checking
                    self.elapsed = 0
                    return False  # coroutine object[bool]
                # Show some progress on the screen
                print('.')
                # Put on hold for polling_interval. Non-blocking, so you can
                # do other stuff in the meantime.
                await asyncio.sleep(self.polling_interval)
                self.elapsed = self.elapsed + self.polling_interval

        self.elapsed = 0
        # All transactions in the bundle are confirmed
        return True  # coroutine object[bool]

    async def fetch(self, address):
        """
        Argument:
        address: Address | bundle hash

        Return: unicode string(base64 encoded) | None
        """

        data = []
        while True:
            if self.timeout <= self.elapsed:
                # timeout reached, terminate checking
                print('Found No data or invaild address type:{}, should be iota.types.Address or str, [] will be returned'.format(type(address)))
                self.elapsed = 0
                return []  # coroutine object[bool]

            # if Address object is provided
            if isinstance(address, Address):

                response = await self.api.find_transaction_objects(addresses=[address])

                if not response['transactions']:
                    print('Couldn\'t find data for the given address for now...')
                else:
                    # Iterate over the fetched transaction objects
                    for tx in response['transactions']:
                        # data is in the signature_message_fragment attribute
                        # as trytes, we need to decode it into a unicode string
                        found_data = tx.signature_message_fragment.decode(errors='ignore')
                        found_value = tx.value  # 不想改后面的了，上面只是接收信息的一部分，没有value
                        data.append(found_data)
                    print(f'find data successfully:{data}')
                    self.elapsed = 0
                    return data

            # if bundle hash object is provided
            if isinstance(address, str):

                if len(address) == 81:

                    # assume there is only one bundle under a tail_hash
                    response = await self.api.get_bundles([address])
                    for msg in response['bundles'][0]:
                        data.append(msg.signature_message_fragment.decode(errors='ignore'))
                    if data != []:
                        print(f'find data successfully:{data}')
                        self.elapsed = 0
                        return data

                else:
                    print('invaild bundle hash, the length of hash should be 81, [] will be returned')
                    self.elapsed = 0
                    return data

            # Put on hold for polling_interval. Non-blocking, so you can
            # do other stuff in the meantime.
            await asyncio.sleep(self.polling_interval)
            self.elapsed = self.elapsed + self.polling_interval



def decorator(coroutine):
    """
    a simple method to get return of a coroutine object
    notice: this method is only for result display
            cause it actually doesn't co-route with
            other coroutine objects.[not sure]

    """
    # define event loop
    loop =  asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # transfer coroutine object to task object
    task = loop.create_task(coroutine)
    # trigger task in event loop
    result = loop.run_until_complete(task)
    loop.stop()
    loop.close()
    return result
