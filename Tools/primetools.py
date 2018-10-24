def primenum(N):
    primes = [2]
    for n in range(3,N):
        if all(n%p>0 for p in primes):
            primes.append(n)
    return primes