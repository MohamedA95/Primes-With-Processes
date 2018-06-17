"""
This program (code) generates and check prime numbers using multiprocessing.
One way to test if a number is prime or not is to divide it by all the number from 2 up to that number (N).
All these dividing operations does not depend on each other so, we can break them into groups and give each core (thread)
a group to calculate. In addition we really need to divide up to the square root of the number. Finally, there is no
need to divide by two or check even numbers or divide by even numbers.
"""
import multiprocessing as mp
import math
import sys


def calculate(number, s, e, q):
    """Takes a group and divides the number by all the numbers in this group
    We only need to divide by odd numbers so if the start is even make it odd.
    :returns a list
    the first item is 'd' if the number is not prime and the second is the divisor
     if the number is prime it returns true
    """

    if s % 2 == 0:
        s += 1
    for i in range(s, 1 + e, 2):
        if number % i == 0:
            q.put(['d', i])
            return
    q.put([True])
    return


def isprime(number, proc):
    """This function takes a number and the number of cores the user wants to use
     then it creates a multiprocess queue to enable the communication, then it calculates some
     needed variables. Finally, it starts the appropriate number of processes.
     :returns
     -1 if the number is prime
     -2 if the number is even
     else it returns the number that the input is dividable by
     """
    q = mp.Queue()
    process = []
    finishedProc = 0
    GroubStart = 3
    if number == 1:
        return 1
    if number == 2:
        return -1
    if number % 2 == 0:
        return -2
    maxDiv = math.ceil(math.sqrt(number))
    GroupSize = math.ceil((maxDiv - 3) / proc)
    GroupEnd = GroubStart + GroupSize
    if GroupSize <= proc:
        calculate(number, 3, number - 1, q, )
        finishedProc=proc-1
    else:
        for i in range(proc):
            p = mp.Process(target=calculate, args=(number, GroubStart, GroupEnd, q,))
            p.start()
            process.append(p)
            GroubStart += GroupSize
            GroupEnd += GroupSize
            if GroupEnd == number:
                GroupEnd -= 1

    while True:
        if q.qsize() > 0:
            val = q.get()
            if val[0] == 'd':
                for i in process:
                    i.terminate()
                return val[1]
            elif val[0]:
                finishedProc += 1
                if finishedProc == proc:
                    for i in process:
                        i.terminate()
                    return -1


if __name__ == '__main__':
    print('Welcome to prime numbers generator/checker')
    realCores = mp.cpu_count()
    cores = int(input("You have {0} cores (Threads), how many would you like to use? ".format(realCores)).strip())
    if cores > realCores:
        print("WRONG VALUE")
        sys.exit()
    choose = input('(1) Check or (2) Generate ? ').strip()

    if choose == '1':
        num = int(input('What number is that? ').strip())
        result = isprime(num, cores)
        if result == -1:
            print('it is a prime :)')
            sys.exit()
        elif result == -2:
            print('even numbers are not prime')
            sys.exit()
        else:
            print('no it is not prime it is divisible by {0}'.format(result))
            sys.exit()
    elif choose == '2':
        end = int(input('How many prime numbers do you need?[0 for infinite] ').strip())
        i = 1
        if end > 0:
            while end > 0:
                result = isprime(i, cores)
                if result == -1:
                    print(i)
                    end -= 1
                i += 2
        elif end == 0:
            while True:
                result = isprime(i, cores)
                if result == -1:
                    print(i)
                i += 2
    elif choose == '3':
        file = input('Where is your file??').strip()
        with open(file, 'r') as inFile:
            for line in inFile:
                l = line.split()
                for num in l:
                    res = isprime(int(num), cores)
                    if res != -1:
                        print('The program failed with the following test case {0}'.format(num))
                    elif res == -1:
                        print(num)
                    else:
                        print('Something wrong happened while checking {0}'.format(num))
    else:
        print("WRONG VALUE")
        sys.exit()