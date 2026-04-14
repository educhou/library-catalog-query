#!/usr/bin/env python3
"""
Catalog Lookup CLI - Look up book metadata by ISBN.
Uses Open Library API as primary source.
"""

import json
import sys
import urllib.request
import urllib.error
from typing import Optional, Dict, Any


def validate_isbn(isbn: str) -> str:
    """
    Validate and auto-correct ISBN-10/13 checksums.
    Returns corrected ISBN or raises ValueError if invalid format.
    """
    # Remove hyphens and spaces
    isbn_clean = isbn.replace("-", "").replace(" ", "")
    
    if len(isbn_clean) == 10:
        return validate_isbn10(isbn_clean)
    elif len(isbn_clean) == 13:
        return validate_isbn13(isbn_clean)
    else:
        raise ValueError(f"Invalid ISBN length: {len(isbn_clean)}. Expected 10 or 13 digits.")


def validate_isbn10(isbn: str) -> str:
    """Validate and correct ISBN-10 checksum."""
    if not isbn[:9].isdigit():
        raise ValueError(f"Invalid ISBN-10 format: {isbn}")
    
    # Calculate correct checksum
    total = sum(int(digit) * (10 - i) for i, digit in enumerate(isbn[:9]))
    checksum = (11 - (total % 11)) % 11
    correct_check = "X" if checksum == 10 else str(checksum)
    
    if isbn[9] != correct_check:
        print(f"Warning: Correcting ISBN-10 checksum from {isbn[9]} to {correct_check}", 
              file=sys.stderr)
        return isbn[:9] + correct_check
    return isbn


def validate_isbn13(isbn: str) -> str:
    """Validate and correct ISBN-13 checksum."""
    if not isbn.isdigit():
        raise ValueError(f"Invalid ISBN-13 format: {isbn}")
    
    # Calculate correct checksum
    total = sum(int(digit) * (1 if i % 2 == 0 else 3) for i, digit in enumerate(isbn[:12]))
    checksum = (10 - (total % 10)) % 10
    
    if int(isbn[12]) != checksum:
        print(f"Warning: Correcting ISBN-13 checksum from {isbn[12]} to {checksum}", 
              file=sys.stderr)
        return isbn[:12] + str(checksum)
    return isbn


def lookup_isbn(isbn: str) -> Optional[Dict[str, Any]]:
    """
    Look up book metadata by ISBN using Open Library API.
    Primary endpoint: /isbn/{isbn}.json
    Fallback: search API if needed.
    """
    try:
        isbn_valid = validate_isbn(isbn)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return None
    
    # Try the edition endpoint first (primary source)
    url = f"https://openlibrary.org/isbn/{isbn_valid}.json"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            return extract_catalog_fields(data, isbn_valid)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"ISBN not found: {isbn_valid}", file=sys.stderr)
            return None
        else:
            print(f"API error: {e.code}", file=sys.stderr)
            return None
    except (urllib.error.URLError, json.JSONDecodeError, Exception) as e:
        print(f"Error querying API: {e}", file=sys.stderr)
        return None


def extract_catalog_fields(data: Dict[str, Any], isbn: str) -> Dict[str, Any]:
    """
    Extract required catalog fields from Open Library response.
    Fields: Title, author, publish, subject, date, abstract, ISBN, location
    """
    catalog = {
        "isbn": isbn,
        "title": data.get("title", "Not available"),
        "author": extract_authors(data.get("authors", [])),
        "publish": extract_publisher(data.get("publishers", [])),
        "publish_date": data.get("publish_date", "Not available"),
        "subject": extract_subjects(data.get("subjects", [])),
        "abstract": data.get("description", "Not available"),
        "location": "Not available",  # Not provided by Open Library endpoint
    }
    return catalog


def extract_authors(authors: list) -> str:
    """Extract author names from author list."""
    if not authors:
        return "Not available"
    
    names = []
    for author in authors:
        if isinstance(author, dict):
            names.append(author.get("name", "Unknown"))
        elif isinstance(author, str):
            names.append(author)
    
    return "; ".join(names) if names else "Not available"


def extract_publisher(publishers: list) -> str:
    """Extract publisher names from publisher list."""
    if not publishers:
        return "Not available"
    
    names = []
    for pub in publishers:
        if isinstance(pub, dict):
            names.append(pub.get("name", "Unknown"))
        elif isinstance(pub, str):
            names.append(pub)
    
    return "; ".join(names) if names else "Not available"


def extract_subjects(subjects: list) -> str:
    """Extract subject tags from subject list."""
    if not subjects:
        return "Not available"
    
    names = []
    for subject in subjects:
        if isinstance(subject, dict):
            names.append(subject.get("name", "Unknown"))
        elif isinstance(subject, str):
            names.append(subject)
    
    return "; ".join(names) if names else "Not available"


def format_output(catalog: Dict[str, Any]) -> str:
    """Format catalog data for display."""
    output = []
    fields = [
        ("ISBN", "isbn"),
        ("Title", "title"),
        ("Author", "author"),
        ("Publisher", "publish"),
        ("Publication Date", "publish_date"),
        ("Subject", "subject"),
        ("Abstract", "abstract"),
        ("Location", "location"),
    ]
    
    for label, key in fields:
        value = catalog.get(key, "Not available")
        output.append(f"{label:20} : {value}")
    
    return "\n".join(output)


def main():
    if len(sys.argv) < 2:
        print("Usage: python catalog_lookup.py <ISBN>")
        print("Example: python catalog_lookup.py 978-0-12-345678-9")
        sys.exit(1)
    
    isbn = sys.argv[1]
    result = lookup_isbn(isbn)
    
    if result:
        print(format_output(result))
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
