import unittest
import pytest
from unittest import mock

from currency import get_total_currency_value, get_currency_value_from_api


class TestCurrency(unittest.TestCase):

    @pytest.mark.base
    def test_currency_positive(self):
        res = get_total_currency_value(
            rate='GBP',
            count=100_000,
            discount=100
       )
        self.assertEqual(res, 1219.62)

    @pytest.mark.base
    def test_currency_negative(self):
        with self.assertRaises(ValueError) as err:
            get_total_currency_value('GBP', 100_000, -1)

    @pytest.mark.api
    def test_currency_with_api(self):
        with mock.patch('currency.get_currency_value_from_api') as mock_currency:
            mock_currency.return_value = 0.0131962
            res = get_total_currency_value(
                rate = 'GBP',
                count = 100_000,
                discount=100
            )
            self.assertEqual(res, 1219.62)

# последний параметр должен возвращать ошибку
# num - стоимость валюты
# output - стоимость в руб с учетом комиссии
@pytest.mark.parametrize("num, output", [(0.0275192, 2651.92), (0.039605, 3860.5), (6.39742056, 639642.056), (0.0275192, 1)])
def test_currency_multiple(num, output):
    assert 100_000*num - 100 == output

# последний параметр должен возвращать ошибку
# rate - название валюты
# output - стоимость валюты
@pytest.mark.parametrize("rate, output", [('AUD', 0.02376019), ('GBP', 0.0131962), ('AMD', 6.39742056), ('BYN', 0)])
def test_currency_multiple_rate(rate, output):
    res = get_currency_value_from_api(rate)
    assert res == output

# последний параметр должен возвращать ошибку
# rate - название валюты
# value - стоимость валюты
# output - стоимость в руб с учетом комиссии
@pytest.mark.parametrize("rate, value, output", [('AUD', 0.02376019, 2276.0190000000002),
                                                 ('GBP', 0.0131962, 1219.62),
                                                 ('AMD', 6.39742056, 639642.056),
                                                 ('BYN', 0, -1)])
def test_currency_multiple_rate_value(rate, value, output):
    res = get_currency_value_from_api(rate)
    assert (res == value) & (100_000 * res - 100 == output)


# ------ TESTS RESULTS ------

# pytest -m base -v
# test_currency.py::TestCurrency::test_currency_negative PASSED
# test_currency.py::TestCurrency::test_currency_positive PASSED

# pytest -m api -v
# test_currency.py::TestCurrency::test_currency_with_api PASSED

# pytest -v
# test_currency.py::TestCurrency::test_currency_negative PASSED
# test_currency.py::TestCurrency::test_currency_positive PASSED
# test_currency.py::TestCurrency::test_currency_with_api PASSED

# test_currency.py::test_currency_multiple[0.0275192-2651.92] PASSED
# test_currency.py::test_currency_multiple[0.039605-3860.5] PASSED
# test_currency.py::test_currency_multiple[6.39742056-639642.056] PASSED
# test_currency.py::test_currency_multiple[0.0275192-1] FAILED

# test_currency.py::test_currency_multiple_rate[AUD-0.02376019] PASSED
# test_currency.py::test_currency_multiple_rate[GBP-0.0131962] PASSED
# test_currency.py::test_currency_multiple_rate[AMD-6.39742056] PASSED
# test_currency.py::test_currency_multiple_rate[BYN-0] FAILED

# test_currency.py::test_currency_multiple_rate_value[AUD-0.02376019-2276.0190000000002] PASSED
# test_currency.py::test_currency_multiple_rate_value[GBP-0.0131962-1219.62] PASSED
# test_currency.py::test_currency_multiple_rate_value[AMD-6.39742056-639642.056] PASSED
# test_currency.py::test_currency_multiple_rate_value[BYN-0--1] FAILED
