# -*- coding: utf-8 -*-
from __future__ import division
import random
import matplotlib.pyplot as plt


class Process:
    process_counter = 0

    def __init__(self, work_q):
        self.work_q = work_q
        self.number = Process.process_counter
        Process.process_counter += 1

    def work(self):
        self.work_q -= 1
        return self.work_q == 0


class ProcessQueue(list):
    priority_counter = 0

    def __init__(self, *args):
        list.__init__(self, *args)
        self.waiting_timers = [0]
        self.priority = ProcessQueue.priority_counter
        ProcessQueue.priority_counter -= 1

    def work(self):
        current_process = self[self.__len__() - 1]
        self.pop()
        if not current_process.work():
            self.insert(0, current_process)
        if self.waiting_timers[self.waiting_timers.__len__() - 1] != 0:
            self.waiting_timers.append(0)
        print('Працює процес #{} з пріорітетом {}, до виконання залишилось {}'.format(current_process.number,
                                                                                      self.priority,
                                                                                      current_process.work_q))

    def tic(self):
        self.waiting_timers[self.waiting_timers.__len__() - 1] += 1

    def add(self, process):
        self.insert(0, process)


class TaskManager:
    def __init__(self, priority_count):
        ProcessQueue.priority_counter = priority_count
        self.no_job_q_count = 0
        self.queues = []
        for i in range(priority_count):
            self.queues.append(ProcessQueue([]))

    def work(self):
        worker_queue = None
        for i in range(self.queues.__len__()):
            if self.queues[i].__len__() != 0:
                if not worker_queue:
                    worker_queue = self.queues[i]
                else:
                    self.queues[i].tic()
        if worker_queue:
            worker_queue.work()
        else:
            self.no_job_q_count += 1


waiting_time_to_intensity_stat = []
no_job_percentage_to_intensity_stat = []
waiting_time_to_priority_stat = []


def work(q_count, intensity, calculate_waiting_time_to_priority_stat=False):
    qs = q_count
    qs_before_new_task = intensity
    task_manager = TaskManager(8)

    while qs != 0:
        if qs_before_new_task == 0:
            qs_before_new_task = intensity
            new_process = Process(random.randrange(1, 10))
            priority = random.randrange(0, task_manager.queues.__len__())
            task_manager.queues[priority].add(new_process)
            print(
                'Додано процес #{} з пріорітетом {}'.format(new_process.number, task_manager.queues[priority].priority))

        task_manager.work()
        qs_before_new_task -= 1
        qs -= 1

    all_waiting_timers = []

    for queue in task_manager.queues:
        all_waiting_timers.extend(queue.waiting_timers)

        if calculate_waiting_time_to_priority_stat:
            average_waiting_time_for_queue = 0
            for j in queue.waiting_timers:
                average_waiting_time_for_queue += j
            waiting_time_to_priority_stat.append(
                (queue.priority, average_waiting_time_for_queue / queue.waiting_timers.__len__()))

    average_waiting_time = 0
    for j in all_waiting_timers:
        average_waiting_time += j
    average_waiting_time /= all_waiting_timers.__len__()
    waiting_time_to_intensity_stat.append((10 - intensity, average_waiting_time))
    no_job_percentage_to_intensity_stat.append((10 - intensity, (task_manager.no_job_q_count / q_count) * 100))


def unpack_to_xy_arrays(list_of_tuples):
    x = []
    y = []
    for tup in list_of_tuples:
        x.append(tup[0])
        y.append(tup[1])
    return x, y


for i in range(1, 10):
    Process.process_counter = 0
    ProcessQueue.priority_counter = 0
    print('-' * 60)
    work(200, i, i == 3)

x, y = unpack_to_xy_arrays(waiting_time_to_priority_stat)
# x, y = unpack_to_xy_arrays(waiting_time_to_intensity_stat)
# x, y = unpack_to_xy_arrays(no_job_percentage_to_intensity_stat)
plt.plot(x, y)
plt.show()
