import csv
import argparse


class Slcsp:
    """
    Slcp class to calculate the second lowest cost silver plan for each zipcode.

    """

    def __init__(self, zips: str, plans: str, slcsp: str, output: str) -> None:
        """
        Initialize the slcsp class with the file paths for zips, plans, and slcsp.

        Args:
            zips (str): Path to the zips.csv file.
            plans (str): Path to the plans.csv file.
            slcsp (str): Path to the slcsp.csv file.
        """
        self.zips: str = zips
        self.plans: str = plans
        self.slcsp: str = slcsp
        self.output: str = output

    def read_data(self) -> tuple[dict[str, str], list[tuple[str, float]]]:
        """
        Read the data from the zips, plans, and slcsp files.

        Returns:
            zip_to_rate_area (dict[str, str]): A mapping of zipcodes to rate areas.
            silver_plans (list[tuple[str, float]]): A list of tuples containing the rate area and rate for silver plans.
        """
        ## First, read the zips.csv file and create a mapping of zipcodes to rate areas.
        try:
            with open(self.zips, newline="") as f:
                reader = csv.DictReader(f)
                zip_to_rate_area = {
                    row["zipcode"]: f"{row['state']}{row['rate_area']}"
                    for row in reader
                }
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Error: zips.csv file not found: {e}")
        except KeyError as e:
            raise KeyError(f"Error: zips.csv file is missing required columns: {e}")

        ## Next, read the plans.csv file and extract the silver plans.
        try:
            with open(self.plans, newline="") as f:
                reader = csv.DictReader(f)
                silver_plans = []
                for row in reader:
                    if row["metal_level"] == "Silver":
                        state = row["state"]
                        rate_area = row["rate_area"]
                        rate = float(row["rate"])
                        key = f"{state}{rate_area}"
                        silver_plans.append((key, rate))
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Error: plans.csv file not found: {e}")
        except KeyError as e:
            raise KeyError(f"Error: plans.csv file is missing required columns {e}")

        ## Finally, read the slcsp.csv file and extract the zipcodes.
        try:
            with open(self.slcsp, newline="") as f:
                reader = csv.DictReader(f)
                self.slcsp_zipcodes = [row["zipcode"] for row in reader]
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Error: plans.csv file not found: {e}")
        except KeyError as e:
            raise KeyError(f"Error: plans.csv file is missing required columns {e}")

        return zip_to_rate_area, silver_plans

    def create_rate_area_to_rates(
        self, silver_plans: list[tuple[str, float]]
    ) -> dict[str, list]:
        """
        Create a mapping of rate areas to rates.

        Args:
            silver_plans (list[tuple[str, float]): A list of tuples containing the rate area and rate for silver plans.

        Returns:
            rate_area_to_rates (dict[str, list]): A mapping of rate areas to rates.
        """
        rate_area_to_rates: dict[str, list] = {}
        ## Loop over the silver plans and create a mapping of rate areas to rates.
        for state_rate_area, rate in silver_plans:
            ## If the rate area is not in the dictionary, add it with the rate as a list.
            if rate_area_to_rates.get(state_rate_area) is None:
                rate_area_to_rates[state_rate_area] = [rate]
            else:
                rate_area_to_rates[state_rate_area].append(rate)
        return rate_area_to_rates

    def find_second_lowest_rate(
        self, rate_area_to_rates: dict[str, list]
    ) -> dict[str, float | None]:
        """
        Find the second lowest unique rate for each rate area.

        Args:
            rate_area_to_rates (dict[str, list]): A mapping of rate areas to rates.

        Returns:
            slcsp_rates (dict[str, float]): A dictionary with rate areas as keys and the second lowest rate as values.
        """
        slcsp_rates: dict[str, float | None] = {}
        ## Loop over the rate areas and find the second lowest unique rate.
        for rate_area, rates in rate_area_to_rates.items():
            ## Sort the rates and get the unique rates using a set.
            unique_rates = sorted(set(rates))
            if len(unique_rates) > 1:
                slcsp_rates[rate_area] = unique_rates[1]
            else:
                slcsp_rates[rate_area] = None
        return slcsp_rates

    def assign_slcsp_to_zipcodes(
        self, zip_to_rate_area: dict[str, str], slcsp_rates: dict[str, float | None]
    ) -> dict[str, float | None]:
        """
        Assign SLCSP to ZIP codes.

        Args:
            zip_to_rate_area (dict[str, str]): A mapping of zipcodes to rate areas.
            slcsp_rates (dict[str, float | None]): A dictionary with rate areas as keys and the second lowest rate as values.

        Returns:
            zipcode_to_slcsp (dict[str, float | None]): A mapping of zipcodes to the SLCSP rates.
        """
        zipcode_to_slcsp: dict[str, float | None] = {}
        for zipcode in self.slcsp_zipcodes:
            ## Get the rate area for the zipcode.
            rate_area = zip_to_rate_area.get(zipcode)
            ## If the rate area is in the SLCSP rates, assign the rate, otherwise assign None.
            if rate_area in slcsp_rates:
                zipcode_to_slcsp[zipcode] = slcsp_rates[rate_area]
            else:
                zipcode_to_slcsp[zipcode] = None
        return zipcode_to_slcsp

    def output_results(self, zipcode_to_slcsp: dict[str, float | None]) -> None:
        """
        Output the results to a CSV file.

        Args:
            zipcode_to_slcsp (dict[str, float | None]): A mapping of zipcodes to the SLCSP rates.

        Returns:
            None
        """
        with open(self.output, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["zipcode", "rate"])
            for zipcode in self.slcsp_zipcodes:
                rate = zipcode_to_slcsp[zipcode]
                if rate is not None:
                    ## Format the rate to 2dp.
                    formatted_rate = f"{rate:.2f}"
                else:
                    formatted_rate = ""
                writer.writerow([zipcode, formatted_rate])
        print(f"SLCSP calculation completed. Results are saved in '{self.output}'.")

    def run(self) -> None:
        """
        Run the SLCSP calculation.

        """
        zip_to_rate_area, silver_plans = self.read_data()
        rate_area_to_rates = self.create_rate_area_to_rates(silver_plans)
        slcsp_rates = self.find_second_lowest_rate(rate_area_to_rates)
        zipcode_to_slcsp = self.assign_slcsp_to_zipcodes(zip_to_rate_area, slcsp_rates)
        self.output_results(zipcode_to_slcsp)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Calculate the SLCSP for each zipcode."
    )
    parser.add_argument("--zips", type=str, help="Path to the zips.csv file")
    parser.add_argument("--plans", type=str, help="Path to the plans.csv file")
    parser.add_argument("--slcsp", type=str, help="Path to the slcsp.csv file")
    parser.add_argument(
        "--output", type=str, default="slcsp.csv", help="Path to the output file"
    )

    args = parser.parse_args()

    runner = Slcsp(args.zips, args.plans, args.slcsp, args.output)
    runner.run()
