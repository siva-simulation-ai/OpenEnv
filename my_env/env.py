from dataclasses import dataclass

# State
@dataclass
class TrainState:
    speed: float
    distance: float

# Action
@dataclass
class TrainAction:
    accelerate: float
    brake: float

class TrainEnv:

    def __init__(self):
        self.speed = 0
        self.distance = 100  # meters to station

    def reset(self):
        self.speed = 0
        self.distance = 100
        return TrainState(speed=self.speed, distance=self.distance)

    def step(self, action: TrainAction):
        # Update speed
        self.speed += action.accelerate
        self.speed -= action.brake

        # Clamp speed
        if self.speed < 0:
            self.speed = 0

        # Update distance
        self.distance -= self.speed

        # Reward logic
        reward = -1  # step penalty

        # Enhancement 1: Speed limit near station
        if self.distance < 50 and self.speed > 5:
            reward -= 5

        # Enhancement 2: Energy penalty
        reward -= 0.1 * self.speed

        # Enhancement 3: Smooth Braking Bonus
        if self.distance <= 0 and self.speed < 1:
            reward += 150  # perfect stop bonus

        # Prevent unrealistic high speed
        if self.speed > 15:
            reward -= 10

        # Prevent braking when already stopped
        if self.speed == 0 and action.brake > action.accelerate:
            reward -= 0.5  # small penalty for unnecessary braking

        # Success/failure condition
        if self.distance <= 0:
            if self.speed < 1:
                reward += 150  # smooth stop bonus
            else:
                reward = -100  # overshoot crash
            done = True
        else:
            done = False

        return TrainState(self.speed, self.distance), reward, done, {}