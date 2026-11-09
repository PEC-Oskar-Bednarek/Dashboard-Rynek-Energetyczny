from datetime import date, datetime
from pathlib import Path
from uuid import uuid4


def save_dashboard_html(
    html: bytes,
    report_date: date,
    output_directory: Path,
) -> tuple[Path, Path]:
    output_directory.mkdir(parents=True, exist_ok=True)
    archive_directory = output_directory / "raporty"
    archive_directory.mkdir(parents=True, exist_ok=True)
    timestamp = f"{datetime.now():%Y%m%d-%H%M%S-%f}-{uuid4().hex[:8]}"
    current_path = output_directory / "market_dashboard.html"
    archive_path = archive_directory / f"raport-{report_date.isoformat()}-{timestamp}.html"
    current_path.write_bytes(html)
    archive_path.write_bytes(html)
    return current_path, archive_path


def save_report_pdf(pdf: bytes, archived_html_path: Path) -> Path:
    pdf_path = archived_html_path.with_suffix(".pdf")
    pdf_path.write_bytes(pdf)
    return pdf_path
