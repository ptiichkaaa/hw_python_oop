class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type, duration, distance, speed, calories):
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
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MIN_IN_HOUR: float = 60
    
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action # число шагов
        self.duration = duration # длительность тренировки
        self.weight = weight # вес спортсмена   
                
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
    coeff_calorie_1 = 18
    coeff_calorie_2 = 20
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action # число шагов
        self.duration = duration # длительность тренировки
        self.weight = weight # вес спортсмена  
            
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.coeff_calorie_1 * self.get_mean_speed() 
            - self.coeff_calorie_2) * self.weight / self.M_IN_KM 
            * self.duration * self.MIN_IN_HOUR
        )
        

class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_calorie_1 = 0.035
    coeff_calorie_2 = 0.029
    def __init__(self, action: int, 
                duration: float, # длительность тренировки
                weight: float, # вес спортсмена  
                height: float # рост спортсмена  
                ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

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
    LEN_STEP = 1.38
    M_IN_KM = 1000
    def __init__(self, action: int, # число гребков
                duration: float, # длительность тренировки
                weight: float, # вес спортсмена
                length_pool: float, # длина бассейна в метрах
                count_pool: float # сколько раз пользователь переплыл бассейн
                ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP / self.M_IN_KM)
       
    def get_mean_speed(self)-> float:
        """Получить среднюю скорость движения."""
        speed_swimming = (self.length_pool * self.count_pool / self.M_IN_KM / self.duration)
        return speed_swimming
        
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        self.coeff_calorie_1 = 1.1
        self.coeff_calorie_2 = 2
        speed_swimming = (self.length_pool * self.count_pool / self.M_IN_KM / self.duration) # средняя скорость при плавании
        return (speed_swimming + 1.1) * 2 * self.weight
     
    
def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout: dict = {'SWM': Swimming,
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

