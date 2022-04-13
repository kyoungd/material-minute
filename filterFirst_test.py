from unittest import mock, TestCase
from filterFirst import FilterFirst
import pandas as pd


class TestFilterFirst(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def dataSetup(self, price, isFirstMin, p0, p1, p2, p3, p4, p5, v0, v1, v2, v3, v4, v5):
        data = {'Date':
                ['2021-01-07T00:00:00.000000000', '2021-02-01T00:00:00.000000000',
                 '2021-03-12T00:00:00.000000000', '2021-04-23T00:00:00.000000000',
                 '2021-05-28T00:00:00.000000000', '2021-09-01T00:00:00.000000000'],
                'Close':
                    [p0, p1, p2,
                     p3, p4, p5],
                'Volume':
                    [v0, v1, v2,
                    v3, v4, v5],
                'High':
                    [p0+1, p1+1, p2+1,
                     p3+1, p4+1, p5+1],
                'Low':
                    [p0-1, p1-1, p2-1,
                     p3-1, p4-1, p5-1],
                'Open':
                    [p0-0.5, p1-0.5, p2-0.5,
                     p3-0.5, p4-0.5, p5-0.5]
                }
        df = pd.DataFrame(data)
        app = FilterFirst()
        result = app.IsFilter("TEST", df)
        return result

    def test_PriceFilter(self):
        result = self.dataSetup(100.1, False, 4, 10, 15, 20, 25, 30, 200000, 200000, 200000, 200000, 200000, 200000)
        self.assertEqual(result, True)
