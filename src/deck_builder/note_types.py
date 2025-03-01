import genanki

# Global CSS shared by all note types.
BASE_CSS = """
/* Base card styling */
.card {
  font-family: 'Century Gothic', sans-serif;
  font-size: 16px;
  color: #cad3f5;             /* Text */
  background-color: #24273a;  /* Base */
  
  /* Use Flexbox to center content vertically and horizontally */
  display: flex;
  justify-content: center;   /* center horizontally */
  align-items: center;       /* center vertically */
  min-height: 100vh;
  min-width: 100vw;
  margin: 0;
  padding: 0;
}

/* A wrapper to constrain the content width and keep text left-aligned */
.card-content {
  margin: 20px;
  width: auto;  /* Let it shrink to fit content */
  text-align: left;
}

.card_header {
  color: #b7bdf8;             /* Lavender */
  font-size: 24px;
  font-weight: bold;
  display: table;             /* Allows margin auto to center horizontally */
  margin: 0 auto 32px auto;   /* Center horizontally, plus bottom margin */
  text-align: center;         /* Center the header text itself */
}

.hints {
  color: #b7bdf8;             /* Lavender */
  margin-top: 32px;           /* Top margin */
  white-space: pre-wrap;
}

.masked, .unmasked, .code {
  font-family: 'Inconsolata', monospace;
}
"""

RANDOMIZE_TABLE_COLUMS_QUESTION_SCRIPT = """
<script>
(function() {
    // Generate and store random seed
    var storageKey = "randomSeed"
    storedSeed = Date.now();
    storedSeed = parseInt(storedSeed, 10);
    localStorage.setItem(storageKey, storedSeed);

    // Simple linear congruential generator (LCG) for seeded randomness.
    function seededRandom(seed) {
        var m = 0x80000000; // 2^31
        var a = 1103515245;
        var c = 12345;
        seed = (a * seed + c) % m;
        return { value: seed / m, seed: seed };
    }

    // Deterministically shuffle an array using the seed.
    function shuffleArray(array, seed) {
        var newArray = array.slice();
        for (var i = newArray.length - 1; i > 0; i--) {
            var rnd = seededRandom(seed);
            seed = rnd.seed;
            var j = Math.floor(rnd.value * (i + 1));
            var temp = newArray[i];
            newArray[i] = newArray[j];
            newArray[j] = temp;
        }
        return newArray;
    }

    // Find the table by its class.
    var table = document.querySelector("table");
    if (!table) return;
    var firstRow = table.rows[0];
    if (!firstRow) return;
    var colCount = firstRow.cells.length;
    if (colCount <= 1) return;

    // Create an array of column indices to shuffle (excluding the first column).
    var indices = [];
    for (var i = 1; i < colCount; i++) {
        indices.push(i);
    }
    // Shuffle deterministically using the stored seed.
    var shuffledIndices = shuffleArray(indices, storedSeed);

    // Apply the permutation to each row.
    for (var r = 0; r < table.rows.length; r++) {
        var row = table.rows[r];
        var firstCell = row.cells[0]; // leave first column as-is.
        var otherCells = [];
        for (var c = 1; c < colCount; c++) {
            otherCells.push(row.cells[c]);
        }
        var newCells = [firstCell];
        shuffledIndices.forEach(function(idx) {
            // Since idx is the original cell index (starting at 1), subtract 1 for our otherCells.
            newCells.push(otherCells[idx - 1]);
        });
        // Clear and reappend cells in new order.
        while (row.firstChild) {
            row.removeChild(row.firstChild);
        }
        newCells.forEach(function(cell) {
            row.appendChild(cell);
        });
    }
})();
</script>
"""

RANDOMIZE_TABLE_COLUMS_ANSWER_SCRIPT = """
<script>
(function() {
    // Load random seed from question
    var storageKey = "randomSeed"
    var storedSeed = localStorage.getItem(storageKey);
    storedSeed = parseInt(storedSeed, 10);

    // Simple linear congruential generator (LCG) for seeded randomness.
    function seededRandom(seed) {
        var m = 0x80000000; // 2^31
        var a = 1103515245;
        var c = 12345;
        seed = (a * seed + c) % m;
        return { value: seed / m, seed: seed };
    }

    // Deterministically shuffle an array using the seed.
    function shuffleArray(array, seed) {
        var newArray = array.slice();
        for (var i = newArray.length - 1; i > 0; i--) {
            var rnd = seededRandom(seed);
            seed = rnd.seed;
            var j = Math.floor(rnd.value * (i + 1));
            var temp = newArray[i];
            newArray[i] = newArray[j];
            newArray[j] = temp;
        }
        return newArray;
    }

    // Find the table by its class.
    var table = document.querySelector("table");
    if (!table) return;
    var firstRow = table.rows[0];
    if (!firstRow) return;
    var colCount = firstRow.cells.length;
    if (colCount <= 1) return;

    // Create an array of column indices to shuffle (excluding the first column).
    var indices = [];
    for (var i = 1; i < colCount; i++) {
        indices.push(i);
    }
    // Shuffle deterministically using the stored seed.
    var shuffledIndices = shuffleArray(indices, storedSeed);

    // Apply the permutation to each row.
    for (var r = 0; r < table.rows.length; r++) {
        var row = table.rows[r];
        var firstCell = row.cells[0]; // leave first column as-is.
        var otherCells = [];
        for (var c = 1; c < colCount; c++) {
            otherCells.push(row.cells[c]);
        }
        var newCells = [firstCell];
        shuffledIndices.forEach(function(idx) {
            // Since idx is the original cell index (starting at 1), subtract 1 for our otherCells.
            newCells.push(otherCells[idx - 1]);
        });
        // Clear and reappend cells in new order.
        while (row.firstChild) {
            row.removeChild(row.firstChild);
        }
        newCells.forEach(function(cell) {
            row.appendChild(cell);
        });
    }
})();
</script>
"""


class BaseNoteType:
    """
    Base class for Anki note types.
    """

    def __init__(
        self, model_id: int, name: str, fields: list, templates: list, css: str = ""
    ):
        self.model_id = model_id
        self.name = name
        self.fields = fields
        self.templates = templates
        self.css = BASE_CSS + "\n" + css

    def create_model(self) -> genanki.Model:
        return genanki.Model(
            self.model_id,
            self.name,
            fields=self.fields,
            templates=self.templates,
            css=self.css,
        )


class TableNoteType(BaseNoteType):
    """
    A basic note type for ts_table flashcards.

    - Front: rendered as HTML.
    - Back: rendered as HTML.
    """

    def __init__(self):
        fields = [{"name": "Front"}, {"name": "Back"}]
        templates = [
            {
                "name": "ts_table",
                "qfmt": "\n".join(
                    [
                        RANDOMIZE_TABLE_COLUMS_QUESTION_SCRIPT,
                        '<div class="card">',
                        '<div class="card-content">',
                        "",
                        "{{Front}}",
                        "",
                        "</div>",
                        "</div>",
                    ]
                ),
                "afmt": "\n".join(
                    [
                        RANDOMIZE_TABLE_COLUMS_ANSWER_SCRIPT,
                        '<div class="card">',
                        '<div class="card-content">',
                        "",
                        "{{Back}}",
                        "",
                        "</div>",
                        "</div>",
                    ]
                ),
            }
        ]
        # You can add note-type–specific CSS here if desired.
        specific_css = """
/* Table styling */
table {
  border-collapse: collapse;
  margin: 0 auto;            /* Center the table horizontally */
  width: auto;               /* Table fits content rather than filling width */
  table-layout: auto;        /* Auto layout so columns fit their content */
  border: none;              /* no explicit border on the table itself */
}

th, td {
  border: 2px solid #6e738d; /* Overlay0 */
  white-space: pre-wrap;
}

.table_body {
  text-align: center;
  padding: 12px;
  background-color: #494d64; /* Surface1 */
}

.table_corner {
  border: none;               /* no explicit border on the table itself */
  background-color: #24273a;  /* Base */
}

.table_header_top {
  text-align: center;
  background-color: #363a4f; /* Surface0 */
}

.table_header_left {
  text-align: right;
  background-color: #363a4f; /* Surface0 */
}

/* Remove top border from first row */
table tr:first-child th,
table tr:first-child td {
  border-top: none;
}

/* Remove bottom border from last row */
table tr:last-child th,
table tr:last-child td {
  border-bottom: none;
}

/* Remove left border from first cell in every row */
table tr th:first-child,
table tr td:first-child {
  border-left: none;
}

/* Remove right border from last cell in every row */
table tr th:last-child,
table tr td:last-child {
  border-right: none;
}
        """
        # Ensure the model ID is unique.
        super().__init__(
            model_id=1607392319,
            name="ts_table",
            fields=fields,
            templates=templates,
            css=specific_css,
        )
