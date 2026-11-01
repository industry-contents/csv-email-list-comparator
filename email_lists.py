"""CSV email-list comparison. No network requests or mailbox verification."""

import csv
import io

MAX_BYTES = 5 * 1024 * 1024
MAX_ROWS = 100_000


def read_emails(data: bytes) -> set[str]:
    """Read a UTF-8 CSV with one Email column; reject ambiguous input."""
    if len(data) > MAX_BYTES:
        raise ValueError("Each CSV must be 5 MB or smaller.")
    try:
        text = data.decode("utf-8-sig")
        rows = csv.reader(io.StringIO(text, newline=""), strict=True)
        header = next(rows, None)
        if header is None:
            raise ValueError("The CSV is empty.")
        names = [name.strip().lower() for name in header]
        if names.count("email") != 1:
            raise ValueError("Each CSV must contain exactly one Email column.")
        index = names.index("email")
        emails = set()
        for number, row in enumerate(rows, 1):
            if number > MAX_ROWS:
                raise ValueError("Each CSV must contain no more than 100,000 rows.")
            if not row:
                continue
            if len(row) != len(header):
                raise ValueError(f"CSV row {number + 1} has an unexpected number of columns.")
            address = row[index].strip().lower()
            if address:
                emails.add(address)
        return emails
    except UnicodeDecodeError as error:
        raise ValueError("Save the CSV with UTF-8 encoding and try again.") from error
    except csv.Error as error:
        raise ValueError("The CSV contains malformed or oversized fields.") from error


def compare(first: set[str], second: set[str], mode: str) -> list[str]:
    """Return a deterministic result for an explicit set operation."""
    if mode == "different":
        result = first ^ second
    elif mode == "merged":
        result = first | second
    elif mode == "shared":
        result = first & second
    else:
        raise ValueError("Unknown comparison mode.")
    return sorted(result)


def export_csv(addresses: list[str]) -> bytes:
    """Quote CSV cells and neutralize spreadsheet formula prefixes."""
    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(["Email"])
    for address in addresses:
        safe = "'" + address if address.startswith(("=", "+", "-", "@", "\t", "\r", "\n")) else address
        writer.writerow([safe])
    return output.getvalue().encode("utf-8")
