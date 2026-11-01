import csv
import io
import unittest

from email_lists import MAX_BYTES, compare, export_csv, read_emails


class EmailListTests(unittest.TestCase):
    def test_normalizes_header_bom_whitespace_case_and_duplicates(self):
        data = '\ufeff Email ,Name\n ALEX@example.com ,Alex\nalex@example.com,Alex\n,Missing\n'.encode()
        self.assertEqual(read_emails(data), {"alex@example.com"})

    def test_three_comparison_modes(self):
        first = {"alex@example.com", "sam@example.com"}
        second = {"lee@example.com", "sam@example.com"}
        self.assertEqual(compare(first, second, "different"), ["alex@example.com", "lee@example.com"])
        self.assertEqual(compare(first, second, "merged"), ["alex@example.com", "lee@example.com", "sam@example.com"])
        self.assertEqual(compare(first, second, "shared"), ["sam@example.com"])

    def test_rejects_missing_or_duplicate_email_columns(self):
        for data in [b"Name\nAlex\n", b"Email, email\na,b\n", b""]:
            with self.subTest(data=data), self.assertRaises(ValueError):
                read_emails(data)

    def test_rejects_malformed_csv_and_non_utf8(self):
        for data in [b'Email\n"unterminated', b"Email,Name\na,b,c\n", b"Email\n\xff"]:
            with self.subTest(data=data), self.assertRaises(ValueError):
                read_emails(data)

    def test_rejects_oversized_upload(self):
        with self.assertRaises(ValueError):
            read_emails(b"x" * (MAX_BYTES + 1))

    def test_empty_list_is_valid(self):
        self.assertEqual(read_emails(b"Email\n\n"), set())
        self.assertEqual(compare(set(), {"a@example.com"}, "merged"), ["a@example.com"])

    def test_csv_formula_prefixes_are_neutralized_and_cells_quoted(self):
        addresses = ["=1+1", "+cmd", "-1", "@SUM(1)", "normal@example.com", 'a,"b']
        rows = list(csv.reader(io.StringIO(export_csv(addresses).decode())))
        self.assertEqual(rows, [["Email"], ["'=1+1"], ["'+cmd"], ["'-1"], ["'@SUM(1)"], ["normal@example.com"], ['a,"b']])

    def test_invalid_mode_fails_explicitly(self):
        with self.assertRaises(ValueError):
            compare(set(), set(), "invalid")


if __name__ == "__main__":
    unittest.main()
