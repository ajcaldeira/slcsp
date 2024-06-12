from slcsp import Slcsp
import argparse

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
