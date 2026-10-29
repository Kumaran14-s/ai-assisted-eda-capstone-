import sys
import unittest
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from eda_utils import data_quality_summary, clean_dataframe, outlier_summary

class TestEDAUtils(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            "value": [1.0, 2.0, None, 2.0, 100.0],
            "label": [" a ", "b", "c", "b", "d"]
        })

    def test_quality_summary_counts_missing(self):
        result = data_quality_summary(self.df).set_index("column")
        self.assertEqual(result.loc["value", "missing_count"], 1)
        self.assertEqual(result.loc["value", "unique_values"], 3)

    def test_cleaning_does_not_mutate_original(self):
        cleaned, log = clean_dataframe(self.df, trim_text=True)
        self.assertEqual(self.df.loc[0, "label"], " a ")
        self.assertEqual(cleaned.loc[0, "label"], "a")
        self.assertEqual(log["Output rows"], len(self.df))

    def test_drop_duplicates(self):
        cleaned, log = clean_dataframe(self.df, drop_duplicates=True)
        self.assertEqual(log["Duplicate rows removed"], 1)
        self.assertEqual(len(cleaned), 4)

    def test_median_imputation(self):
        cleaned, _ = clean_dataframe(self.df, missing_action="Fill numeric missing values with median")
        self.assertFalse(cleaned["value"].isna().any())
        self.assertEqual(cleaned.loc[2, "value"], 2.0)

    def test_outlier_summary(self):
        result = outlier_summary(self.df).set_index("column")
        self.assertEqual(result.loc["value", "potential_outliers"], 1)

    def test_empty_dataframe(self):
        result = data_quality_summary(pd.DataFrame(columns=["a"]))
        self.assertEqual(result.loc[0, "missing_percent"], 0.0)

if __name__ == "__main__":
    unittest.main()
