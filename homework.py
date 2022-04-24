from dataclasses import dataclass, asdict
from typing import Type, Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE = (
        'Тип тренировки: {training_type}; Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action          # число шагов
        self.duration: float = duration    # длительность тренировки
        self.weight: float = weight        # вес спортсмена

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            training_type=self.__class__.__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1: float = 18
    coeff_calorie_2: float = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action           # число шагов
        self.duration: float = duration     # длительность тренировки
        self.weight: float = weight         # вес спортсмена

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.coeff_calorie_1
                * self.get_mean_speed()
                - self.coeff_calorie_2)
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.MIN_IN_HOUR
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_calorie_1: float = 0.035
    coeff_calorie_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,           # длительность тренировки
                 weight: float,             # вес спортсмена
                 height: float              # рост спортсмена
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        return (
            (self.coeff_calorie_1 * self.weight
             + (self.get_mean_speed()**2 // self.height)
             * self.coeff_calorie_2 * self.weight) * self.MIN_IN_HOUR
            * self.duration
        )


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    M_IN_KM: int = 1000
    coeff_calorie_1: float = 1.1
    coeff_calorie_2: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: int = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed_swimming = (self.length_pool
                          * self.count_pool
                          / self.M_IN_KM
                          / self.duration
                          )
        return speed_swimming

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        speed_swimming = (self.length_pool
                          * self.count_pool
                          / self.M_IN_KM
                          / self.duration
                          )  # средняя скорость при плавании
        return (
            (speed_swimming
             + self.coeff_calorie_1)
            * self.coeff_calorie_2
            * self.weight
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout: Dict[str, Type[Training]] = {'SWM': Swimming,
                                          'RUN': Running,
                                          'WLK': SportsWalking}
    if workout_type not in workout:
        raise ValueError(f'Не известный {workout_type},'
                         f' тип тренировки!')
    return workout[workout_type](*data)


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