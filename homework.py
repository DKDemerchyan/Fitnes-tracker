'''
This project is a module for calculating and displaying complete
training information based on data from the sensor unit.
Designed on the principles of object-oriented programming (OOP).
'''


class InfoMessage:
    """Informational message on training."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Type of training: {self.training_type}; '
                f'Duration: {self.duration:.3f} h; '
                f'Distance: {self.distance:.3f} km; '
                f'Average speed: {self.speed:.3f} km/h; '
                f'Kcal spent: {self.calories:.3f}.')


class Training:
    """Basic training class."""
    M_IN_KM: float = 1000
    LEN_STEP: float = 0.65
    MIN_IN_H: float = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Get distance in km."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Get average speed."""
        avg_speed: float = self.get_distance() / self.duration
        return avg_speed

    def get_spent_calories(self) -> float:
        """Get the number of calories consumed."""
        raise NotImplementedError('To implement in trainings')

    def show_training_info(self) -> InfoMessage:
        """Return an informational message about the completed training."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Training type: running."""
    CALORIES_RUN_MULTIPLIER: float = 18
    CALORIES_RUN_SHIFT: float = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        spent_calories: float = ((self.CALORIES_RUN_MULTIPLIER
                                 * self.get_mean_speed()
                                 - self.CALORIES_RUN_SHIFT)
                                 * self.weight / self.M_IN_KM
                                 * (self.duration * self.MIN_IN_H))
        return spent_calories


class SportsWalking(Training):
    """Training type: sports walking."""
    CALORIES_SPWALKING_MULTIPLIER: float = 0.035
    CALORIES_SPWALKING_SHIFT: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        spent_calories: float = ((self.CALORIES_SPWALKING_MULTIPLIER
                                 * self.weight
                                 + (self.get_mean_speed()**2 // self.height)
                                 * self.CALORIES_SPWALKING_SHIFT * self.weight)
                                 * self.duration * self.MIN_IN_H)
        return spent_calories


class Swimming(Training):
    """Training type: swimming"""
    LEN_STEP: float = 1.38
    CALORIES_SWIM_MULTIPLIER: float = 1.1
    CALORIES_SWIM_SHIFT: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        avg_speed: float = (self.length_pool * self.count_pool
                            / self.M_IN_KM / self.duration)
        return avg_speed

    def get_spent_calories(self) -> float:
        spent_calories: float = ((self.get_mean_speed()
                                 + self.CALORIES_SWIM_MULTIPLIER)
                                 * self.CALORIES_SWIM_SHIFT * self.weight)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Read the data received from the sensors."""
    activities: dict[str, training] = {'RUN': Running,
                                       'WLK': SportsWalking,
                                       'SWM': Swimming}
    if workout_type in activities:
        return activities[workout_type](*data)
    else:
        return None


def main(training: Training) -> None:
    """Main function."""
    info: str = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
