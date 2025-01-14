# CircleCI API Python Client

A simple Python client for interacting with the CircleCI API.

## Installation

You can install the package using `pip`:

```bash
pip install circleci-api-python
```

## Requirements

This package requires Python 3.8 or higher.

All the dependencies are listed in the `requirements.txt` file are installed automatically when you install the package.


## Usage

### Initialization

To use the CircleCI API Python client, you need to initialize it with your CircleCI token:

```python
from circleci_api_python.client import CircleCI

client = CircleCI(token="your_circleci_token")
```

## Development

### Running Unit Tests

To run the unit tests, you can use the provided shell script:

```bash
./run_unit_tests.sh
```

Alternatively, you can run the tests using `unittest` directly:

```bash
python -m unittest discover -s tests
```

### Running Linting Checks

To run the linting checks, you can use the provided shell script:

```bash
./run_linting_checks.sh
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
