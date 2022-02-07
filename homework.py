class InfoMessage:
    """Информационное сообщение о тренировке."""
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
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000  # meters in kilometer
    LEN_STEP = 0.65  # one step lenght
    MIN_IN_H = 60  # minutes in hour

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        avg_speed = self.get_distance() / self.duration
        return avg_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    workout_type = 'RUN'
    cf_run_1 = 18  # calorie coefficient while running
    cf_run_2 = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        spent_calories = ((self.cf_run_1 * self.get_mean_speed()
                          - self.cf_run_2) * self.weight / self.M_IN_KM
                          * (self.duration * self.MIN_IN_H))
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    workout_type = 'WLK'
    cf_wlk_1 = 0.035  # calorie coefficient while sportswalking
    cf_wlk_2 = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        spent_calories = ((self.cf_wlk_1 * self.weight
                          + (self.get_mean_speed()**2 // self.height)
                          * self.cf_wlk_2 * self.weight)
                          * self.duration * self.MIN_IN_H)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    workout_type = 'SWM'
    LEN_STEP = 1.38  # length of one stroke
    cf_swm_1 = 1.1  # calorie coefficient while swimming
    cf_swm_2 = 2

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
        avg_speed = (self.length_pool * self.count_pool
                     / self.M_IN_KM / self.duration)
        return avg_speed

    def get_spent_calories(self) -> float:
        spent_calories = ((self.get_mean_speed() + self.cf_swm_1)
                          * self.cf_swm_2 * self.weight)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    activities: dict[str, training] = {'RUN': Running,
                                       'WLK': SportsWalking,
                                       'SWM': Swimming}
    if workout_type in activities:
        return activities[workout_type](*data)
    else:
        return None


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
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
