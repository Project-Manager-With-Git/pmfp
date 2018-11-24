import abc
import asyncio


class ActorExit(Exception):
    pass


class ActorClosing(Exception):
    pass


class InboxFull(Exception):
    pass


class ActorMixinAbc(abc.ABC):
    """actor模型的混入基类.

    actor模型是一个并发模型,它通过自己维护一个邮箱来接收消息执行操作.
    将其定义为Mixin是因为它是一种行为模式,可以嵌入其他类中.满足下面的接口都可以是actor.

    通常actor模型不会单独使用,而是结合发布订阅模式做广播,结合中介模式做点对点通信.

    使用方法:

    >>> class Pinger(ActorMixinAbc):
    ...     async def receive(self, message):
    ...         print(message)
    ...         try:
    ...             await pong.send('ping')
    ...         except ActorClosing:
    ...             print("pong is closing")
    ...         except Exception as e:
    ...             raise e
    ...         await asyncio.sleep(0.5)

    >>> class Ponger(ActorMixinAbc):
    ...     async def receive(self, message):
    ...         print(message)
    ...         try:
    ...             await ping.send('pong')
    ...         except ActorClosing:
    ...             print("ping is closing")
    ...         except Exception as e:
    ...             raise e
    ...         await asyncio.sleep(0.5)

    >>> async def run():
    ...     ping.send_nowait('start')
    ...     ping.run()
    ...     pong.run()
    ...     await asyncio.sleep(3)
    ...     await ping.close()
    ...     await pong.close()

    >>> loop = asyncio.new_event_loop()
    >>> ping = Pinger(loop=loop)
    >>> pong = Ponger(loop=loop)
    >>> asyncio.set_event_loop(loop)
    >>> loop.run_until_complete(run())
    start
    ping
    pong
    ping
    pong
    ping
    pong
    ping
    pong
    ping
    pong
    ping
    >>> loop.close()

    publish:
        inbox (asyncio.Queue): 邮箱,即队列
        running (bool):状态标明是否在执行

    protected:
        _actor_task (asyncio.Task): ensure_future后的协程任务.


    abcmethod:
        receive (corfunc): 接收信息后的处理过程
    """

    def __init__(self, maxsize=10, loop:asyncio.AbstractEventLoop=None):
        """初始化一个actor.

        Args:

            maxsize (int, optional): Defaults to 10. 邮箱的最大长度
            loop (AbstractEventLoop, optional): Defaults to None. 事件循环
        """

        self.loop = loop or asyncio.get_event_loop()
        self.inbox = asyncio.Queue(maxsize=maxsize, loop=self.loop)
        self.running = False
        self.closing = False
        self._actor_task = None

    def send_nowait(self, msg):
        """立即将消息发送到邮箱."""
        try:
            self.inbox.put_nowait(msg)
        except asyncio.queues.QueueFull as qf:
            raise InboxFull("邮箱满了")

    async def send(self, msg):
        """使用异步接口向自己的邮箱发送消息."""
        if self.closing is True:
            raise ActorClosing("is closing, no recive new message any more")
        else:
            try:
                await self.inbox.put(msg)
            except asyncio.queues.QueueFull as qf:
                raise InboxFull("邮箱满了")

    async def send_until_success(self, msg):
        """发送消息直到消息被接收."""
        while True:
            try:
                await self.send(msg)
            except InboxFull as full:
                continue
            except Exception as e:
                raise e
            else:
                break

    async def close(self):
        """关闭actor协程.注意不是立刻关闭,而是将队列中都执行完毕再关闭."""
        await self.send_until_success(ActorExit)
        self.closing = True

    async def handle_timeout(self):
        """操作过时时的钩子."""
        pass

    async def process(self):
        """执行actor的过程."""
        self.running = True
        while self.running:
            try:
                message = await self.inbox.get()
            except asyncio.TimeoutError:
                await self.handle_timeout()
            except asyncio.queues.QueueEmpty:
                continue
            else:
                if message is ActorExit:
                    print("actor closed")
                    self.running = False
                    asyncio.Task.current_task().cancel()
                    #raise ActorExit()
                else:
                    await self.receive(message)

    def run(self):
        """将actor做为一个协程独立执行."""
        self._actor_task = asyncio.ensure_future(self.process())

    @abc.abstractmethod
    async def receive(self, message):
        """需要实现的receive方法."""
        raise NotImplemented()


__all__ = ["ActorMixinAbc"]

if __name__ == '__main__':
    import doctest
    doctest.testmod()
