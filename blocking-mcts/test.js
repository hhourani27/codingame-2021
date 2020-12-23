const N = 20000
let startTime = process.hrtime.bigint()
testStringArray(N);
let endTime = process.hrtime.bigint() - startTime;
console.log(endTime);

startTime = process.hrtime.bigint()
testIntArray(N);
endTime = process.hrtime.bigint() - startTime;
console.log(endTime);

function testStringArray(iterations) {
  for (let n = 0; n < iterations; n++) {
    const board = [];
    for (let i = 0; i < 13; i++) {
      board[i] = [];
      for (let j = 0; j < 13; j++) {
        board[i][j] = '.'
      }
    }

    for (let i = 0; i < 13; i++) {
      for (let j = 0; j < 13; j++) {
        if (board[i][j] === '.')
          board[i][j] = '#'
      }
    }
  }
}

function testIntArray(iterations) {
  for (let n = 0; n < iterations; n++) {
    const board = [];
    for (let i = 0; i < 13; i++) {
      board[i] = [];
      for (let j = 0; j < 13; j++) {
        board[i][j] = -1;
      }
    }

    for (let i = 0; i < 13; i++) {
      for (let j = 0; j < 13; j++) {
        if (board[i][j] == -1)
          board[i][j] = 0;
      }
    }
  }
}