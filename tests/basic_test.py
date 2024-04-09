from unittest import TestCase

from autocontext import Context, auto


class TestContextD(Context[str]):

    @classmethod
    def factory(cls, instance_name: str) -> str:
        return "Super Text"


class TestContextA(Context):
    ...


class TestContextB(Context):
    
    # a variable
    text: str = auto(TestContextD, "super")
    
    text: TestContextA = auto(TestContextA)


class BasicTest(TestCase):

    def test_classes(self):
        a = TestContextB.instance()
        b = TestContextB.instance()
        self.assertEqual(a, b)

        c = TestContextB.instance("new")
        d = TestContextB.instance("new")
        self.assertEqual(c, d)

        self.assertNotEqual(a, c)
        self.assertNotEqual(b, c)
        self.assertNotEqual(a, d)
        self.assertNotEqual(b, d)

        f = TestContextD.instance("wann")
        g = TestContextD.instance("wann")
        self.assertEqual(f, g)

        field = auto(
            TestContextA, "root")
