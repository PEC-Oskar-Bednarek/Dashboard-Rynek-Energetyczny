from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from report_storage import save_dashboard_html, save_report_pdf


class ReportStorageTests(unittest.TestCase):
    def test_saves_current_dashboard_and_timestamped_html_and_pdf_archive(self):
        with TemporaryDirectory() as directory:
            output_directory = Path(directory)
            report_date = date(2026, 11, 8)

            current, archived_html = save_dashboard_html(
                b"<html>report</html>", report_date, output_directory
            )
            archived_pdf = save_report_pdf(b"%PDF-report", archived_html)

            self.assertEqual(current, output_directory / "market_dashboard.html")
            self.assertEqual(current.read_bytes(), b"<html>report</html>")
            self.assertTrue(archived_html.is_relative_to(output_directory / "raporty"))
            self.assertIn("raport-2026-11-08-", archived_html.name)
            self.assertEqual(archived_html.read_bytes(), b"<html>report</html>")
            self.assertEqual(archived_pdf, archived_html.with_suffix(".pdf"))
            self.assertEqual(archived_pdf.read_bytes(), b"%PDF-report")

    def test_new_generation_keeps_previous_archive_and_replaces_current_dashboard(self):
        with TemporaryDirectory() as directory:
            output_directory = Path(directory)
            first_current, first_archive = save_dashboard_html(
                b"first", date(2026, 11, 8), output_directory
            )
            second_current, second_archive = save_dashboard_html(
                b"second", date(2026, 11, 8), output_directory
            )

            self.assertEqual(first_current, second_current)
            self.assertEqual(second_current.read_bytes(), b"second")
            self.assertNotEqual(first_archive, second_archive)
            self.assertEqual(first_archive.read_bytes(), b"first")
            self.assertEqual(second_archive.read_bytes(), b"second")


if __name__ == "__main__":
    unittest.main()
