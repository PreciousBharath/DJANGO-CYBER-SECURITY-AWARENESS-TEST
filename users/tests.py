from django.test import SimpleTestCase

from .utility.anovamodel import start_proccess
from .utility.chi_square_test import start_chi


class AnalyticsHelpersTests(SimpleTestCase):
    def test_regression_analysis_returns_summary_and_results(self):
        summary, result = start_proccess()

        self.assertIsNotNone(summary)
        self.assertTrue(result)

    def test_chi_square_analysis_returns_results(self):
        data = start_chi()

        self.assertTrue(data)
        self.assertTrue(any('Chi-square Statistic' in row for row in data))
