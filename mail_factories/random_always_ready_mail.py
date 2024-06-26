import typing
import random
import simpy
import simpy.resources.store

from mail_factories.mail_factory import MailFactory
from structures import Mail


class RandomAlwaysReadyMail(MailFactory):
    def __init__(self, env: simpy.Environment,
                 destination: typing.Callable[[], int] | typing.Sequence[int]):
        super().__init__(env)
        if isinstance(destination, typing.Callable):
            self._destination = destination
        else:
            self._destination = lambda: random.choice(destination)
        self._last_id = 0

    @typing.override
    def __call__(self, input_id: int):
        return lambda: self._get_mail(input_id)

    def _get_mail(self, input_id: int):
        temp = random.randint(0, 2)
        self._stores[input_id].put(Mail(self._last_id, temp))
        self._last_id += 1
        return self._stores[input_id].get()

    @typing.override
    def _putter(self):
        yield self._env.timeout(0)

