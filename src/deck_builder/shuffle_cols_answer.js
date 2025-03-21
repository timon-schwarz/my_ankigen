(function () {
  // Load random seed from question
  var storageKey = "randomSeed";
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
    shuffledIndices.forEach(function (idx) {
      // Since idx is the original cell index (starting at 1), subtract 1 for our otherCells.
      newCells.push(otherCells[idx - 1]);
    });
    // Clear and reappend cells in new order.
    while (row.firstChild) {
      row.removeChild(row.firstChild);
    }
    newCells.forEach(function (cell) {
      row.appendChild(cell);
    });
  }
})();
