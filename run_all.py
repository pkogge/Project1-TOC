#!/usr/bin/env python3

from src.entrypoint import main
from src.graph import run_graphs

result_files = main()     # this now returns the two CSV file paths
run_graphs(result_files)  # plotting