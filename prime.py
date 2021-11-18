def is_prime(n):
    if n == 2:                  # based on Shawon's email
        return True
    elif n < 2:                 # prime numbers are greater than 1
        return False
    else:
        factors = []                #list to store factors after checking division
        for i in range(2, n//2):    #start by trying to divide by 2 an up to half of the input number
            if n % i == 0:          #if there is no remainder,  
                factors.append(i)   #add i to the list of factors
        if len(factors) > 0:        #if there is anything in the list
            return False            
        else:                       #prime numbers will have an empty list
            return True

def is_twin_prime(n):           #twin prime is pair of #s that are only two apart and both prime
    if is_prime(n) == False:    #first check if prime
        return False            #if False, it is not part of pair
    elif is_prime(n + 2) == True or is_prime(n - 2) == True:   #if prime, check if number 2 to the R or L is prime
        return True
    else:
        return False            #if False, it is not part of pair
