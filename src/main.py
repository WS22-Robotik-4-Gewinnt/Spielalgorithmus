import json

from algos import Minimax

import uvicorn
import requests
from fastapi import FastAPI
from pydantic import BaseModel

#########################
# 6 0  0  0  0  0  0  0 #
# 5 0  0  0  0  0  0  0 #
# 4 0  0  0  0  0  0  0 #
# 3 h  0  0  r  0  0  0 #
# 2 h  r  r  h  r  0  r #
# 1 h  h  h  r  h  r  r #
# # 1  2  3  4  5  6  7 #

# h = Human Player | r = Robot Player | 0 = empty space

# Feld={ "Column1": [{"Row1":"h"}, {"Row2":"h"}, {"Row3":"h"}, {"Row4":"r"}, {"Row5":"h"}, {"Row6":"r"}],
#        "Column2": [{"Row1":"h"}, {"Row2":"h"}, {"Row3":"h"}, {"Row4":"r"}, {"Row5":"h"}, {"Row6":"r"}],
#        "Column3": [{"Row1":"h"}, {"Row2":"h"}, {"Row3":"h"}, {"Row4":"r"}, {"Row5":"h"}, {"Row6":"r"}],
#        "Column4": [{"Row1":"h"}, {"Row2":"h"}, {"Row3":"h"}, {"Row4":"r"}, {"Row5":"h"}, {"Row6":"r"}],
#        "Column5": [{"Row1":"h"}, {"Row2":"h"}, {"Row3":"h"}, {"Row4":"r"}, {"Row5":"h"}, {"Row6":"r"}],
#        "Column6": [{"Row1":"h"}, {"Row2":"h"}, {"Row3":"h"}, {"Row4":"r"}, {"Row5":"h"}, {"Row6":"r"}]
# }

ROWS = 6
COLUMNS = 7


class Column(BaseModel):
    Row1: str
    Row2: str
    Row3: str
    Row4: str
    Row5: str
    Row6: str


class Board(BaseModel):
    Column1: Column
    Column2: Column
    Column3: Column
    Column4: Column
    Column5: Column
    Column6: Column
    Column7: Column


app = FastAPI()

board = [["0"] * 7 for i in range(6)]

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/findNextMove")
async def calculateMove():
    return {"col": 5, "row": 3}


@app.post("/updateBoard")
async def updateBoard(newBoard: Board):
    # import board
    pb = newBoard

    # convert to internal format
    board[0] = [pb.Column1.Row1, pb.Column2.Row1, pb.Column3.Row1, pb.Column4.Row1,
                pb.Column5.Row1, pb.Column6.Row1, pb.Column7.Row1]
    board[1] = [pb.Column1.Row2, pb.Column2.Row2, pb.Column3.Row2, pb.Column4.Row2,
                pb.Column5.Row2, pb.Column6.Row2, pb.Column7.Row2]
    board[2] = [pb.Column1.Row3, pb.Column2.Row3, pb.Column3.Row3, pb.Column4.Row3,
                pb.Column5.Row3, pb.Column6.Row3, pb.Column7.Row3]
    board[3] = [pb.Column1.Row4, pb.Column2.Row4, pb.Column3.Row4, pb.Column4.Row4,
                pb.Column5.Row4, pb.Column6.Row4, pb.Column7.Row4]
    board[4] = [pb.Column1.Row5, pb.Column2.Row5, pb.Column3.Row5, pb.Column4.Row5,
                pb.Column5.Row5, pb.Column6.Row5, pb.Column7.Row5]
    board[5] = [pb.Column1.Row6, pb.Column2.Row6, pb.Column3.Row6, pb.Column4.Row6,
                pb.Column5.Row6, pb.Column6.Row6, pb.Column7.Row6]

    # run minimax
    mini = Minimax.Minimax(board)
    moveCol, moveRow = mini.mini_max(board, 4, True)

    # send move to robot service
    # r = requests.post('http://localhost:8096/move', "ok", {"col": moveCol, "row": moveRow})

    return {"col": moveCol, "val": moveRow}


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")
