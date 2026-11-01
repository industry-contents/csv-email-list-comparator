# Email List Checker

[![Python checks](https://github.com/YJush/YJush-email-verifier-streamlit/actions/workflows/python-checks.yml/badge.svg)](https://github.com/YJush/YJush-email-verifier-streamlit/actions/workflows/python-checks.yml)

Compare two CSV email lists, review shared addresses and export the result. Built for small marketing and contact-list workflows with Python and Streamlit.

**Status: portfolio prototype with tested comparison logic.** This is a list-comparison tool, not an email-deliverability verifier.

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
git clone https://github.com/YJush/YJush-email-verifier-streamlit.git
cd YJush-email-verifier-streamlit
python -m venv .venv
```

Activate the environment with `source .venv/bin/activate` on macOS/Linux or `.venv\Scripts\Activate.ps1` in Windows PowerShell, then:

```sh
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

Open the local address printed by Streamlit, choose a comparison mode and upload both files. No API key or external verification service is required.

## Test

The comparison module uses the Python standard library, so its tests do not require installing Streamlit:

```sh
python -m unittest discover -v
python -m py_compile email_lists.py streamlit_app.py test_email_lists.py
```

Eight local tests passed during the November 2026 portfolio update. They cover comparison modes, normalization and duplicate removal, missing/ambiguous headers, malformed/non-UTF-8 input, upload limits, empty lists, safe CSV exports and invalid modes. The GitHub Actions workflow repeats syntax and unit checks on Python 3.11 and 3.12. A passing unit suite does not establish that a deployed UI is working.

## Project structure

| File | Purpose |
| --- | --- |
| `email_lists.py` | CSV parsing, set operations and safe export; no network calls |
| `streamlit_app.py` | Uploads, mode selection, metrics and download interface |
| `test_email_lists.py` | Standard-library regression tests |
| `.github/workflows/python-checks.yml` | Syntax and unit checks |
| `requirements.txt` | UI runtime dependency |
| `.devcontainer/devcontainer.json` | Development-container configuration |

## Limits and data handling

Each input is limited to 5 MB and 100,000 rows. CSVs must use UTF-8, have consistent row widths and contain exactly one normalized `Email` column. Other columns are ignored. The parser does not validate email syntax, confirm consent, check suppression lists or contact a mailbox/DNS service.

Values beginning with spreadsheet formula-sensitive characters are prefixed with an apostrophe in downloads. That is an export safeguard and can change the literal cell value. Case and whitespace normalization also intentionally alter source values.

The application has no explicit persistence layer or external API calls. A hosted deployment still receives uploads on its server. Run locally when appropriate, use synthetic data for demonstrations and never commit real contact exports or credentials. Dependencies are not locked to exact versions; a full deployment and dependency audit remain separate work.

## Contributing

Describe the workflow problem and include synthetic input with the expected result. Run the checks above before proposing a change. Useful next work includes browser-level UI tests, reproducible dependency locking and a synthetic-data demo. Do not post contact lists or secrets in issues.

## License

No project license is currently included. Contact the owner before reusing the code; dependencies retain their own licenses.
