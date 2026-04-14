# Catalog Lookup CLI

A Python command-line tool for looking up book catalog metadata by ISBN.

## Features

- **ISBN Validation**: Validates and auto-corrects ISBN-10 and ISBN-13 checksums
- **Open Library Integration**: Queries the Open Library API as primary data source
- **Comprehensive Metadata**: Returns 8 catalog fields:
  - ISBN
  - Title
  - Author
  - Publisher (Publish)
  - Publication Date
  - Subject
  - Abstract (Description)
  - Location (from local catalog, if available)

## Requirements

- Python 3.6+
- No external dependencies (uses only stdlib)

## Installation

1. Clone or download the repository
2. Make the script executable (optional):
   ```bash
   chmod +x catalog_lookup.py
   ```

## Usage

### Basic lookup
```bash
python catalog_lookup.py 978-0-12-345678-9
```

### With ISBN-10
```bash
python catalog_lookup.py 0-12-345678-9
```

### With hyphens or spaces
```bash
python catalog_lookup.py "978 0 12 345678 9"
```

## Output Example

```
ISBN                 : 978-0-123456789
Title                : The History of Aviation
Author               : Smith, John
Publisher            : Academic Press
Publication Date     : 2020
Subject              : History of aviation; Aerospace engineering
Abstract             : A comprehensive overview of aviation development...
Location             : Not available
```

## How It Works

1. **Validation**: Accepts ISBN-10 or ISBN-13 and auto-corrects invalid checksums
2. **API Query**: Sends request to Open Library: `https://openlibrary.org/isbn/{isbn}.json`
3. **Extraction**: Parses response and extracts catalog metadata
4. **Display**: Formats and prints results to console

## Error Handling

- Invalid ISBN format: Shows error message and exits with code 1
- ISBN not found: Shows "ISBN not found" and exits with code 1
- API errors: Shows error details and exits with code 1
- Checksum corrections: Displays warnings to stderr and uses corrected ISBN

## Exit Codes

- `0`: Success
- `1`: Error (invalid ISBN, not found, API error)

## API Source

- Primary: Open Library Edition endpoint `/isbn/{isbn}.json`
- Fallback: Open Library Search API (not yet implemented)

## Limitations

- **Location**: Not provided by Open Library API; would require local integration
- **Abstract**: Retrieved as "description" field from Open Library
- **Coverage**: Only covers ISBNs indexed in Open Library

## Future Enhancements

- Integrate with library system (OPAC) for local location data
- Add fallback to WorldCat API
- Support for other metadata formats (MARC, JSON-LD)
- Batch lookup from file
- Output to JSON, CSV, or CSV formats
