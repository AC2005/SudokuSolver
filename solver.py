import collections

def is_valid_soduku(board):
    rows = collections.defaultdict(set)
    cols = collections.defaultdict(set)
    boxes = collections.defaultdict(set)
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j].isnumeric():
                if board[i][j] in rows[i] or board[i][j] in cols[j] or board[i][j] in boxes[3 * (i // 3) + j // 3]:
                    return False
                if not board[i][j].isdigit():
                    return False
                if int(board[i][j]) <= 0 or int(board[i][j]) > 9:
                    return False
                rows[i].add(board[i][j])
                cols[j].add(board[i][j])
                boxes[3 * (i // 3) + j // 3].add(board[i][j])
            elif board[i][j] != "":
                return False
    return True


def solve_with_steps(board):
    rows = collections.defaultdict(set)
    cols = collections.defaultdict(set)
    boxes = collections.defaultdict(set)

    # store used numbers
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j].isnumeric():
                rows[i].add(board[i][j])
                cols[j].add(board[i][j])
                boxes[3 * (i // 3) + j // 3].add(board[i][j])
    res = []
    # backtracking algorithm
    def backtrack(x, y):
        nonlocal res
        if x == len(board):
            return True
        if board[x][y] == '':
            row_nums = rows[x]
            col_nums = cols[y]
            box_nums = boxes[3 * (x // 3) + y // 3]
            used_nums = row_nums.union(col_nums).union(box_nums)
            for i in range(1, 10):
                if str(i) not in used_nums:
                    board[x][y] = str(i)
                    rows[x].add(str(i))
                    cols[y].add(str(i))
                    boxes[3 * (x // 3) + (y // 3)].add(str(i))

                    res.append([row[:] for row in board])
                    # found valid number and calling next backtrack
                    if y == len(board[0]) - 1:
                        if backtrack(x + 1, 0):
                            return True
                    else:
                        if backtrack(x, y + 1):
                            return True
                    rows[x].remove(str(i))
                    cols[y].remove(str(i))
                    boxes[3 * (x // 3) + (y // 3)].remove(str(i))
                    board[x][y] = ''
                    res.append([row[:] for row in board])
        else:
            # logic to determine if algorithm should go to next row and next cell
            if y == len(board[0]) - 1:
                if backtrack(x + 1, 0):
                    return True
            else:
                if backtrack(x, y + 1):
                    return True
        return False

    backtrack(0, 0)
    return res
