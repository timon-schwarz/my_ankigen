from typing import List
from note_processor.abstracts import Parser
import markdown
from bs4 import BeautifulSoup
import textwrap


class TableParser(Parser):
    def parse(self, content: str) -> List[List[List[str]]]:
        """
        Parse a markdown table from the given content and return it as a list of rows,
        where each row is a list of cell strings.

        This function uses Python-Markdown with the 'tables' extension to convert the
        markdown into HTML, and then BeautifulSoup to extract table rows and cells.
        """
        # Remove any leading whitespace so the table isn't interpreted as a code block.
        content = textwrap.dedent(content).strip()
        # Convert the markdown to HTML with table support.
        html = markdown.markdown(content, extensions=["tables"])
        # Use BeautifulSoup to parse the HTML.
        soup = BeautifulSoup(html, "html.parser")
        table_tag = soup.find("table")
        if not table_tag:
            return []

        table: List[List[str]] = []
        for tr in table_tag.find_all("tr"):
            # Collect text from header (<th>) and data (<td>) cells.
            cells = tr.find_all(["th", "td"])
            row = [cell.get_text(separator="\n", strip=True) for cell in cells]
            table.append(row)
        tables = []
        tables.append(table)
        return tables
