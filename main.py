import reactpy as rp
import asyncio
from solver import is_valid_soduku,  solve_with_steps

# ReactPy Sudoku App

@rp.component
def SudokuApp():
    # Initialize a 9x9 grid with empty values
    initial_board = [['' for _ in range(9)] for _ in range(9)]
    initial_flag = [[False for _ in range(9)] for _ in range(9)]
    board, set_board = rp.hooks.use_state(initial_board)
    flag, set_flag = rp.hooks.use_state(initial_flag)
    error_message, set_error_message = rp.hooks.use_state("")
    solving, set_solving = rp.hooks.use_state(False)  # Add solving state


    # Handle changes in grid cells
    def handle_input_change(i, j, value):
        new_board = [row[:] for row in board]
        new_flag = [row[:] for row in flag]
        new_board[i][j] = str(value)
        if str(value) != '':
            new_flag[i][j] = True
        else:
            new_flag[i][j] = False
        set_board(new_board)
        set_flag(new_flag)

    async def animate_solver():
        solver = solve_with_steps(board)  # Initialize the generator
        for res in solver:
            set_board(res)
            await asyncio.sleep(0.005)

        solved = True
        for row in board:
            for num in row:
                if num == "":
                    solved = False
        if solved:
            set_error_message("Solved!")
        else:
            set_error_message("No Solution Found!")
        set_solving(False)

    def handle_solve(event):
        if not is_valid_soduku(board):
            set_error_message("Invalid Input")
            return
        set_solving(True)

    # Effect to start animation when solving starts
    def start_animation():
        if solving:
            asyncio.create_task(animate_solver())

    rp.hooks.use_effect(lambda: start_animation(), [solving])

    def handle_reset(event):
        set_board(initial_board)
        set_flag(initial_flag)
        set_error_message("")
        set_solving(False)

    return rp.html.div(
        {
            "style": {
                "display": "flex",
                "flexDirection": "column",
                "alignItems": "center",
                "fontFamily": "Arial, sans-serif",
                "padding": "20px"
            }
        },
        # Header
        rp.html.h2({"style": {"marginBottom": "10px"}}, "Sudoku Solver"),
        # Sudoku Grid
        rp.html.div(
            {
                "style": {
                    "display": "grid",
                    "gridTemplateColumns": "repeat(9, 40px)",
                    "gridTemplateRows": "repeat(9, 40px)",
                    "border": "2px solid black",
                    "boxSizing": "border-box"
                }
            },
            # Render each cell as an input
            [
                rp.html.input(
                    {
                        "value": board[i][j],
                        "onChange": lambda event, i=i, j=j: handle_input_change(i, j, event["target"]["value"]),
                        "style": {
                            "width": "100%",
                            "height": "100%",
                            "textAlign": "center",
                            "fontSize": "20px",
                            "boxSizing": "border-box",
                            "color": "red" if flag[i][j] else "black"
                        },
                    }
                )
                for i in range(9) for j in range(9)
            ]
        ),
        # instructions below the grid
        rp.html.p({"style": {"marginTop": "15px"}}, error_message),
        rp.html.p({"style": {"marginTop": "15px"}}, "Instructions: Click on a cell to enter a number and hit 'Solve' to solve the puzzle."),
        rp.html.div(
            {"style": {"display": "flex", "gap": "10px", "marginTop": "10px"}},
            rp.html.button({"onClick": handle_solve, "style": {"padding": "10px 20px"}}, "Solve"),
            rp.html.button({"onClick": handle_reset, "style": {"padding": "10px 20px"}}, "Clear")
        )
    )

rp.run(SudokuApp)