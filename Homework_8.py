import random
import threading


numbers = []
lock = threading.Lock()


def fill_list():
    global numbers
    for _ in range(10_000):
        numbers.append(random.randint(1, 1000000))


def get_primes_amount():
    primes_count = 0
    for num in numbers:
        if num > 1:
            is_prime = True
            for i in range(2, int(num**0.5) + 1):
                if num % i == 0:
                    is_prime = False
                    break
            if is_prime:
                primes_count += 1
    return primes_count


def get_average():
    if numbers:
        return sum(numbers) / len(numbers)
    return 0


def run_t2():
    # Wait until the list is filled
    while len(numbers) < 10_000:
        pass
    print("Sum of elements:", sum(numbers))


def run_t3():
    while len(numbers) < 10_000:
        pass
    print("Average of elements:", get_average())


def run_t1():
    fill_list()


t1 = threading.Thread(target=run_t1)
t2 = threading.Thread(target=run_t2)
t3 = threading.Thread(target=run_t3)


t1.start()
t2.start()
t3.start()


t1.join()
t2.join()
t3.join()


primes_count = get_primes_amount()
print("Number of prime numbers:", primes_count)
