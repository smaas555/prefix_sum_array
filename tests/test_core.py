import math
import unittest

from prefix_sum_array import PrefixSumArray


class TestConstruction(unittest.TestCase):
    def test_empty(self):
        psa = PrefixSumArray([])
        self.assertEqual(len(psa), 0)
        self.assertEqual(psa.total(), 0.0)

    def test_default_construct_is_empty(self):
        psa = PrefixSumArray()
        self.assertEqual(len(psa), 0)
        self.assertEqual(psa.total(), 0.0)

    def test_single_element(self):
        psa = PrefixSumArray([42])
        self.assertEqual(len(psa), 1)
        self.assertEqual(psa.total(), 42.0)
        self.assertEqual(psa.range_sum(0, 1), 42.0)

    def test_accepts_any_iterable(self):
        # A generator is not a sequence; the implementation must consume it
        # rather than index into it.
        def gen():
            for v in (1, 2, 3):
                yield v

        psa = PrefixSumArray(gen())
        self.assertEqual(psa.range_sum(0, 3), 6.0)


class TestRangeSum(unittest.TestCase):
    def test_whole_range(self):
        psa = PrefixSumArray([1, 2, 3, 4, 5])
        self.assertEqual(psa.range_sum(0, 5), 15.0)

    def test_subrange(self):
        psa = PrefixSumArray([1, 2, 3, 4, 5])
        self.assertEqual(psa.range_sum(1, 4), 9.0)
        self.assertEqual(psa.range_sum(2, 3), 3.0)

    def test_empty_range_is_zero(self):
        psa = PrefixSumArray([1, 2, 3])
        self.assertEqual(psa.range_sum(2, 2), 0.0)
        self.assertEqual(psa.range_sum(0, 0), 0.0)

    def test_negative_index_counts_from_end(self):
        psa = PrefixSumArray([10, 20, 30, 40, 50])
        # Python slice: arr[-2:] == [40, 50]
        self.assertEqual(psa.range_sum(-2, 5), 90.0)
        # arr[1:-1] == [20, 30, 40]
        self.assertEqual(psa.range_sum(1, -1), 90.0)

    def test_out_of_range_clamps(self):
        psa = PrefixSumArray([1, 2, 3])
        self.assertEqual(psa.range_sum(-100, 100), 6.0)
        self.assertEqual(psa.range_sum(10, 20), 0.0)
        self.assertEqual(psa.range_sum(-10, -10), 0.0)

    def test_reversed_bounds_returns_zero(self):
        # start > end after clamping: no elements in the range, so zero.
        psa = PrefixSumArray([1, 2, 3])
        self.assertEqual(psa.range_sum(3, 0), 0.0)

    def test_negatives_in_data(self):
        psa = PrefixSumArray([-1, 2, -3, 4, -5])
        self.assertEqual(psa.total(), -3.0)
        self.assertEqual(psa.range_sum(0, 3), -2.0)
        self.assertEqual(psa.range_sum(2, 5), -4.0)

    def test_floats_handled_without_integer_loss(self):
        psa = PrefixSumArray([0.1, 0.2, 0.3])
        result = psa.range_sum(0, 3)
        # Compare with tolerance; the prefix stores doubles so we check the
        # accumulated value is within one ULP-scale of the naive sum.
        self.assertTrue(math.isclose(result, 0.6, rel_tol=1e-12, abs_tol=1e-12))


class TestTypeSafety(unittest.TestCase):
    def test_float_index_rejected(self):
        psa = PrefixSumArray([1, 2, 3])
        with self.assertRaises(TypeError):
            psa.range_sum(0.0, 3)

    def test_bool_index_rejected(self):
        # bool is a subclass of int but accepting True/False as 1/0 here would
        # be a silent footgun, so we reject it explicitly.
        psa = PrefixSumArray([1, 2, 3])
        with self.assertRaises(TypeError):
            psa.range_sum(True, 3)

    def test_string_index_rejected(self):
        psa = PrefixSumArray([1, 2, 3])
        with self.assertRaises(TypeError):
            psa.range_sum("0", 3)


class TestLenAndTotal(unittest.TestCase):
    def test_len_tracks_source(self):
        psa = PrefixSumArray([7, 8, 9, 10])
        self.assertEqual(len(psa), 4)

    def test_total_matches_naive_sum(self):
        data = [5, -5, 5, -5, 10]
        psa = PrefixSumArray(data)
        self.assertEqual(psa.total(), float(sum(data)))


if __name__ == "__main__":
    unittest.main()
