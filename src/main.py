import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.init as init
import time

from g2048 import *

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
GAME_BOARD_SIZE = 8

class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(GAME_BOARD_SIZE*GAME_BOARD_SIZE, GAME_BOARD_SIZE*GAME_BOARD_SIZE).to(DEVICE)
        self.fc2 = nn.Linear(GAME_BOARD_SIZE*GAME_BOARD_SIZE, GAME_BOARD_SIZE*GAME_BOARD_SIZE).to(DEVICE)
        self.fc3 = nn.Linear(GAME_BOARD_SIZE*GAME_BOARD_SIZE, 16).to(DEVICE)
        self.fc4 = nn.Linear(16, 4).to(DEVICE)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        x = torch.sigmoid(self.fc4(x))
        return x

class GameScoreLoss(nn.Module):
    def __init__(self):
        super(GameScoreLoss, self).__init__()
        self.loss_fn = nn.MSELoss()  # use MSE loss for regression

    def forward(self, output, score):
        score_pred = output  # use the output of the model as the predicted game score
        loss = self.loss_fn(score_pred, score)  # compute the MSE loss
        return loss

model = SimpleNN().to(DEVICE)
init.uniform_(model.fc1.weight, a=-0.5, b=0.5)
init.uniform_(model.fc2.weight, a=-0.5, b=0.5)

loss_fn = GameScoreLoss().to(DEVICE)
optimizer = optim.SGD(model.parameters(), lr=0.001)

MAX_SCORE = 0
def runModel():
    global MAX_SCORE
    game = Game2048(GAME_BOARD_SIZE)

    data = []
    print("| Running Game...")
    while not game.is_lost:
        state = game.getState()
        board = torch.tensor([i for j in state["board"] for i in j]).view(1, -1).to(model.fc1.weight.dtype).to(DEVICE)

        model_output = model(board)
        max_index = torch.argmax(model_output, dim=1).item()
        direction = ["UP", "DOWN", "LEFT", "RIGHT"][max_index]

        data.append((board, max_index, state["score"]))
        game.tick(direction)
        
        if game.score >= MAX_SCORE:
            MAX_SCORE = game.score
        # os.system("clear")
        # print("Max Score: ", MAX_SCORE, flush=False)
        # print("Current Score: ", game.score, flush=False)
        # print(game, flush=False)
        # print("Choosen Move: ", direction, flush=False)
    print("| Score: ", game.score, " | Max Score: ", MAX_SCORE)
    return data

def train_model(training_data):
    print("| Training Model...")
    for i in range(1000):
        # print("| | Shuffling... ", str(i+1).rjust(4, "0"), "/", 1000, end="       \r")
        random.shuffle(training_data)
    # print()

    count = 0
    for input, output, score in training_data:
        # print("| | Propagating... ", str(count+1).rjust(len(str(len(training_data))), "0"), "/", len(training_data), end="            \r")
        optimizer.zero_grad()
        output_pred = model(input)
        loss = loss_fn(output_pred, torch.tensor(score).type(torch.float).to(DEVICE))
        loss.backward()
        optimizer.step()
        count += 1
    # print()
    # time.sleep(1)

epoch = 0
while True:
    print("Epoch: ", epoch)
    new_data = runModel()
    train_model(new_data)
    epoch += 1