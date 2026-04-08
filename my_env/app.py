from fastapi import FastAPI
from my_env.env import TrainEnv, TrainAction

app = FastAPI()

env = TrainEnv()

@app.get("/")
def root():
    return {"status": "WORKING FINAL"}

# ✅ FIXED RESET
@app.post("/reset")
def reset():
    state = env.reset()
    return {
        "observation": state.__dict__
    }

# ✅ FIXED STEP
@app.post("/step")
def step(action: TrainAction):
    state, reward, done, _ = env.step(action)
    return {
        "observation": state.__dict__,
        "reward": reward,
        "done": done
    }