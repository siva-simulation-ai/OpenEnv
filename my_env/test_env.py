from env import TrainEnv, TrainAction

env = TrainEnv()
state = env.reset()   # ✅ initialize state first

print("Initial:", state)

for i in range(30):

    # Decide action based on current state
    if state.distance < 30:
        action = TrainAction(accelerate=0.2, brake=1.0)
    else:
        action = TrainAction(accelerate=1.0, brake=0.2)

    # Take step
    state, reward, done, _ = env.step(action)

    print(f"Step {i}: {state}, Reward={reward}, Done={done}")

    if done:
        break