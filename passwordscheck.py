import passwords, fragments

print('Input a password length:')
length = input()

check = 1
while check < 10:
    password = passwords.easy_password(int(length))
    print(password)
    print(len(password))
    check += 1

print('done')