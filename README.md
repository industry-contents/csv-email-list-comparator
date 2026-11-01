# CSV Email List Comparator

[![Python checks](https://github.com/industry-contents/csv-email-list-comparator/actions/workflows/python-checks.yml/badge.svg)](https://github.com/industry-contents/csv-email-list-comparator/actions/workflows/python-checks.yml)

Compare two CSV email lists, review shared addresses and export the result. Built for marketing and contact-list workflows with Python and Streamlit. It compares lists; it does not check deliverability.

Built by [Industry Contents](https://industrycontents.com).

## What it does

- Accepts two UTF-8 CSV files with an `Email` column.
- Normalizes column names, letter case and surrounding whitespace; removes duplicate and empty values.
- Offers explicit comparison modes rather than silently choosing a merge rule.
- Shows distinct-list and overlap counts, then exports results in stable alphabetical order.
- Rejects malformed, ambiguous or oversized CSV input and neutralizes spreadsheet formula prefixes in exports.

## Comparison modes

| Mode | Result |
| --- | --- |
| Only in one list | Addresses in either list, excluding addresses shared by both; the original default behavior |
| Merge both lists | Every address, with one copy of each |
| Shared by both lists | Addresses present in both lists |

### Example

First file:

```csv
Email
alex@example.com
sam@example.com
```

Second file:

```csv
Email
sam@example.com
lee@example.com
```

“Only in one list” returns `alex@example.com` and `lee@example.com`. “Merge” returns all three addresses. “Shared” returns `sam@example.com`.

## Run locally

Use Python 3.11 or 3.12:

```sh
git clone https://github.com/industry-contents/csv-email-list-comparator.git
cd csv-email-list-comparator
python -m venv .venv
```

Activate the environment with `source .venv/bin/activate` on macOS/Linux or `.venv\Scripts\Activate.ps1` in Windows PowerShell, then:

```sh
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

Open the local address printed by Streamlit, choose a comparison mode and upload both files. No API key or external verification service is required.

## Test

```sh
python -m unittest discover -v
```

The comparison module uses only the standard library. Tests cover comparison modes, normalization, duplicate removal, malformed input, upload limits and safe CSV export. GitHub Actions runs them on Python 3.11 and 3.12.

## Project structure

| File | Purpose |
| --- | --- |
| `email_lists.py` | CSV parsing, set operations and safe export; no network calls |
| `streamlit_app.py` | Upload, mode selection, metrics and download interface |
| `test_email_lists.py` | Unit tests |

## Limits and data handling

Each input is limited to 5 MB and 100,000 rows. CSVs must be UTF-8 with exactly one `Email` column; other columns are ignored. Exports prefix formula-sensitive values with an apostrophe to prevent spreadsheet injection.

The app makes no external calls and stores nothing. Run it locally for real contact data.

## Contributing

Open an issue with a synthetic input and the expected result. Run the tests before submitting a pull request.

## Security

See [SECURITY.md](SECURITY.md).

## License

[MIT](LICENSE) © Yajush Gupta
