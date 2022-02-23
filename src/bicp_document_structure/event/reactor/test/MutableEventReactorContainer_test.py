import unittest

from bicp_document_structure.event.P6Event import P6Event
from bicp_document_structure.event.reactor.EventReactor import EventReactor
from bicp_document_structure.event.reactor.MutableEventReactorContainer import MutableEventReactorContainer


class DummyReactor(EventReactor[int]):
    def __init__(self, rid):
        self.rid = rid

    @property
    def id(self) -> str:
        return self.rid

    def react(self, data: int):
        i = data + 1
        print(i)


class MutableEventReactorContainerTest(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.ev1 = P6Event("Ev1", "ev1")
        self.ev2 = P6Event("Ev2", "ev2")
        self.innerMap = dict()
        self.container: MutableEventReactorContainer = MutableEventReactorContainer[int](self.innerMap)
        self.r1 = DummyReactor("1")
        self.r2 = DummyReactor("2")
        self.r3 = DummyReactor("3")

    def test_add(self):
        container = self.container
        reactor = self.r1
        self.assertTrue(container.isEmpty())
        container.addReactor(self.ev1, reactor)
        l = container.getReactorsForEvent(self.ev1)
        self.assertEqual(1, len(l))
        self.assertEqual(reactor, l[0])
        self.assertTrue(container.isNotEmpty())

    def test_addDuplicate(self):
        """test add duplicate reactor to the same event"""
        container = self.container
        reactor = self.r1
        self.assertTrue(container.isEmpty())
        container.addReactor(self.ev1, reactor)
        l = container.getReactorsForEvent(self.ev1)
        self.assertEqual(1, len(l))
        self.assertEqual(reactor, l[0])
        self.assertTrue(container.isNotEmpty())

        container.addReactor(self.ev1, reactor)
        self.assertEqual(1, len(l))
        self.assertEqual(reactor, l[0])

    def test_removeReactorsForEvent(self):
        self.container.addReactor(self.ev1, self.r1)
        self.container.addReactor(self.ev1, self.r2)
        self.container.addReactor(self.ev1, self.r3)

        self.container.addReactor(self.ev2, self.r2)
        self.container.addReactor(self.ev2, self.r3)
        self.container.removeReactorsForEvent(self.ev1)
        r1list = self.container.getReactorsForEvent(self.ev1)
        self.assertEqual(0, len(r1list))
        e2list = self.container.getReactorsForEvent(self.ev2)
        self.assertEqual(2, len(e2list))

    def test_removeReactorById(self):
        self.a()
        self.container.removeReactorById(self.r2.id)
        self.assertTrue(self.r2 not in self.container.getReactorsForEvent(self.ev1))
        self.assertTrue(self.r2 not in self.container.getReactorsForEvent(self.ev2))

    def test_removeReactorByEventAndId(self):
        self.a()
        self.container.removeReactorByEventAndId(self.ev2, self.r2.id)
        self.assertEqual(3, len(self.container.getReactorsForEvent(self.ev1)))
        self.assertEqual(1, len(self.container.getReactorsForEvent(self.ev2)))

        self.container.removeReactorByEventAndId(self.ev2,self.r1.id)
        self.assertEqual(3, len(self.container.getReactorsForEvent(self.ev1)))
        self.assertEqual(1, len(self.container.getReactorsForEvent(self.ev2)))

    def a(self):
        self.container.addReactor(self.ev1, self.r1)
        self.container.addReactor(self.ev1, self.r2)
        self.container.addReactor(self.ev1, self.r3)

        self.container.addReactor(self.ev2, self.r2)
        self.container.addReactor(self.ev2, self.r3)


if __name__ == '__main__':
    unittest.main()
