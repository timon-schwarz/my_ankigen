import re
from typing import List


def get_masked(text: str) -> str:
    """
    Replace every character in the input string, except tabs and newlines, with a space.
    A span tag with a special style is used to instruct the HTML renderer to preserve the whitespace.
    The "masked" class is added.
    """
    return (
        '<span class="masked" style="white-space: pre;">'
        + re.sub(r"[^\t\n]", " ", text)
        + "</span>"
    )


def get_unmasked(text: str) -> str:
    """
    A span tag with with the "unmasked" class is added.
    """
    return '<span class="unmasked">' + text + "</span>"


def add_card_header(header: str, content: str) -> str:
    """
    Prepends the header to the content.
    """
    return "\n".join([f'<span class="card_header">{header}</span>', content])


def render_table(table: List[List[str]]) -> str:
    """
    Format a 2D list of strings as an HTML table.
    The entire table is enclosed in a <tbody>.
    The first row cells receive the 'table_header_top' class,
    the first column cells receive the 'table_header_left' class,
    and all cells receive the 'table_body' class.
    """
    if not table:
        return ""

    html_lines = ["<table>", "  <tbody>"]

    for i, row in enumerate(table):
        html_lines.append("    <tr>")
        for j, cell in enumerate(row):
            classes = ["table_body"]
            if i == 0 and j == 0:
                classes.append("table_corner")
            elif i == 0:
                classes.append("table_header_top")
            elif j == 0:
                classes.append("table_header_left")
            class_attr = " ".join(classes)
            html_lines.append(f'      <td class="{class_attr}">{cell}</td>')
        html_lines.append("    </tr>")

    html_lines.append("  </tbody>")
    html_lines.append("</table>")
    return "\n".join(html_lines)
