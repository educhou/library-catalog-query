#!/usr/bin/env python3
"""
Historian's Guide - Using Catalog Lookup for Historical Research
Demonstrates answering historical questions using catalog metadata.
"""

import subprocess
import sys
import json
from typing import Dict, Any, Optional


def query_book(isbn: str) -> Optional[Dict[str, Any]]:
    """Query catalog for book metadata and return as dict."""
    result = subprocess.run(
        ["python", "catalog_lookup.py", isbn],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    if result.returncode != 0:
        return None
    
    # Parse the output into a dictionary
    catalog = {}
    for line in result.stdout.strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            catalog[key.strip()] = value.strip()
    
    return catalog


def answer_historical_question(question: str, isbn: str) -> str:
    """
    Answer a historical question using catalog metadata.
    Historian methodology: base answer on primary catalog sources.
    """
    print(f"\nHistorical Research Query")
    print("="*70)
    print(f"Question: {question}")
    print(f"ISBN: {isbn}")
    print("="*70)
    
    catalog = query_book(isbn)
    
    if not catalog:
        return f"Error: Could not retrieve catalog data for ISBN {isbn}"
    
    # Build historian-style response using catalog fields
    response = []
    
    if catalog.get('Title') and catalog['Title'] != 'Not available':
        response.append(f"Work: {catalog['Title']}")
    
    if catalog.get('Publisher') and catalog['Publisher'] != 'Not available':
        response.append(f"Publisher: {catalog['Publisher']}")
    
    if catalog.get('Publication Date') and catalog['Publication Date'] != 'Not available':
        response.append(f"Date of Publication: {catalog['Publication Date']}")
    
    if catalog.get('Subject') and catalog['Subject'] != 'Not available':
        response.append(f"\nHistorical Subject(s): {catalog['Subject']}")
        response.append("\nInterpretation: Based on the catalog metadata, this work")
        response.append(f"addresses the following historical topics: {catalog['Subject']}")
    
    if catalog.get('Abstract') and catalog['Abstract'] != 'Not available':
        response.append(f"\nAbstract: {catalog['Abstract']}")
    
    response.append(f"\nCatalog Identifier: ISBN {catalog.get('ISBN', 'Unknown')}")
    
    return "\n".join(response)


def main():
    print("HISTORIAN'S GUIDE TO CATALOG LOOKUPS")
    print("====================================\n")
    
    # Example 1: Aviation history question
    print("\nEXAMPLE 1: Subject-based historical inquiry")
    answer1 = answer_historical_question(
        "What is the subject of the book with ISBN 978-0-12-345678-9?",
        "978-0-12-345678-9"
    )
    print(answer1)
    
    # Example 2: Real book example
    print("\n\n" + "="*70)
    print("\nEXAMPLE 2: Technology history research")
    answer2 = answer_historical_question(
        "What historical topics does this book cover?",
        "978-0-596-00712-6"
    )
    print(answer2)
    
    # Example 3: Using ISBN-10
    print("\n\n" + "="*70)
    print("\nEXAMPLE 3: Classic algorithms work (ISBN-10 format)")
    answer3 = answer_historical_question(
        "What is documented about algorithm development?",
        "0-262-23253-7"
    )
    print(answer3)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
