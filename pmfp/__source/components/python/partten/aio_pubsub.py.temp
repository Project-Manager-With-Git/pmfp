import abc
from collections import defaultdict
from contextlib import contextmanager


class Publisher:
    """发布订阅模式.

    Exchange是一个发布器,会向所有发送者推送信息.

    protected:
        _subscribers (Set[]):订阅者,必须都有send()方法
    """

    def __init__(self):
        self._subscribers = set()

    def attach(self, subscriber):
        """订阅发布者."""
        self._subscribers.add(subscriber)

    def detach(self, subscriber):
        """取消订阅."""
        self._subscribers.remove(subscriber)

    @contextmanager
    def subscribe(self, *subscribers):
        """使用with语句订阅和取消订阅."""
        for subscriber in subscribers:
            self.attach(subscriber)
        try:
            yield self
        finally:
            for subscriber in subscribers:
                self.detach(subscriber)

    async def notify(self, msg):
        """向订阅者发送消息通知."""
        for subscriber in self._subscribers:
            await subscriber.send(msg)


_publishers = defaultdict(Publisher)


def get_publisher(name: str)->Publisher:
    """获取一个广播器对象.
    
    广播器对象是发布订阅模式的中心.发布订阅模式是一个三方关系

    + 发布者
    + 订阅者
    + 广播器

    广播器在发布者和订阅者之间为这两者解耦

    发布者只要可以直接访问广播器即可;
    订阅者需要都有一个`send`接口用于接收消息,同时需要先订阅广播器.


    使用时订阅者通过

    + 调用广播器的`attach`接口订阅广播器中的内容
    + 使用广播器的`detach`接口取消订阅

    而发布者则通过
    
    + 调用广播器的`notify`接口向所有订阅者发送内容

    本对象还提供了一个上下文管理器来批量地让订阅者订阅和取定广播器

    
    >>> class DisplayMessages:
    ...     def __init__(self):
    ...         self.count = 0
    ...     async def send(self, msg):
    ...         self.count += 1
    ...         print('msg[{}]: {!r}'.format(self.count, msg))

    >>> async def main():
    ...     exc = get_publisher('name')
    ...     task_a, task_b = DisplayMessages(),DisplayMessages()
    ...     with exc.subscribe(task_a, task_b) as ex:
    ...         await ex.notify('msg1')
    ...         await ex.notify('msg2')

    >>> import asyncio
    >>> loop = asyncio.new_event_loop()
    >>> asyncio.set_event_loop(loop)
    >>> loop.run_until_complete(main())
    msg[1]: 'msg1'
    msg[1]: 'msg1'
    msg[2]: 'msg2'
    msg[2]: 'msg2'
    >>> loop.close()

    Args:
        name (str): 可以是任意名字,如果名字未被使用过则会自动创建一个这个名字的广播器对象
    
    Returns:
        Publisher: - 广播器对象

    """

    return _publishers[name]


__all__ = ["get_publisher"]

if __name__ == '__main__':
    import doctest
    doctest.testmod()