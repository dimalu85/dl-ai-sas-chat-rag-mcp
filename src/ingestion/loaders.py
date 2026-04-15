"""Document loaders for PDFs and CSV disaster data."""

from pathlib import Path

import pandas as pd
from langchain_core.documents import Document

from src.config import REQUIRED_CSV_COLUMNS


def load_pdfs(pdf_dir: str | Path) -> list[Document]:
    """Load all PDFs from a directory into LangChain Documents.

    Each page becomes one Document with metadata:
    ``filename``, ``page``, ``doc_type``.
    """
    from langchain_community.document_loaders import PyPDFLoader

    pdf_dir = Path(pdf_dir)
    if not pdf_dir.exists():
        return []

    docs: list[Document] = []
    for pdf_path in sorted(pdf_dir.glob("*.pdf")):
        loader = PyPDFLoader(str(pdf_path))
        pages = loader.load()
        for page in pages:
            page.metadata.update(
                {
                    "filename": pdf_path.name,
                    "doc_type": "pdf",
                }
            )
        docs.extend(pages)

    return docs


def load_csv_as_docs(csv_path: str | Path) -> list[Document]:
    """Convert CSV rows into LangChain Documents for embedding.

    Each row becomes one Document whose ``page_content`` is a
    human-readable summary of the key columns.  Metadata includes
    ``source``, ``doc_type``, ``year``, ``country``, ``disaster_type``.
    """
    csv_path = Path(csv_path)
    df = pd.read_csv(csv_path)

    docs: list[Document] = []
    for idx, row in df.iterrows():
        parts = []
        if pd.notna(row.get("Year")):
            parts.append(f"Year: {int(row['Year'])}")
        if pd.notna(row.get("Country")):
            parts.append(f"Country: {row['Country']}")
        if pd.notna(row.get("Disaster Type")):
            parts.append(f"Disaster Type: {row['Disaster Type']}")
        if pd.notna(row.get("Disaster Subtype")):
            parts.append(f"Subtype: {row['Disaster Subtype']}")
        if pd.notna(row.get("Total Deaths")):
            parts.append(f"Total Deaths: {int(row['Total Deaths'])}")
        if pd.notna(row.get("Total Affected")):
            parts.append(f"Total Affected: {int(row['Total Affected'])}")
        damages_col = "Total Damages ('000 US$)"
        if pd.notna(row.get(damages_col)):
            parts.append(f"Damages (000 US$): {int(row[damages_col])}")
        if pd.notna(row.get("Location")):
            parts.append(f"Location: {row['Location']}")

        content = " | ".join(parts)

        metadata = {
            "source": csv_path.name,
            "doc_type": "csv",
            "row_index": int(idx),
            "year": int(row["Year"]) if pd.notna(row.get("Year")) else None,
            "country": str(row.get("Country", "")),
            "disaster_type": str(row.get("Disaster Type", "")),
        }

        docs.append(Document(page_content=content, metadata=metadata))

    return docs
