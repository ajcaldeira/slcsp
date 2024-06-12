import os
import unittest
from main_project import Slcsp
import csv


class TestSlcsp(unittest.TestCase):
    """
    Test the Slcsp class.
    """

    def setUp(self) -> None:
        """
        Set up the test environment.
        """
        self.test_dir = os.path.dirname(os.path.abspath(__file__))
        self.zips_path = os.path.join(self.test_dir, "resources", "zips.csv")
        self.plans_path = os.path.join(self.test_dir, "resources", "plans.csv")
        self.slcsp_path = os.path.join(self.test_dir, "resources", "slcsp.csv")
        self.output_path = os.path.join(self.test_dir, "resources", "test_output.csv")
        with open(self.output_path, "w") as f:
            f.write("zipcode,state,county_code\n12345,NY,36001\n")

    def test_read_data(self) -> None:
        """
        Test the read_data method.
        """
        ## Arrange
        slcsp_runner = Slcsp(
            self.zips_path, self.plans_path, self.slcsp_path, self.output_path
        )
        expected_zip_to_rate_area = {
            "12345": "NY1",
            "23456": "CA1",
            "34567": "NY2",
            "45678": "TX1",
            "56789": "TX2",
            "67890": "FL1",
            "99999": "TX3",
        }
        expected_silver_plans = [
            ("NY1", 298.62),
            ("CA1", 421.43),
            ("TX2", 350.00),
            ("FL1", 275.00),
            ("FL1", 375.00),
            ("FL1", 175.00),
            ("TX1", 300.00),
            ("TX1", 200.00),
        ]

        ## Act
        zip_to_rate_area, silver_plans = slcsp_runner.read_data()

        ## Assert
        self.assertEqual(zip_to_rate_area, expected_zip_to_rate_area)
        self.assertEqual(silver_plans, expected_silver_plans)

    def test_read_data_file_not_found(self) -> None:
        """
        Test the read_data method when a file is not found.
        """
        invalid_paths = [
            ("invalid_zips.csv", "valid_plans.csv", "valid_slcsp.csv"),
            ("valid_zips.csv", "invalid_plans.csv", "valid_slcsp.csv"),
            ("valid_zips.csv", "valid_plans.csv", "invalid_slcsp.csv"),
        ]

        for invalid_zips_path, invalid_plans_path, invalid_slcsp_path in invalid_paths:
            with self.subTest(
                invalid_zips_path=invalid_zips_path,
                invalid_plans_path=invalid_plans_path,
                invalid_slcsp_path=invalid_slcsp_path,
            ):
                slcsp_runner = Slcsp(
                    invalid_zips_path,
                    invalid_plans_path,
                    invalid_slcsp_path,
                    self.output_path,
                )
                with self.assertRaises(FileNotFoundError):
                    slcsp_runner.read_data()

    def test_read_data_key_error(self) -> None:
        """
        Test the read_data method when a KeyError is raised.
        """
        ## Arrange
        invalid_zip_file = os.path.join(self.test_dir, "resources", "invalid_zips.csv")
        with open(invalid_zip_file, "w") as f:
            f.write("zipcode,state,county_code\n12345,NY,36001\n")

        slcsp_runner = Slcsp(
            invalid_zip_file, self.plans_path, self.slcsp_path, self.output_path
        )

        ## Act and Assert
        with self.assertRaises(KeyError):
            slcsp_runner.read_data()

        # Clean up
        os.remove(invalid_zip_file)

    def test_create_rate_area_to_rates(self) -> None:
        """
        Test the create_rate_area_to_rates method.
        """
        ## Arrange
        slcsp_runner = Slcsp(
            self.zips_path, self.plans_path, self.slcsp_path, self.output_path
        )
        expected_rate_area_to_rates = {
            "NY1": [298.62],
            "CA1": [421.43],
            "TX2": [350.00],
            "FL1": [275.00, 375.00, 175.00],
            "TX1": [300.00, 200.00],
        }
        ## Act
        _, silver_plans = slcsp_runner.read_data()
        rate_area_to_rates = slcsp_runner.create_rate_area_to_rates(silver_plans)

        ## Assert
        self.assertEqual(rate_area_to_rates, expected_rate_area_to_rates)

    def test_find_second_lowest_rate(self) -> None:
        """
        Test the find_second_lowest_rate method.
        """
        ## Arrange
        slcsp_runner = Slcsp(
            self.zips_path, self.plans_path, self.slcsp_path, self.output_path
        )
        expected_slcsp_rates = {
            "NY1": None,
            "CA1": None,
            "TX2": None,
            "FL1": 275.00,
            "TX1": 300.00,
        }

        ## Act
        _, silver_plans = slcsp_runner.read_data()
        rate_area_to_rates = slcsp_runner.create_rate_area_to_rates(silver_plans)
        slcsp_rates = slcsp_runner.find_second_lowest_rate(rate_area_to_rates)

        ## Assert
        self.assertEqual(slcsp_rates, expected_slcsp_rates)

    def test_assign_slcsp_to_zipcodes(self) -> None:
        """
        Test the assign_slcsp_to_zipcodes method.
        """
        ## Arrange
        slcsp_runner = Slcsp(
            self.zips_path, self.plans_path, self.slcsp_path, self.output_path
        )
        expected_zipcode_to_slcsp = {
            "12345": None,
            "23456": None,
            "34567": None,
            "45678": 300.00,
            "56789": None,
            "67890": 275.00,
            "99999": None,
            "88888": None,
        }

        ## Act
        zip_to_rate_area, silver_plans = slcsp_runner.read_data()
        rate_area_to_rates = slcsp_runner.create_rate_area_to_rates(silver_plans)
        slcsp_rates = slcsp_runner.find_second_lowest_rate(rate_area_to_rates)
        zipcode_to_slcsp = slcsp_runner.assign_slcsp_to_zipcodes(
            zip_to_rate_area, slcsp_rates
        )

        ## Assert
        self.assertEqual(zipcode_to_slcsp, expected_zipcode_to_slcsp)

    def test_output_results(self) -> None:
        """
        Test the output_results method.
        """
        ## Arrange
        slcsp_runner = Slcsp(
            self.zips_path, self.plans_path, self.slcsp_path, self.output_path
        )
        expected_results = {
            "12345": "",
            "23456": "",
            "34567": "",
            "45678": "300.00",
            "56789": "",
            "67890": "275.00",
            "99999": "",
            "88888": "",
        }

        ## Act
        zip_to_rate_area, silver_plans = slcsp_runner.read_data()
        rate_area_to_rates = slcsp_runner.create_rate_area_to_rates(silver_plans)
        slcsp_rates = slcsp_runner.find_second_lowest_rate(rate_area_to_rates)
        zipcode_to_slcsp = slcsp_runner.assign_slcsp_to_zipcodes(
            zip_to_rate_area, slcsp_rates
        )
        slcsp_runner.output_results(zipcode_to_slcsp)

        with open(self.output_path, newline="") as f:
            reader = csv.DictReader(f)
            results = {row["zipcode"]: row["rate"] for row in reader}

        ## Assert
        self.assertEqual(results, expected_results)

    def tearDown(self) -> None:
        """
        Clean up the test environment.
        """
        os.remove(self.output_path)


if __name__ == "__main__":
    unittest.main(verbosity=2)
