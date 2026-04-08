from fastapi import FastAPI
from my_env.env import TrainEnv, TrainAction

app = FastAPI(
    title="Train Control RL Environment",
    docs_url="/docs",
    openapi_url="/openapi.json",
)

env = TrainEnv()

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/reset")
def reset():
    state = env.reset()
    return {
        "state": state.dict() if hasattr(state, "dict") else state,
        "reward": 0,
        "done": False
    }

@app.post("/step")
def step(action: TrainAction):
    state, reward, done, _ = env.step(action)
    return {
        "state": state.dict() if hasattr(state, "dict") else state,
        "reward": reward,
        "done": done
    }

def main():
    return app
