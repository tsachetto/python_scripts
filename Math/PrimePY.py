import time
import multiprocessing as mp

# função para verificar se um número é primo
def is_prime(num, primes):
    if num in primes:
        return True

    if num > 5 and str(num)[-1] not in ("1", "3", "7", "9"):
        return False

    if num % 2 == 0 or num % 3 == 0 or num % 7 == 0 or num % 9 == 0:
        return False

    f = 5
    if primes:
        f = primes[-1]  # Começar pelo maior número primo na lista primes
  
    r = int(num ** 0.5)
    while f <= r:
        if num % f == 0:
            return False
        if num % (f + 2) == 0:
            return False
        f += 6
        while f <= r:
            if any(f % prime == 0 for prime in primes if prime <= f):
                f += 6
            else:
                break
    return True 

def prime_checker(args):
    num, primes = args
    return is_prime(num, primes)

def find_primes(limit, primes):
    with mp.Pool(processes=mp.cpu_count()) as pool:
        args = [(num, primes) for num in range(2, limit + 1)]
        results = pool.map(prime_checker, args)
    return [num for num, prime in enumerate(results, 2) if prime]

def get_digit_ending_stats(primes):
    counts = {'1': 0, '2': 0, '3': 0, '5': 0, '7': 0, '9': 0}
    
    for prime in primes:
        last_digit = str(prime)[-1]
        counts[last_digit] += 1

    total = sum(counts.values())
    stats = {digit: count / total * 100 for digit, count in counts.items()}

    return stats


def main():
    # Recebe a entrada do usuário
    limit = int(input("Informe um número teto: "))
    primes = []
    # Define o temporizador de execução
    start_time = time.time()
    
    # Calcula os números primos
    if limit < 2:
        print("Não existem números primos até 1.")
    else:
        primes = find_primes(limit, primes)
        print("Tempo total de execução: %s segundos" % (time.time() - start_time))
        # Gera o arquivo de texto
        with open(str(limit) + '.txt', 'w') as f:
            for prime in primes:
                f.write(f"{prime}\n")
        
        # Imprime a quantidade de números primos encontrados
        print(f"{len(primes)} números primos foram encontrados até {limit}.")
    
    # Imprime o tempo total de execução
    #contar primes
    stats = get_digit_ending_stats(primes)
    
    print("Estatísticas dos números terminados em 1, 3, 7 e 9:")
    for digit, percentage in stats.items():
        print(f"Números terminados em {digit}: {percentage:.2f}%")

    input("...")

if __name__ == "__main__":
    main()
