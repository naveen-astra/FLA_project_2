#!/usr/bin/env python3
"""
Test runner for DFA Minimizer Web Application
"""

import os
import sys
import unittest

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_tests():
    """Run all unit tests"""
    
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = os.path.join(os.path.dirname(__file__), 'tests')
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code based on test results
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    print("Running DFA Minimizer Test Suite...")
    print("=" * 50)
    
    exit_code = run_tests()
    
    print("=" * 50)
    if exit_code == 0:
        print("All tests passed! ✅")
    else:
        print("Some tests failed! ❌")
    
    sys.exit(exit_code)
