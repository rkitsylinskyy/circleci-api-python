#!/bin/bash

# Run pylint on all Python files in the repository
pylint $(git ls-files '*.py')