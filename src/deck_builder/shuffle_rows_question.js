(function () {
  // Generate and store random seed
  var storageKey = "randomSeed";
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

  var rows = Array.from(table.rows);
  if (rows.length <= 1) return; // Ensure there are multiple rows to shuffle

  var header = rows.shift(); // Exclude the column header row from shuffling

  // Shuffle rows deterministically using the stored seed.
  var shuffledRows = shuffleArray(rows, storedSeed);

  // Reinsert rows in shuffled order.
  table.innerHTML = ""; // Clear table
  table.appendChild(header); // Reinsert header row
  shuffledRows.forEach(function (row) {
    table.appendChild(row);
  });
})();
