# Code Style

## Python

- No comments unless explicitly requested
- Use docstrings only for public APIs
- Follow existing patterns in the codebase

## File Structure

- Entry points: `validate_*.py`, `generate_*.py` in project root
- Data directories: `products/`, `reviews/`, `images/`, `sellers/`, `verdicts/` for Amazon
- OTTO directories: prefixed with `otto-`
- Raw data: `scraped/`, `search/`

## JSON Data Files

- Use `{asin}_listing.json`, `{asin}_analysis.json`, etc. naming convention
- Store in respective data directories

## Script Patterns

- `validate_*.py` — validates required fields in verdict JSON
- `generate_*.py` — generates HTML report from verdict JSON
- Always run validation before report generation
