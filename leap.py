print('Enter a year A.D.:')
year = int(input())
if year % 4 == 0 and year % 100 != 0:
    print(str(year) + ' is a leap year')
elif year % 400 == 0:
    print(str(year) + ' is a leap year')
else:
    print(str(year) + ' is not a leap year')
