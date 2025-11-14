"""Test cases for Bin Packing Backtracking"""
import pytest
import os
from src.bin_packing_LANK import BinPacking

def test_all_data():
    """Test all data from consolidated file"""
    test_file = os.path.join(os.path.dirname(__file__), "test_data_LANK.txt")
    packer = BinPacking(test_file, result_file_name="test_results")
    
    print(f"\nTesting {len(packer.solution_instances)} instances")
    
    for i, instance in enumerate(packer.solution_instances):
        result = packer.binpacking_backtracing(instance[0], instance[1:])
        print(f"Instance {i}: {len(instance[1:])} items, {len(result)} solutions")
        for sol in result:
            assert sum(sol) == instance[0]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])

