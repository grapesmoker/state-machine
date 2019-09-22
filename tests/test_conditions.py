from unittest import TestCase

from state_machine.Condition import Condition


class ConditionsTestCase(TestCase):

    def test_parse_data_spec(self):

        condition = Condition('foo.bar.5', None, None)
        self.assertEqual(condition.data_spec, ['foo', 'bar', '5'])

    def test_extract_data_int(self):

        self.assertEqual(Condition._extract_data(5, []), 5)

    def test_extract_data_dict(self):

        data = {'foo': 5}
        self.assertEqual(Condition._extract_data(data, ['foo']), 5)

    def test_extract_data_list(self):

        data = [1, 2, 3]
        self.assertEqual(Condition._extract_data(data, ['1']), 2)

    def test_extract_data_class(self):

        class Foo:
            bar = 5

        data = Foo()
        self.assertEqual(Condition._extract_data(data, ['bar']), 5)

    def test_extract_data_complex1(self):

        data = {'foo': {'bar': [1, 2, 3]}}
        self.assertEqual(Condition._extract_data(data, ['foo', 'bar', '2']), 3)

    def test_extract_data_complex2(self):

        class Foo:
            baz = 5

        data = {'foo': {'bar': [Foo()]}}
        self.assertEqual(Condition._extract_data(data, ['foo', 'bar', '0', 'baz']), 5)

    def test_conditions(self):

        condition1 = Condition('.', 5, '=')
        condition2 = Condition('.', 5, '>=')
        condition3 = Condition('.', 5, '<=')
        condition4 = Condition('.', 5, '<')
        condition5 = Condition('.', 5, '>')
        condition6 = Condition('.', 5, '!=')
        condition7 = Condition('.', 5, lambda x, y: x**2 > y)

        self.assertTrue(condition1.check_condition(5))
        self.assertFalse(condition1.check_condition(10))

        self.assertTrue(condition2.check_condition(5))
        self.assertTrue(condition2.check_condition(6))
        self.assertFalse(condition2.check_condition(4))

        self.assertTrue(condition3.check_condition(5))
        self.assertTrue(condition3.check_condition(4))
        self.assertFalse(condition3.check_condition(6))

        self.assertTrue(condition4.check_condition(4))
        self.assertTrue(condition4.check_condition(3))
        self.assertFalse(condition4.check_condition(5))
        self.assertFalse(condition4.check_condition(6))

        self.assertTrue(condition5.check_condition(6))
        self.assertTrue(condition5.check_condition(7))
        self.assertFalse(condition5.check_condition(5))
        self.assertFalse(condition5.check_condition(4))

        self.assertTrue(condition6.check_condition(6))
        self.assertTrue(condition6.check_condition(7))
        self.assertFalse(condition6.check_condition(5))

        self.assertTrue(condition7.check_condition(3))
        self.assertTrue(condition7.check_condition(4))
        self.assertFalse(condition7.check_condition(2))
        self.assertFalse(condition7.check_condition(1))