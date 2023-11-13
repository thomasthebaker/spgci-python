import unittest
import pytest
from spgci.arbflow import Arbflow
from pandas import DataFrame
from typing import cast
from datetime import date


class CrudeArbitrageTest(unittest.TestCase):
    arbflow = Arbflow()

    ## Simple testcase for margins_catalog endpoint
    @pytest.mark.integtest
    def test_simple(self):
        df = self.arbflow.get_margins_catalog(location_id=34, crude_symbol="AAQZB00")
        self.assertGreater(len(df), 1)  # type: ignore

    ## Paging testcase for margins_data endpoint
    @pytest.mark.integtest
    def test_paging(self):
        paged = self.arbflow.get_margins_data(
            frequency_id=3, page_size=100, paginate=True
        )
        df = self.arbflow.get_margins_data(frequency_id=3, paginate=True)
        self.assertEqual(len(df), len(paged))  # type: ignore

    # Simple testcase for arbitrage endpoint
    @pytest.mark.integtest
    def test_arbitrage(self):
        df = cast(
            DataFrame,
            self.arbflow.get_arbitrage(
                margin_id=[229, 1457],
                base_margin_id=330,
                frequency_id=2,
                page_size=100,
            ),
        )
        self.assertGreater(len(df), 1)

    ## Testcase with multiple filters for margins_data endpoint
    @pytest.mark.integtest
    def test_get_margins_data(self):
        df = cast(
            DataFrame,
            self.arbflow.get_margins_data(
                frequency_id=1,
                margin_date=date(2023, 8, 16),
                page_size=100,
            ),
        )
        self.assertGreater(len(df), 1)

    def test_ref(self):
        for t in self.arbflow.RefTypes:
            df = cast(DataFrame, self.arbflow.get_reference_data(type=t))
            self.assertGreater(len(df), 1)