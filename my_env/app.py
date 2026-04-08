from fastapi import FastAPI
from my_env.env import TrainEnv, TrainAction

app = FastAPI(
    title="Train Control RL Environment",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# Debug print (will show in logs)
print("APP STARTED SUCCESSFULLY")

env = TrainEnv()

@app.get("/")
def root():
    return {"status": "WORKING FINAL"}

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