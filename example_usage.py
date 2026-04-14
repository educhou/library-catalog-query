#!/usr/bin/env python3
"""
Example usage of the catalog_lookup CLI.
Demonstrates looking up book metadata by ISBN.
"""

import subprocess
import sys

# Example ISBN from the earlier catalog lookup
EXAMPLE_ISBN = "978-0-12-345678-9"

# Real ISBN examples for testing (these exist in Open Library)
TEST_ISBNS = [
    "978-0-596-00712-6",  # Learning Python
    "978-0-134-68599-1",  # Clean Code
    "0-262-23253-7",      # Introduction to Algorithms (ISBN-10)
]

def lookup_book(isbn: str):
    """Look up a book by ISBN using the catalog_lookup tool."""
    print(f"\n{'='*60}")
    print(f"Looking up ISBN: {isbn}")
    print('='*60)
    
    try:
        result = subprocess.run(
            ["python", "catalog_lookup.py", isbn],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("Warnings/Errors:", file=sys.stderr)
            print(result.stderr, file=sys.stderr)
        
        return result.returncode == 0
    
    except subprocess.TimeoutExpired:
        print("Error: Lookup timed out", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return False


def main():
    print("Catalog Lookup CLI - Example Usage")
    print("==================================\n")
    
    # Example 1: The ISBN from the earlier historian question
    print("Example 1: ISBN from earlier question")
    lookup_book(EXAMPLE_ISBN)
    
    # Example 2: Try some real ISBNs
    print("\n\nExample 2: Testing with real ISBNs from Open Library")
    success_count = 0
    for isbn in TEST_ISBNS:
        if lookup_book(isbn):
            success_count += 1
    
    print(f"\n\n{'='*60}")
    print(f"Results: {success_count}/{len(TEST_ISBNS)} lookups successful")
    print('='*60)


if __name__ == "__main__":
    main()
