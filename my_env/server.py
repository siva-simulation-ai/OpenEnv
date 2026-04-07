from fastapi import FastAPI
from my_env.env import TrainEnv, TrainAction

app = FastAPI()

env = TrainEnv()

@app.get("/")
def home():
    return {"message": "Train RL Environment Running"}

@app.post("/reset")
def reset():
    state = env.reset()
    return state.__dict__

@app.post("/step")
def step(action: TrainAction):
    state, reward, done, _ = env.step(action)
    return {
        "state": state.__dict__,
        "reward": reward,
        "done": done
    }