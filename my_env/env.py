from dataclasses import dataclass

# ---------------------------
# State
# ---------------------------
@dataclass
class TrainState:
    speed: float
    distance: float

from pydantic import BaseModel

class TrainAction(BaseModel):
    accelerate: float
    brake: float


# ---------------------------
# Action
# ---------------------------
@dataclass
class TrainAction:
    accelerate: float
    brake: float


# ---------------------------
# Environment
# ---------------------------
class TrainEnv:

    def __init__(self):
        self.max_speed = 15
        self.station_distance = 100
        self.reset()

    def reset(self):
        self.speed = 0.0
        self.distance = self.station_distance
        return TrainState(speed=self.speed, distance=self.distance)

    def step(self, action: TrainAction):

        # ---------------------------
        # 1. Apply action
        # ---------------------------
        self.speed += action.accelerate
        self.speed -= action.brake

        # Clamp speed
        if self.speed < 0:
            self.speed = 0
        if self.speed > self.max_speed:
            self.speed = self.max_speed

        # ---------------------------
        # 2. Update distance
        # ---------------------------
        self.distance -= self.speed

        # ---------------------------
        # 3. Base reward
        # ---------------------------
        reward = -1  # time penalty (encourage faster completion)

        # ---------------------------
        # 4. Energy efficiency penalty
        # ---------------------------
        reward -= 0.1 * self.speed

        # ---------------------------
        # 5. Idle penalty (important)
        # ---------------------------
        if self.speed == 0:
            reward -= 0.5

        # ---------------------------
        # 6. Speed limit near station
        # ---------------------------
        if self.distance < 50 and self.speed > 5:
            reward -= 5  # unsafe high speed near station

        # ---------------------------
        # 7. Overspeed penalty
        # ---------------------------
        if self.speed >= self.max_speed:
            reward -= 2

        # ---------------------------
        # 8. Unnecessary braking penalty
        # ---------------------------
        if self.speed == 0 and action.brake > action.accelerate:
            reward -= 0.5

        # ---------------------------
        # 9. Smooth approach reward
        # ---------------------------
        if 0 < self.distance < 20 and self.speed < 3:
            reward += 2  # encourage slow approach

        # ---------------------------
        # 10. Terminal conditions
        # ---------------------------
        if self.distance <= 0:
            done = True

            # Perfect stop
            if self.speed < 1:
                reward += 200  # BIG reward for perfect stop

            # Slight overshoot but controllable
            elif self.speed < 3:
                reward += 20  # partial success

            # Crash / overshoot
            else:
                reward -= 100

        else:
            done = False

        return TrainState(self.speed, self.distance), reward, done, {}