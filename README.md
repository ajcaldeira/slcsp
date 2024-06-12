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
python main_project.py --zips zips.csv --plans plans.csv --slcsp slcsp.csv --output output.csv
```

## Testing

#### Command

```
python -m unittest tests/tests.py
```
## How to run with Makefile

#### Run the project
```
make run-me
```
This uses the command: `python main_project.py --zips data/zips.csv --plans data/plans.csv --slcsp data/slcsp.csv --output data/output.csv`

#### Run unit test
```
make unit-test
```

#### Run pre-commit
```
make pre-commit
```
