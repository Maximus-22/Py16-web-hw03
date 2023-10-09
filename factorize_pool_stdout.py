import logging, sys
from multiprocessing import Pool, Process, current_process, cpu_count
from time import time


# у класі [Process] немає явної реалізації збереження результатів роботи функції при задіянні аргументу [target] 
data_result = []


# функція приймає довільну кількість аргументів, які передаються у цю функцію як кортеж зі значень
def factorize(*number: int | float) -> list:
    global data_result
    if len(number):
        try:
            print(f"Start execute of a function [factorize].")
            timer = time()
            # data_result = []
            for num in number:
                factors = []
                for i in range(1, num + 1):
                    if num % i == 0:
                        factors.append(i)
                data_result.append(factors)
            print(f"Execution of the function [factorize] completed by {round(time() - timer, 4)} sec.")
            return data_result
        except ValueError as err:
            print(err)
    else:
        return list()


# один з варіантів реалізації виводу результатів роботи функції у класі [Pool]
def callback(result: list) -> None:
     print(f"Result in callback: {result}")


if __name__ == "__main__":
    # test_data = (128, 255, 99999, 10651060)
    test_data = (512, 8888, 56665, 110110, 7336225, 11991188)


    # блок тестування звичайної функції
    with open("test.txt", "w") as file:
        sys.stdout = file

        # синхронний режим
        single_list = factorize(*test_data)
        [print(row) for row in single_list]
        print(end = "\n\n")


        # асинхронний режим з використанням класу [Pool]
        print(f"Count CPU: {cpu_count()}")
        print(f"Start execute of a function [factorize] with Pool.")
        timer = time()
        with Pool(cpu_count()) as pool:
            # pool.map_async(factorize, test_data,)
            result = [pool.apply_async(factorize, (num,), callback = callback,) for num in test_data]
            pool.close()          # перестати виділяти процеси в пул
            pool.join()           # дочекатися завершення всіх процесів 
        print(f"End {current_process().name} with Pool by {round(time() - timer, 4)} sec.")
        print(end = "\n\n")


        # асинхронний режим з використанням класу [Process]
        print(f"Count CPU: {cpu_count()}")
        print(f"Start execute of a function [factorize] with Process.")
        timer = time()
        processes = []
        if len(test_data) <= int(cpu_count()):
            for i in range(len(test_data)):
                sub_process = Process(target = factorize, args = (*test_data,), name = f"Function №{i}", )
                sub_process.start()
                processes.append(sub_process)
        else:
            for i in range(int(cpu_count())):
                sub_process = Process(target = factorize, args = (*test_data,), name = f"Function №{i}",)
                sub_process.start()
                processes.append(sub_process)
        [ps.join() for ps in processes]        
        print(f"End {current_process().name} with Processes by {round(time() - timer, 4)} sec.")
        [print(row) for row in data_result]
        sys.stdout = sys.__stdout__