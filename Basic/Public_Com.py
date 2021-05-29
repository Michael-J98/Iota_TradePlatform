from typing import Optional
import redis
import time


class Client():
    """
    A class for instantiating Publish Client or Subscribe Client
    Call self.subscribe before self.publish otherwise msg could be lost

    Important attributions:
        self.sub: bool, make the instance a Subscribe Clinet or not, default=False

    Method Call Example:
        pub = Client()
        sub = Client(sub=True)

        sub.subscribe('w', thread_on=True)
        sub.get_message()  # get None if thread_on=True

        num = pub.publish('w','878')  # msg will be handled instantly
        # CHANNEL[b'w']:b'878'
    """

    def __init__(self, sub: bool = False):

        self.sub = sub
        self.thread_on = None
        self.client = redis.StrictRedis(host='115.159.218.11',
                     port=6379, password='2Wy%sGehG3UAe3mt')

        if self.sub:
            self.client = self.client.pubsub()

        print("Client has started, the connection will be closed if it's no longer active")

    def publish(self, channel: str, msg: str) -> Optional[int]:
        """publish msg to specific channel"""
        if self.sub:
            print('sub client does not support publish msg')
            return None

        rev_num = self.client.publish(channel, msg)
        return rev_num

    def subscribe(self, channel: str, thread_on=False, handler=None) ->\
                Optional[redis.client.PubSubWorkerThread]:
        """
        subscribe one channel once a time
        """
        if not self.sub:
            print('pub client does not support subscribe msg')
            return None

        if thread_on:
            if handler is None:
                handler = self.handler
            self.client.subscribe(**{channel: handler})
            thread = self.client.run_in_thread()
            print('msg of [channel: {}] will be handled by self.handler as soon as recived'.format(channel))
            print('to stop this thread, call thread.stop()')
            return thread

        else:
            self.client.subscribe(channel)
            time.sleep(0.1)
            first_msg = self.client.get_message()
            if first_msg['type'] == 'subscribe':
                print('[channel: {}] has been subscribed, you can call self.get_message when new msg is received'.format(channel.decode()))
            else:
                print('Warning: the format of the 1st msg was unexpected:\n\
                    {}'.format(first_msg))

    def get_message(self) -> Optional[dict]:
        """
        get None or msg like:
        {'pattern': Optional[str], 'type': str, 'channel': bytes, 'data': bytes} 
        """
        msg = self.client.get_message()
        return msg

    def handler(self, message):
        """
        highly recommended to rewrite this method if thread_on=True
        in self.subscribe
        include a global parameter so that you can access the msg
        outside the thread
        """
        # global store
        # store.append(message['data'])
        print('CHANNEL[{}]:{}'.format(message['channel'], message['data']))
