#!/bin/bash
# Test runner script for the blog application

set -e

echo "=================================="
echo "Blog Application Test Suite"
echo "=================================="
echo ""

# Activate virtual environment
source .venv/bin/activate

echo "Running all tests with coverage..."
echo ""

# Run all tests with coverage
pytest

echo ""
echo "=================================="
echo "Test Results Summary"
echo "=================================="
echo ""
echo "Coverage report has been generated:"
echo "  - Terminal: See above"
echo "  - HTML: Open htmlcov/index.html"
echo "  - XML: coverage.xml"
echo ""
echo "To run specific test types:"
echo "  Unit tests only:       pytest tests/test_auth_service.py tests/test_blog_service.py"
echo "  API tests only:        pytest tests/test_api.py"
echo "  BDD tests only:        pytest tests/test_bdd_*.py"
echo "  With verbose output:   pytest -vv"
echo "  With print statements: pytest -s"
echo ""
