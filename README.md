# Email List Checker

A small Python and Streamlit tool for comparing two CSV email lists and exporting addresses that appear in only one list.

**Status: prototype.** Despite the repository's historical name, this application does not verify email deliverability, DNS records or mailbox ownership.

## Use case

Compare two campaign or contact-list exports before a marketing workflow. The app highlights shared addresses and produces the symmetric difference between the lists. Use only data you are authorized to process.

## How it works

1. Upload two CSV files, each containing an `Email` column. Column names are trimmed and converted to lowercase.
2. The app drops missing email values, lowercases addresses and creates a set for each file.
3. It reports the number of addresses shared by both sets.
4. It exports addresses present in exactly one set as `unique_emails.csv`.

**This is not a normal merge-and-deduplicate operation:** an address that appears in both lists is excluded from the output entirely.

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

The output contains `alex@example.com` and `lee@example.com`; `sam@example.com` is excluded. Row order is not guaranteed.

## Run locally

Install Python 3 and create an isolated environment:

```sh
git clone https://github.com/YJush/YJush-email-verifier-streamlit.git
cd YJush-email-verifier-streamlit
python -m venv .venv
```

Activate it with `source .venv/bin/activate` on macOS/Linux or `.venv\Scripts\Activate.ps1` in Windows PowerShell. Then:

```sh
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

Open the local address printed by Streamlit and upload the two CSV files. No external email-verification API or API key is required.

## Project structure

| File | Purpose |
| --- | --- |
| `streamlit_app.py` | Upload interface, set comparison and CSV download |
| `requirements.txt` | Python dependencies |
| `.devcontainer/devcontainer.json` | Development-container configuration |

The application uses Streamlit and pandas. `dnspython` is listed as a dependency but is not used by the current code.

## Validation and limitations

Use the synthetic example above to check the expected comparison. No automated test suite is currently included. Dependencies are not version-pinned.

Email values are lowercased but not trimmed, so surrounding whitespace can produce mismatches. Malformed CSV input and non-text email columns are not fully handled. The tool does not check syntax, consent, suppression lists, delivery status or whether an address exists. CSV downloads are not hardened against spreadsheet formula injection; use synthetic data for demonstrations and treat untrusted exports carefully.

## Privacy

The current code has no explicit persistence layer or external API calls. Uploads are processed by the machine running Streamlit. A hosted deployment receives the uploaded data on its server; run locally when appropriate and do not commit real contact lists, exported files or credentials.

## Contributing

Good next improvements include whitespace normalization, explicit comparison modes, stable output ordering, friendly CSV errors, safe exports and deterministic tests. Include a synthetic input and the expected result when proposing a change.

## License

No project license is currently included. Contact the repository owner before reusing the code; dependencies retain their own licenses.
