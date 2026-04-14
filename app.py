#!/usr/bin/env python3
"""
Library Catalog Query Application
Web interface for librarians to search and retrieve book metadata.
Uses Flask for the web framework and Open Library API as the data source.
"""

from flask import Flask, render_template, request, jsonify
import json
import logging
import os
import time
import urllib.parse
import urllib.request
import urllib.error
from collections import defaultdict
from typing import Optional, Dict, Any, List

app = Flask(__name__)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Rate limiting: max 60 requisições por minuto por IP
_rate_store: dict = defaultdict(list)
RATE_LIMIT = 60
RATE_WINDOW = 60  # segundos


def is_rate_limited(ip: str) -> bool:
    """Return True if the IP has exceeded the rate limit."""
    now = time.time()
    window_start = now - RATE_WINDOW
    _rate_store[ip] = [t for t in _rate_store[ip] if t > window_start]
    if len(_rate_store[ip]) >= RATE_LIMIT:
        return True
    _rate_store[ip].append(now)
    # Evict IPs with no recent requests to prevent unbounded memory growth
    stale = [k for k, v in _rate_store.items() if not v]
    for k in stale:
        del _rate_store[k]
    return False


def validate_isbn(isbn: str) -> str:
    """Validate and auto-correct ISBN-10/13 checksums."""
    isbn_clean = isbn.replace("-", "").replace(" ", "").strip()
    
    if len(isbn_clean) == 10:
        return validate_isbn10(isbn_clean)
    elif len(isbn_clean) == 13:
        return validate_isbn13(isbn_clean)
    else:
        raise ValueError(f"ISBN deve ter 10 ou 13 dígitos. Recebido: {len(isbn_clean)}")


def validate_isbn10(isbn: str) -> str:
    """Validate and correct ISBN-10 checksum."""
    if not isbn[:9].isdigit():
        raise ValueError("ISBN-10 inválido: deve conter apenas dígitos")
    
    total = sum(int(digit) * (10 - i) for i, digit in enumerate(isbn[:9]))
    checksum = (11 - (total % 11)) % 11
    correct_check = "X" if checksum == 10 else str(checksum)
    
    if isbn[9] != correct_check:
        return isbn[:9] + correct_check
    return isbn


def validate_isbn13(isbn: str) -> str:
    """Validate and correct ISBN-13 checksum."""
    if not isbn.isdigit():
        raise ValueError("ISBN-13 inválido: deve conter apenas dígitos")
    
    total = sum(int(digit) * (1 if i % 2 == 0 else 3) for i, digit in enumerate(isbn[:12]))
    checksum = (10 - (total % 10)) % 10
    
    if int(isbn[12]) != checksum:
        return isbn[:12] + str(checksum)
    return isbn


def lookup_by_isbn(isbn: str) -> Optional[Dict[str, Any]]:
    """Look up book metadata by ISBN from Open Library."""
    try:
        isbn_valid = validate_isbn(isbn)
    except ValueError as e:
        return {"error": str(e)}
    
    url = f"https://openlibrary.org/isbn/{isbn_valid}.json"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            return extract_catalog_fields(data, isbn_valid)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"error": f"ISBN não encontrado: {isbn_valid}"}
        else:
            return {"error": f"Erro na API: {e.code}"}
    except Exception as e:
        return {"error": f"Erro ao consultar: {str(e)}"}


def search_by_title_or_author(query: str, search_type: str = "title") -> List[Dict[str, Any]]:
    """Search Open Library by title or author."""
    if not query or len(query.strip()) < 2:
        return []
    
    if search_type == "author":
        url = f"https://openlibrary.org/search/authors.json?q={urllib.parse.quote_plus(query)}&limit=10"
    else:  # title
        url = f"https://openlibrary.org/search.json?title={urllib.parse.quote_plus(query)}&limit=10"
    
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if search_type == "author":
                docs = data.get("docs", [])
                results = []
                for doc in docs:
                    results.append({
                        "name": doc.get("name", "Desconhecido"),
                        "works_count": doc.get("work_count", 0),
                        "type": "author"
                    })
                return results
            else:
                docs = data.get("docs", [])
                results = []
                for doc in docs:
                    isbn_list = doc.get("isbn", [])
                    isbn = isbn_list[0] if isbn_list else "Não disponível"
                    
                    results.append({
                        "title": doc.get("title", "Desconhecido"),
                        "author": ", ".join(doc.get("author_name", ["Desconhecido"])),
                        "isbn": isbn,
                        "year": doc.get("first_publish_year", "Desconhecido"),
                        "type": "book",
                        "edition_count": doc.get("edition_count", 0)
                    })
                return results
    except Exception as e:
        logger.error("Erro na busca por %s '%s': %s", search_type, query, e)
        return []


def _extract_text(value: Any, default: str = "Não disponível") -> str:
    """Safely extract a string value that may be a dict (Open Library pattern)."""
    if value is None:
        return default
    if isinstance(value, dict):
        return value.get("value", default)
    return str(value)


def extract_catalog_fields(data: Dict[str, Any], isbn: str) -> Dict[str, Any]:
    """Extract 8 required catalog fields from Open Library response."""
    return {
        "isbn": isbn,
        "title": data.get("title", "Não disponível"),
        "author": extract_authors(data.get("authors", [])),
        "publisher": extract_publisher(data.get("publishers", [])),
        "publish_date": data.get("publish_date", "Não disponível"),
        "subject": extract_subjects(data.get("subjects", [])),
        "abstract": data.get("description", "Não disponível"),
        "location": "Não disponível",
        "type": "book",
        "pages": data.get("number_of_pages", "Desconhecido")
    }


def extract_authors(authors: list) -> str:
    """Extract author names from author list."""
    if not authors:
        return "Não disponível"
    
    names = []
    for author in authors:
        if isinstance(author, dict):
            names.append(author.get("name", "Desconhecido"))
        elif isinstance(author, str):
            names.append(author)
    
    return "; ".join(names) if names else "Não disponível"


def extract_publisher(publishers: list) -> str:
    """Extract publisher names from publisher list."""
    if not publishers:
        return "Não disponível"
    
    names = []
    for pub in publishers:
        if isinstance(pub, dict):
            names.append(pub.get("name", "Desconhecido"))
        elif isinstance(pub, str):
            names.append(pub)
    
    return "; ".join(names) if names else "Não disponível"


def extract_subjects(subjects: list) -> str:
    """Extract subject tags from subject list."""
    if not subjects:
        return "Não disponível"
    
    names = []
    for subject in subjects:
        if isinstance(subject, dict):
            names.append(subject.get("name", "Desconhecido"))
        elif isinstance(subject, str):
            names.append(subject)
    
    return "; ".join(names[:5]) if names else "Não disponível"


@app.route('/')
def index():
    """Render the main search page."""
    return render_template('index.html')


@app.route('/api/search', methods=['GET'])
def search():
    """API endpoint for searching."""
    if is_rate_limited(request.remote_addr):
        logger.warning("Rate limit atingido: %s", request.remote_addr)
        return jsonify({"error": "Muitas requisições. Tente novamente em instantes."}), 429

    query = request.args.get('q', '').strip()
    search_type = request.args.get('type', 'isbn')  # isbn, title, author

    logger.info("Busca: type=%s q=%s ip=%s", search_type, query, request.remote_addr)

    if not query:
        return jsonify({"error": "Consulta vazia"}), 400
    
    if search_type == 'isbn':
        result = lookup_by_isbn(query)
        if "error" in result:
            return jsonify(result), 404
        return jsonify({"results": [result]})
    
    elif search_type == 'title':
        results = search_by_title_or_author(query, 'title')
        return jsonify({"results": results})
    
    elif search_type == 'author':
        results = search_by_title_or_author(query, 'author')
        return jsonify({"results": results})
    
    else:
        return jsonify({"error": "Tipo de busca inválido"}), 400


@app.route('/api/lookup-isbn', methods=['GET'])
def lookup_isbn_api():
    """Direct ISBN lookup endpoint."""
    if is_rate_limited(request.remote_addr):
        logger.warning("Rate limit atingido: %s", request.remote_addr)
        return jsonify({"error": "Muitas requisições. Tente novamente em instantes."}), 429

    isbn = request.args.get('isbn', '').strip()

    logger.info("ISBN lookup: isbn=%s ip=%s", isbn, request.remote_addr)

    if not isbn:
        return jsonify({"error": "ISBN não fornecido"}), 400
    
    result = lookup_by_isbn(isbn)
    
    if "error" in result:
        return jsonify(result), 404
    
    return jsonify(result)


if __name__ == '__main__':
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=debug, host=host, port=port)
