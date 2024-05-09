def is_valid_move(board, row, col, color):
    if board[row][col] != 0:
        return False

    opposite_color = 1 if color == 2 else 2
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == opposite_color:
            while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == opposite_color:
                r += dr
                c += dc
            if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == color:
                return True
    return False


def mark_possible_moves(board, color):
    new_board = [row[:] for row in board]  # Create a deep copy of the board
    for i in range(len(board)):
        for j in range(len(board[0])):
            if new_board[i][j] == 3:
                new_board[i][j] = 0
            if is_valid_move(board, i, j, color):
                new_board[i][j] = 3
    return new_board



