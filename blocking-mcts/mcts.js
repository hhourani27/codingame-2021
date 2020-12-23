// TODO: there's a diff between codingame's allowed moves and my allowed moves

const fs = require('fs');


// Game constants
const BOARD_SIZE = 13;
const NB_PLAYERS = 2;
const BLOCKS = getBlocks(NB_PLAYERS);

const MCTS_TIME_CONSTRAINT = 2000;

// Init game helper information
// {shape(LTRV): [maxValue, sw, sh, sdefHash, sdefN, shiftw, shifth]}
let SHAPES = {};
for (let block of BLOCKS) {
  SHAPES = { ...SHAPES, ...computeShapeDefinitions(block) }
}

const initialState = initializeState(NB_PLAYERS, BLOCKS)

const root = {
  state: initialState,
  Q: 0,
  N: 0,
  fullyExpanded: false, // All the children of this node have been visited
  expanded: false, // All the children of this node have been created and are ready to be visited
  visited: false, // A simulation started at this node
  simulated: true, // This node was part of a simulation
  leaf: false,
  parent: null
}

monte_carlo_tree_search(root, MCTS_TIME_CONSTRAINT);

printTree(root);

console.log('===END====');

//#region Monte Carlo Tree Search
function monte_carlo_tree_search(root, timeConstraint) {
  let startTime = process.hrtime.bigint()

  while ((process.hrtime.bigint() - startTime) < timeConstraint * 1000000) {
    console.count('loop');
    const node = traverse(root);
    const simulation_winners = simulate(node);
    backpropagate(node, simulation_winners);
  }
}

function traverse(node) {
  let _node = node;

  // If node is fully expanded, descend the game tree (by best uct) to find the next node
  while (_node.fullyExpanded) {
    _node = best_uct(_node);
  }

  // Expand node if it is not already expanded
  if (!_node.expanded) {
    _node.children = expand(_node);
    _node.expanded = true;
  }

  //Pick a children at random
  if (!_node.leaf) { // if it is not a leaf
    const unvisitedChildren = _node.children.filter(c => c.visited == false);
    const pickedUnvisitedChild = pickRandomElement(unvisitedChildren);
    pickedUnvisitedChild.visited = true;

    // Check if node became fully expanded
    if (_node.children.every(c => c.visited == true)) _node.fullyExpanded = true;

    return pickedUnvisitedChild;
  }
  else {
    return node;
  }
}

function best_uct(node) {
  const uctScores = node.children.map(child => uct(child));

  const maxUctScore = Math.max(...uctScores);
  const bestChild = node.children[uctScores.indexOf(maxUctScore)];
  return bestChild;
}

function uct(node) {
  const exploitationComponent = node.Q / node.N;
  //  const c = Math.SQRT2;
  const c = 0;
  const explorationComponent = Math.sqrt(Math.log(node.parent.N) / node.N);
  const uct = exploitationComponent + c * explorationComponent;
  return uct;
}

function simulate(node) {
  console.log('Start simulation');
  let _node = node;
  //Go down fast on the game tree until the end
  while (!_node.leaf) {
    _node.simulated = true;

    const child = pickNextNode(_node);
    if (!child) break;
    else _node = child;
  }

  // Return the winners
  const finalScores = _node.state.players.map(p => p.score);
  const maxScore = Math.max(...finalScores);
  const winningPlayers = _node.state.players.filter(p => p.score == maxScore);

  return winningPlayers.map(p => p.id);
}

function backpropagate(node, winners) {

  //update stats
  node.N += 1;
  if (winners.includes(node.state.playerId)) {
    node.Q += 1;
  }

  // if root, stop back propagating
  if (node.parent == null) return;
  //else backpropagate to its parent
  backpropagate(node.parent, winners);
}


//#endregion

//#region Board functions
function createBoard() {
  const board = [];
  for (let i = 0; i < BOARD_SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < BOARD_SIZE; j++) {
      board[i][j] = '.'
    }
  }
  return board
}

function getCorners(board, i, j) {
  const corners = [];
  if ((i - 1) >= 0 && (j - 1) >= 0) corners.push(board[i - 1][j - 1]);
  if ((i - 1) >= 0 && (j + 1) < BOARD_SIZE) corners.push(board[i - 1][j + 1]);
  if ((i + 1) < BOARD_SIZE && (j - 1) >= 0) corners.push(board[i + 1][j - 1]);
  if ((i + 1) < BOARD_SIZE && (j + 1) < BOARD_SIZE) corners.push(board[i + 1][j + 1]);

  return corners;
}

function getSides(board, i, j) {
  const sides = [];
  if (i - 1 >= 0) sides.push(board[i - 1][j]);
  if (i + 1 < BOARD_SIZE) sides.push(board[i + 1][j]);
  if (j - 1 >= 0) sides.push(board[i][j - 1]);
  if (j + 1 < BOARD_SIZE) sides.push(board[i][j + 1]);

  return sides;
}


// returns a new board with shape on it
// if shape is placed on an occupied cell, or touched the side of another shape, return null
function placeShapeOnBoard(move, board, playerIds) {
  const [x, y, shape] = move;
  const shapeInfo = SHAPES[shape];
  const [maxValue, sw, sh, sdefHash, sdefN, shiftw, shifth] = shapeInfo

  const sdefIds = sdefHash.split('#').join(playerIds);
  const _board = copyBoard(board);

  for (let i = 0; i < sdefIds.length; i++) {
    const _x = x + i % sw - shiftw;
    const _y = y + Math.floor(i / sw) - shifth;

    if (_x < 0 || _x >= BOARD_SIZE || _y < 0 || y >= BOARD_SIZE) return null;
    if (_board[_x][_y] != '.') return null;


    if (sdefIds.charAt(i) === playerIds) {
      if (getSides(board, _x, _y).includes(playerIds)) return null;
    }
    _board[_x][_y] = sdefIds.charAt(i);
  }
  return _board;
}

function copyBoard(board) {
  const _board = [];
  for (let i = 0; i < BOARD_SIZE; i++) {
    _board[i] = [];
    for (let j = 0; j < BOARD_SIZE; j++) {
      _board[i][j] = board[i][j]
    }
  }
  return _board
}

function printBoard(board) {
  const _board = transpose(board);
  _board.map(col => console.log(col.join(' ')));
}

function transpose(board) {
  _board = [];
  for (let i = 0; i < boardSize; i++) _board[i] = []

  for (let i = 0; i < boardSize; i++) {
    for (let j = 0; j < boardSize; j++) {
      _board[i][j] = board[j][i].slice()
    }
  }
  return _board;
}

//#endregion

//#region State functions

// return null if this node has no children or is a terminal node
function expand(node) {
  //compute the node's children and return them
  const nextStates = computeNextStates(node.state);
  //if it's a terminal node after all, mark it as such and return null
  if (nextStates.length == 0) {
    node.leaf = true;
    return null;
  }

  const children = nextStates.map(s => ({
    state: s,
    Q: 0,
    N: 0,
    fullyExpanded: false,
    expanded: false,
    visited: false,
    simulated: false,
    leaf: false,
    parent: node,
    children: [],
  }));
  node.children = children;

  return children;
}

function computeNextStates(prevState) {
  const turn = prevState.turn + 1;

  for (let i = 1; i <= NB_PLAYERS; i++) {
    const playerId = (prevState.playerId + i) % NB_PLAYERS
    const player = prevState.players[playerId];
    const moves_boards = computeMoves(turn, player.ids, player.blocks, prevState.board);
    if (moves_boards.length == 0) continue;

    return moves_boards.map(mvb => {
      const [move, board] = mvb
      const state = {};
      state.turn = turn;
      state.status = 'RUN';
      state.board = board;
      state.players = clone(prevState.players);
      state.playerId = playerId;
      state.move = move;
      state.playedMoves = [...prevState.playedMoves, [playerId, move]];

      const playedShape = move[2]
      state.players[playerId].score += SHAPES[playedShape][0];

      const playedBlock = move[2].charAt(0);
      state.players[playerId].blocks.splice(state.players[playerId].blocks.indexOf(playedBlock), 1);

      return state;
    })
  }

  return [];
}

function computeMoves(turn, playerIds, playerBlocks, board) {
  const allowedCells = computeAllowedCells(turn, playerIds, board);
  if (allowedCells.length == 0) return [];

  const allowedBlocks = computeAllowedBlocks(turn, playerIds, playerBlocks);
  if (allowedBlocks.length == 0) return [];

  const allowedShapes = computeAllowedShapes(allowedBlocks);

  const allowedMoves_boards = [];

  for (const [i, j] of allowedCells) {
    for (const shape of allowedShapes) {
      const move = [i, j, shape];
      const _board = placeShapeOnBoard(move, board, playerIds);
      if (_board) allowedMoves_boards.push([move, _board]);
    }
  }

  return allowedMoves_boards;
}

function pickNextNode(node) {
  console.log('Pick next node in simulation')
  const nextState = pickNextState(node.state);
  if (!nextState) {
    node.leaf = true;
    return null;
  }

  const child = {
    state: nextState,
    Q: 0,
    N: 0,
    fullyExpanded: false,
    expanded: false,
    visited: false,
    simulated: false,
    leaf: false,
    parent: node,
    children: []
  }
  node.children.push(child);
  return child;
}

function pickNextState(prevState) {
  console.log('Pick next state in simulation')
  const turn = prevState.turn + 1;

  for (let i = 1; i <= NB_PLAYERS; i++) {
    const playerId = (prevState.playerId + i) % NB_PLAYERS
    const player = prevState.players[playerId];
    const move_board = pickMove(turn, player.ids, player.blocks, prevState.board);
    if (!move_board) continue;

    const [move, board] = move_board
    const state = {};
    state.turn = turn;
    state.status = 'RUN';
    state.board = board;
    state.players = clone(prevState.players);
    state.playerId = playerId;
    state.move = move;
    state.playedMoves = [...prevState.playedMoves, [playerId, move]];

    const playedShape = move[2]
    state.players[playerId].score += SHAPES[playedShape][0];

    const playedBlock = move[2].charAt(0);
    state.players[playerId].blocks.splice(state.players[playerId].blocks.indexOf(playedBlock), 1);
    return state;
  }

  return null;
}

function pickMove(turn, playerIds, playerBlocks, board) {
  console.log('Pick next move in simulation');
  const allowedCells = computeAllowedCells(turn, playerIds, board);
  if (allowedCells.length == 0) return null;
  shuffle(allowedCells);

  const allowedBlocks = computeAllowedBlocks(turn, playerIds, playerBlocks);
  if (allowedBlocks.length == 0) return null;

  const allowedShapes = computeAllowedShapes(allowedBlocks);
  shuffle(allowedShapes);

  for (const [i, j] of allowedCells) {
    for (const shape of allowedShapes) {
      console.log('Try move');
      const move = [i, j, shape];
      const _board = placeShapeOnBoard(move, board, playerIds);
      if (_board) return [move, _board];
    }
  }

  return null;
}

function computeAllowedCells(turn, playerIds, board) {
  if (turn == 1 && playerIds === '0') return [[0, 0]];
  if (turn == 2 && playerIds === '1') return [[BOARD_SIZE - 1, BOARD_SIZE - 1]];
  if (NB_PLAYERS == 3 && turn == 3 && playerIds === '2') return [[0, BOARD_SIZE - 1]];
  if (NB_PLAYERS == 4 && turn == 4 && playerIds === '3') return [[BOARD_SIZE - 1, 0]];

  const allowedCells = [];
  for (let i = 0; i < BOARD_SIZE; i++) {
    for (let j = 0; j < BOARD_SIZE; j++) {
      if (board[i][j] === '.') {
        if (getCorners(board, i, j).includes(playerIds)) {
          if (!getSides(board, i, j).includes(playerIds)) {
            allowedCells.push([i, j])
          }
        }
      }
    }
  }

  return allowedCells;

}

function computeAllowedBlocks(turn, playerIds, playerBlocks) {
  if (NB_PLAYERS == 3) {
    if ((turn == 1 && playerIds === '0') || (turn == 2 && playerIds === '1')) {
      return ['A', 'B', 'C', 'D']
    }
  }

  return playerBlocks;
}

function computeAllowedShapes(blocks) {
  const shapes = [];

  for (shape in SHAPES) {
    for (block of blocks) {
      if (shape.startsWith(block)) {
        shapes.push(shape);
      }
    }
  }

  return shapes
}


function initializeState(NB_PLAYERS, BLOCKS) {
  const state = {};
  state.turn = 0;
  state.status = 'INIT';

  state.board = createBoard();

  state.players = []
  for (let i = 0; i < NB_PLAYERS; i++) {
    state.players.push({
      id: i,
      ids: i.toString(),
      score: 0,
      blocks: BLOCKS.map(s => s[0]),
    })
  }

  state.playerId = -1;

  state.move = null;
  state.playedMoves = [];

  return state
}

//#endregion

//#region Generate initial state
function getBlocks(NB_PLAYERS) {
  const blocks = [
    ['A', 1, 1, '#'],
    ['B', 2, 1, '##'],
    ['C', 3, 1, '###'],
    ['D', 2, 2, '###.'],
    ['E', 4, 1, '####'],
    ['F', 3, 2, '####..'],
    ['G', 3, 2, '###.#.'],
    ['H', 2, 2, '####'],
    ['I', 3, 2, '##..##'],
    ['J', 5, 1, '#####'],
    ['K', 4, 2, '#####...'],
    ['L', 4, 2, '####.#..'],
    ['M', 4, 2, '###...##'],
    ['N', 3, 2, '#####.'],
    ['O', 3, 2, '####.#'],
    ['P', 3, 3, '####..#..'],
    ['Q', 3, 3, '###.#..#.'],
    ['R', 3, 3, '##..#..##'],
    ['S', 3, 3, '##..##..#'],
    ['T', 3, 3, '##..##.#.'],
    ['U', 3, 3, '.#.###.#.']
  ];

  switch (NB_PLAYERS) {
    case 2: return blocks.slice(0, 18);
    case 3: return blocks.slice(0, 13);
    case 4: return blocks.slice(0, 10);
  }
}

// Return {shape(LTRV): [maxValue, sw, sh, sdefHash, sdefN, shiftw, shifth]}
function computeShapeDefinitions([sid, scol, srow, definition]) {
  const result = {}

  const maxValue = definition.split('').filter(c => c === '#').length

  for (let flip in [0, 1]) {
    for (let rotate in [0, 1, 2, 3]) {
      const [sw, sh, sdefHash, sdefN] = transformShape(scol, srow, toSdefN(definition), flip, rotate)
      for (let value = 1; value <= maxValue; value++) {
        const shiftw = sdefN.indexOf(value.toString()) % sw;
        const shifth = Math.floor(sdefN.indexOf(value.toString()) / sw);

        const shape = sid + flip.toString() + rotate.toString() + value.toString();

        result[shape] = [maxValue, sw, sh, sdefHash, sdefN, shiftw, shifth]
      }
    }
  }

  return result;
}

// Return [sw, sh, sdefHash, sdefN]
function transformShape(sw, sh, sdefN, flip, rotate) {
  let _sw = sw;
  let _sh = sh;
  let _sdefN = sdefN.slice();

  // Flip
  if (flip == 1) {
    let _sdefT = ''
    for (let i = 0; i < _sw; i++) {
      for (let j = 0; j < _sh; j++) {
        _sdefT += _sdefN.charAt(i + j * sw);
      }
    }
    _sdefN = _sdefT.slice();
    [_sw, _sh] = [_sh, _sw];
  }

  // Rotate
  if (rotate == 1) {
    let _sdefT = ''
    for (let i = 0; i < _sw; i++) {
      for (let j = _sh - 1; j >= 0; j--) {
        _sdefT += _sdefN.charAt(i + j * _sw);
      }
    }
    _sdefN = _sdefT.slice();
    [_sw, _sh] = [_sh, _sw];
  }
  else if (rotate == 2) {
    _sdefN = reverse(_sdefN);
  }
  else if (rotate == 3) {
    let _sdefT = ''
    for (let i = 0; i < _sw; i++) {
      for (let j = _sh - 1; j >= 0; j--) {
        _sdefT += reverse(_sdefN).charAt(i + j * _sw)
      }
    }
    _sdefN = _sdefT.slice();
    [_sw, _sh] = [_sh, _sw];
  }

  return [_sw, _sh, toSdefHash(_sdefN), _sdefN]
}

function toSdefN(sdefHash) {
  let sdefN = ''
  let n = 1
  for (let i = 0; i < sdefHash.length; i++) {
    if (sdefHash.charAt(i) === '.')
      sdefN += '.'
    else {
      sdefN += n.toString()
      n += 1
    }
  }
  return sdefN;
}

function toSdefHash(sdefN) {
  let sdefHash = ''
  for (let i = 0; i < sdefN.length; i++) {
    if (sdefN.charAt(i) === '.')
      sdefHash += '.'
    else
      sdefHash += '#'
  }

  return sdefHash;

}

function reverse(s) {
  return s.split('').reverse().join('')
}


//#endregion

//#region Utils function
function clone(obj) {
  return JSON.parse(JSON.stringify(obj))
}

function pickRandomElement(array) {
  return array[Math.floor(Math.random() * array.length)];
}

function shuffle(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
}

//#endregion

//#region Print tree
function printTree(root) {

  // Iterate through the tree
  const stack = [];
  stack.push(root)
  while (stack.length > 0) {
    const node = stack.pop();

    //modify node
    if (node.parent && node.visited) node.UCT = uct(node);
    delete node.parent;

    // add children to the stack
    if (node.children) {
      /*      node.children = node.children.filter(c => {
              if (c.parent.expanded == true) {
                if (c.visited == false) return false;
                else return true;
              }
              else return true;
            });
            */
      node.children = node.children.filter(c => c.visited == true);
      stack.push(...node.children);
    }
  }
  const outputTree = JSON.stringify(root, (key, value) => {
    if (key === 'parent') return '';
    return value;
  })
  fs.writeFile('tree.js', "data='" + outputTree + "'", 'utf8', () => {
    console.log('WROTE TREE TO FILE');
  });
}
//#endregion
