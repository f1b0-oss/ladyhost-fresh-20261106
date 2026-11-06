import unittest

from stream_statistics import mean


class MeanTests(unittest.TestCase):
    def test_integer_values(self):
        self.assertEqual(mean([1, 2, 3]), 2)
        self.assertEqual(mean([1, 2]), 1.5)

    def test_float_and_mixed_values(self):
        self.assertAlmostEqual(mean([0.1, 0.2, 0.3]), 0.2)
        self.assertEqual(mean([1, 2.5, 4]), 2.5)

    def test_negative_values_and_zero(self):
        self.assertEqual(mean([-6, -3, 0]), -3)
        self.assertEqual(mean([-2, 0, 2]), 0)

    def test_single_value(self):
        for value in (0, -7, 2.5):
            with self.subTest(value=value):
                self.assertEqual(mean([value]), value)

    def test_empty_inputs(self):
        for values in ([], iter(()), (value for value in ())):
            with self.subTest(values=values):
                with self.assertRaises(ValueError):
                    mean(values)

    def test_generator(self):
        values = (value for value in [1, -2, 4, 7])
        self.assertEqual(mean(values), 2.5)
        self.assertEqual(list(values), [])

    def test_iterable_is_consumed_only_once_without_length(self):
        class SinglePass:
            def __init__(self):
                self.started = False

            def __iter__(self):
                if self.started:
                    raise AssertionError("iterated twice")
                self.started = True
                yield from (2, 4, 9)

            def __len__(self):
                raise AssertionError("length requested")

        self.assertEqual(mean(SinglePass()), 5)

    def test_non_finite_values(self):
        for value in (float('inf'), float('-inf'), float('nan')):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    mean(item for item in (1, value))

    def test_unsupported_types(self):
        for value in ('2', None, 1j, True, False):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    mean([1, value])

    def test_large_finite_values_do_not_overflow_intermediate_sum(self):
        self.assertEqual(mean([1e308, 1e308]), 1e308)
        self.assertEqual(mean([10 ** 400, 10 ** 400]), 10 ** 400)

    def test_cancellation_retains_small_values(self):
        self.assertEqual(mean([1e16, 1, -1e16]), 1 / 3)


if __name__ == '__main__':
    unittest.main()
