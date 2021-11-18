import prime

print('Please enter a whole number to check if prime or \'quit\' for next option')
num = input()
while num != 'quit':
    print(prime.is_prime(int(num)))
    print('Please enter a whole number to check if prime or \'quit\' for next option')
    num = input()

print('Please enter a whole number to check if twin prime or \'quit\' to quit')
num = input()
while num != 'quit':
    print(prime.is_twin_prime(int(num)))
    print('Please enter a whole number to check if twin prime or \'quit\' to quit')
    num = input()