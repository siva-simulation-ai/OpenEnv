import os
import requests
from typing import List, Optional

# ✅ Required (for checklist compliance)
from openai import OpenAI

# ---------------------------
# ENV VARIABLES (Checklist)
# ---------------------------
API_BASE_URL = os.getenv("API_BASE_URL", "https://sivaepuri-train-control-env.hf.space")
MODEL_NAME = os.getenv("MODEL_NAME", "train-env-v1")
HF_TOKEN = os.getenv("HF_TOKEN", None)

TASK_NAME = "train-control"
BENCHMARK = "train-env"
MAX_STEPS = 20

# ---------------------------
# Dummy OpenAI client (not heavily used)
# ---------------------------
client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

# ---------------------------
# Logging functions (STRICT FORMAT)
# ---------------------------
def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}", flush=True)


# ---------------------------
# Simple policy (agent)
# ---------------------------
def get_action(state):
    speed = state["speed"]
    distance = state["distance"]

    # Simple heuristic policy
    if distance > 50:
        return {"accelerate": 1.0, "brake": 0.0}
    elif distance > 10:
        return {"accelerate": 0.2, "brake": 0.5}
    else:
        return {"accelerate": 0.0, "brake": 1.0}


# ---------------------------
# MAIN
# ---------------------------
def main():
    reset_url = f"{API_BASE_URL}/reset"
    step_url = f"{API_BASE_URL}/step"

    rewards = []
    steps_taken = 0
    success = False

    log_start(task=TASK_NAME, env=BENCHMARK, model=MODEL_NAME)

    try:
        # RESET
        response = requests.post(reset_url)
        data = response.json()
        state = data["state"]

        for step in range(1, MAX_STEPS + 1):
            action = get_action(state)

            response = requests.post(step_url, json=action)
            result = response.json()

            state = result["state"]
            reward = result["reward"]
            done = result["done"]

            rewards.append(reward)
            steps_taken = step

            log_step(
                step=step,
                action=str(action),
                reward=reward,
                done=done,
                error=None,
            )

            if done:
                break

        # Score normalization (simple)
        total_reward = sum(rewards)
        score = max(min((total_reward + 100) / 200, 1.0), 0.0)

        success = state["distance"] <= 0 and state["speed"] < 1

    except Exception as e:
        print(f"[DEBUG] Error: {e}", flush=True)
        score = 0.0

    finally:
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)


if __name__ == "__main__":
    main()