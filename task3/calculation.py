# Мы сохраняем время присутствия каждого пользователя на уроке  виде интервалов.
# В функцию передается словарь, содержащий три списка с таймстемпами (время в секундах):
# — lesson – начало и конец урока
# — pupil – интервалы присутствия ученика
# — tutor – интервалы присутствия учителя
# Интервалы устроены следующим образом – это всегда список из четного количества элементов.
# Под четными индексами (начиная с 0) время входа на урок, под нечетными - время выхода с урока.
# Нужно написать функцию, которая получает на вход словарь с интервалами и возвращает время
# общего присутствия ученика и учителя на уроке (в секундах).

tests = [
   {'data': {'lesson': [1594663200, 1594666800],
             'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
             'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
    'answer': 3117
    },
   {'data': {'lesson': [1594702800, 1594706400],
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
    'answer': 3577
    },
   {'data': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
    'answer': 3565
    },
]


class Lessons:
    def __init__(self, tests):
        self.tests = tests

    def appearance(self, intervals):
        pupil_pair = self.get_pair(intervals['pupil'])
        tutor_pair = self.get_pair(intervals['tutor'])
        lesson_pair = self.get_pair(intervals['lesson'])
        pupil_unic_pair = self.check_uniq(pupil_pair)
        tutor_unic_pair = self.check_uniq(tutor_pair)
        lesson_unic_pair = self.check_uniq(lesson_pair)
        pupil_in_tutor = self.get_coincidence(tutor_unic_pair, pupil_unic_pair)
        pupil_and_tutor_in_lesson = self.get_coincidence(lesson_unic_pair, pupil_in_tutor)
        sum_time = self.get_counting_time(pupil_and_tutor_in_lesson)

        return sum_time

    @staticmethod
    def check_uniq(check_pair):
        """вычесление отрезка временипроверка пар на нахождение
           одновременного присутствия на уроке"""
        unic_pair = []

        def check(check_pair):
            pair = []
            time_start = check_pair[0][0]
            time_end = check_pair[0][1]
            for i in check_pair[1:]:
                if (i[0] < time_start) & (i[1] > time_start):
                    time_start = i[0]
                elif (i[1] > time_end) & (i[0] < time_end):
                    time_end = i[1]
                elif (i[0] > time_end) or (i[1] < time_start):
                    if i not in pair:
                        pair.append(i)
            if [time_start, time_end] not in unic_pair:
                unic_pair.append([time_start, time_end])
            if len(pair) > 0:
                check(pair)

            return unic_pair

        return check(check_pair)

    @staticmethod
    def get_coincidence(pair_1, pair_2):
        """вычесление отрезка времени общего нахождения в эфире
           первой пары(pair_1) и второй пары(pair_2)"""
        coincidence_list = []
        for p_i in pair_1:
            for p_j in pair_2:
                if (p_j[0] == p_i[0]) & (p_j[1] == p_i[1]):
                    time_start = p_i[0]
                    time_end = p_i[1]
                    coincidence_list.append([time_start, time_end])

                elif (p_j[0] > p_i[0]) & (p_j[0] < p_i[1]) & (p_j[1] > p_i[1]):
                    time_start = p_j[0]
                    time_end = p_i[1]
                    coincidence_list.append([time_start, time_end])

                elif (p_j[0] < p_i[0]) & (p_j[1] < p_i[1]) & (p_j[1] > p_i[0]):
                    time_start = p_i[0]
                    time_end = p_j[1]
                    coincidence_list.append([time_start, time_end])

                elif (p_j[0] == p_i[0]) & (p_j[1] < p_i[1]) & (p_j[1] > p_i[0]):
                    time_start = p_i[0]
                    time_end = p_j[1]
                    coincidence_list.append([time_start, time_end])

                elif (p_j[0] > p_i[0]) & (p_j[1] == p_i[1]) & (p_j[0] < p_i[1]):
                    time_start = p_j[0]
                    time_end = p_i[1]
                    coincidence_list.append([time_start, time_end])

                elif (p_j[0] < p_i[0]) & (p_j[1] > p_i[1]):
                    time_start = p_i[0]
                    time_end = p_i[1]
                    coincidence_list.append([time_start, time_end])

                elif (p_j[0] > p_i[0]) & (p_j[0] < p_i[1]) & (p_j[1] < p_i[1]):
                    time_start = p_j[0]
                    time_end = p_j[1]
                    coincidence_list.append([time_start, time_end])

        return coincidence_list

    @staticmethod
    def get_counting_time(pair_time):
        """подсчет суммы времени каждой пары с момента включения p[0] и выключения p[1]"""
        sum_time = 0
        for p in pair_time:
            coincidence_time = p[1] - p[0]
            sum_time += coincidence_time

        return sum_time

    @staticmethod
    def get_pair(lists):
        """разбиение списков на пары из четного и нечетного индекса
           (начало и конец урока)"""
        pair_element = []
        for elem in range(int(len(lists) / 2)):
            pair_element.append(lists[0:2])
            del lists[0:2]

        return pair_element

    def run(self):
        for i, test in enumerate(self.tests):
            test_answer = self.appearance(test['data'])
            assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
            print(test_answer)


if __name__ == '__main__':
    lessons = Lessons(tests)
    lessons.run()


