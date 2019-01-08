from datetime import datetime, timedelta

from bamboo.models import Training


class Trainings(object):
    __NUMBER_OF_DAYS = 8

    def __init__(self):
        self.now_date = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        self.trainings = self.__get_trainings()

    def __get_trainings(self):
        start = self.now_date
        stop = self.now_date + timedelta(days=self.__NUMBER_OF_DAYS + 1)
        return Training.query.filter(Training.start >= start, Training.stop < stop).order_by('start')

    def to_table(self):
        table = [self.__set_data(i) for i in range(self.__NUMBER_OF_DAYS)]
        for training in self.trainings:
            i = training.start.day - self.now_date.day
            table[i]['trainings'].append(training.to_json())
        empty_days = []
        for i in range(len(table)):
            if not table[i]['trainings']:
                empty_days.append(i)
        for i, index in enumerate(empty_days):
            del table[index - i]
        return table

    def __set_data(self, i: int):
        weekday, date = (self.now_date + timedelta(days=i)).strftime('%A|%d-%m-%Y').split('|')
        return {'weekday': weekday, 'date': date, 'trainings': []}
