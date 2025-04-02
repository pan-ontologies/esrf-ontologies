import os
import json
from typing import List, Dict, Any

from docutils import nodes
from docutils.parsers.rst import Directive


class InsertTechniqueTable(Directive):
    def run(self):
        rows = _generate_table_data()
        table_node = self._create_table(rows)
        search_box = self._create_search_box()
        script = self._create_filter_script()
        return [search_box, table_node, script]

    def _create_table(self, rows: List[Dict[str, Any]]) -> nodes.container:
        # Create a container for the scrollable table
        scrollable_container = nodes.container(classes=["scrollable-table"])

        # Create the table node
        table_node = nodes.table(classes=["table", "table-bordered", "table-striped"])
        table_node["ids"] = ["technique-table"]
        tgroup = nodes.tgroup(cols=len(rows[0]))
        table_node += tgroup

        # Create column specifications
        for _ in rows[0]:
            colspec = nodes.colspec(colwidth=1)
            tgroup += colspec

        # Create and add table header
        thead = nodes.thead()
        tgroup += thead
        header_row = nodes.row()
        for key in rows[0]:
            entry = nodes.entry()
            entry += nodes.paragraph(text=key)
            header_row += entry
        thead += header_row

        # Create and add table body
        tbody = nodes.tbody()
        tgroup += tbody
        for row_data in rows:
            row = nodes.row()
            row["classes"].append("table-row")
            for key, value in row_data.items():
                entry = nodes.entry()
                value = str(value)
                if value.startswith("<a "):
                    entry += nodes.raw("", value, format="html")
                else:
                    entry += nodes.paragraph(text=value)
                row += entry
            tbody += row

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
