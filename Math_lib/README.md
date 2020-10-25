# math_lip.py
* *find_divisors():* Find the common divisors of number1 and number2. Assumes that number1 and number2 are positive ints. Returns a tuple containing all common divisors.
* *find_extreme_divisors():* Find the smallest and largest common divisors of number1 and number2 other than 1. Assumes that number1 and number2 are positive ints.

## Studied various approaches to find prime number
* divisors(): checks to see if there is a divisor within a range.
* is_prime(): checks to see if a number is a prime.
* list_primes(): creates list of prime numbers within a range with recursion.
* list_primes_loop(): creates list of prime number within a range with loop.
* sieve_primes(): creates a list of prime number with a range using sieve algo which eliminates multiples of any prime found to speed up implementation
* seive_primes_comprehension(): cool implementation using comprehension. The trick is to remove from the full list from [2,n], all the multiples

 ### Observations:
* list_primes(): for numbers < 500 since recursion limit is exceeded.
* list_primes_loop(): for numbers < 995 since recursion is exceeded in divisors
* seive_primes_comprehension(): is a cool implementation using comprehension.
* is_prime_sqrt() and listPrimesSqrt() are version that test divisors from 2 to sqrt(limit) to speed.
* sieve_primes(): is more efficient by removing multiples of prime number as soon as it finds a prime. It also doe not use as many recursions therefore can go to limit < 7877.
* sieve_primes_comprehension(): has the most flexibility and can go > 50kWe can also change the recursion level by importing sys.  """

