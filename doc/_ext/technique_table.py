import json
import os
from typing import Any
from typing import Dict
from typing import List

from docutils import nodes
from docutils.parsers.rst import Directive

VISIBLE_COLUMNS = ["Name", "Alternative names", "Description"]


class InsertTechniqueTable(Directive):

    def run(self):
        rows = _generate_table_data()
        count_paragraph = self._create_technique_count(len(rows))
        table_node = self._create_table(rows)
        search_box = self._create_search_box()
        script = self._create_filter_script()
        return [count_paragraph, search_box, table_node, script]

    def _create_technique_count(self, count: int) -> nodes.paragraph:
        paragraph = nodes.paragraph()
        paragraph += nodes.Text("The ESRFET ontology currently contains ")
        paragraph += nodes.strong(text=f"{count} techniques")
        paragraph += nodes.Text(".")
        return paragraph

    def _create_row(self, row_data: Dict[str, Any]) -> nodes.row:
        row = nodes.row()
        row["classes"].append("table-row")
        for key in VISIBLE_COLUMNS:
            entry = nodes.entry()
            if key == "Name":
                entry += self._create_name_cell(row_data)
            else:
                entry += nodes.paragraph(text=str(row_data.get(key, "")))
            row += entry
        return row

    def _create_name_cell(self, row_data: Dict[str, Any]) -> nodes.paragraph:
        name = str(row_data.get("Name", ""))
        copy_iri = row_data.get("copyIRI", "")
        versioned_link = row_data.get("Link", "")

        html = f"""
        <div class="technique-entry">
            <span onclick="navigator.clipboard.writeText('{copy_iri}');"
                title="Copy stable IRI"
                style="cursor:pointer; margin-right:4px;">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M10 1.5v1h1A1.5 1.5 0 0 1 12.5 4v10A1.5 1.5 0 0 1 11 15.5H5A1.5 1.5 0 0 1 3.5 14V4A1.5 1.5 0 0 1 5 2.5h1v-1h4zM5 2a.5.5 0 0 0-.5.5v1h7v-1a.5.5 0 0 0-.5-.5H5z"/>
                </svg>
            </span>
            <a href="{versioned_link}" target="_blank" rel="noreferrer">
                {name}
            </a>
        </div>
        """
        return nodes.raw("", html, format="html")

    def _create_table(self, rows: List[Dict[str, Any]]) -> nodes.container:
        # Create a container for the scrollable table
        scrollable_container = nodes.container(classes=["scrollable-table"])

        # Create the table node
        table_node = nodes.table(classes=["table", "table-bordered", "table-striped"])
        table_node["ids"] = ["technique-table"]

        tgroup = nodes.tgroup(cols=len(VISIBLE_COLUMNS))
        table_node += tgroup

        for _ in VISIBLE_COLUMNS:
            tgroup += nodes.colspec(colwidth=1)

        # Create and add table header
        thead = nodes.thead()
        tgroup += thead
        header_row = nodes.row()
        for key in VISIBLE_COLUMNS:
            entry = nodes.entry()
            entry += nodes.paragraph(text=key)
            header_row += entry
        thead += header_row

        # Create and add table body
        tbody = nodes.tbody()
        tgroup += tbody
        for row_data in rows:
            tbody += self._create_row(row_data)

        # Add the table node to the scrollable container
        scrollable_container += table_node

        return scrollable_container

    def _create_search_box(self) -> nodes.raw:
        search_html = """
        <div>
            <input type="text" id="search-box" placeholder="Search...">
        </div>
        """
        return nodes.raw("", search_html, format="html")

    def _create_filter_script(self) -> nodes.raw:
        script_html = """
        <script>
            document.addEventListener("DOMContentLoaded", function() {
                var searchBox = document.getElementById("search-box");
                searchBox.addEventListener("input", function() {
                    var filter = searchBox.value.toLowerCase();
                    var rows = document.querySelectorAll(".table-row");
                    rows.forEach(function(row) {
                        var text = row.textContent.toLowerCase();
                        if (text.includes(filter)) {
                            row.style.display = "";
                        } else {
                            row.style.display = "none";
                        }
                    });
                });
            });
        </script>
        """
        return nodes.raw("", script_html, format="html")


def _generate_table_data() -> List[Dict[str, Any]]:
    filename = os.path.join(os.path.dirname(__file__), "techniques.json")
    with open(filename, "r") as f:
        return json.load(f)


def setup(app):
    app.add_directive("insert_technique_table", InsertTechniqueTable)
