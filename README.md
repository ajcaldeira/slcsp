# SLCSP

## How to run manually

#### Arguments
```
options:
  -h, --help       show this help message and exit
  --zips ZIPS      Path to the zips.csv file
  --plans PLANS    Path to the plans.csv file
  --slcsp SLCSP    Path to the slcsp.csv file
  --output OUTPUT  Path to the output file [DEFAULT=slcsp.csv]
```
#### Example Command
```
python main.py --zips zips.csv --plans plans.csv --slcsp slcsp.csv --output output.csv
```

## Testing

#### Command

```
python -m unittest tests/test_slcsp.py
```
## How to run with Makefile

#### Run the project
```
make run-me
```
This uses the command: `python main.py --zips data/zips.csv --plans data/plans.csv --slcsp data/slcsp.csv --output data/output.csv`

#### Run unit test
```
make unit-test
```

#### Run pre-commit
```
make pre-commit
```

## Additional Notes

I have not used Poetry in this project - I think it may have been out of scope as I am not using any (excluding pre-commit) external libraries. Poetry is my preference when building projects.

I have opted to use unittest over pytest. However, pytest is my preference. The reason for using unittest is to minimize the number of external libraries as per the instructions. Usually I would like to be using pytest - I find it easier and more convenient. Additionally, coverage is very helpful (which is not included in this project), especially in larger projects.
