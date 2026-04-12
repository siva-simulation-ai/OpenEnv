from fastapi import FastAPI
from my_env.env import TrainEnv, TrainAction

app = FastAPI()

env = TrainEnv()

@app.get("/")
def root():
    return {"status": "OK"}

@app.post("/reset")
def reset():
    state = env.reset()
    return {
        "state": state.__dict__,
        "reward": 0,
        "done": False
    }

@app.post("/step")
def step(action: TrainAction):
    state, reward, done, _ = env.step(action)
    return {
        "state": state.__dict__,
        "reward": reward,
        "done": done
    }
