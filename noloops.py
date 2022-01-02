def product(nums):
    pd = 0
    if len(nums) == 0:
        pd = 1
    elif len(nums) == 1:
        pd = nums[0]
    else:
        first = nums[0]
        last = nums[1:]
        pd = first * product(last)
    return pd

def squares(nums):
    sq = 0
    sqlist = []
    if nums == []:
        sqlist = nums
        return sqlist
    elif len(nums) == 1:
        sq = nums[0] * nums[0]
        sqlist.append(sq)
        return sqlist
    else:
        sq = nums[0] * nums[0]
        last = nums[1:]
        sqlist.append(sq)
        sqlast = squares(last)
        return sqlist + sqlast
    
def num_zeros(n):
    z = 0
    if n < 0:
        pass
    elif 0 < n < 10:
        z = 0
    else:
        if n % 10 == 0:
            z += 1
        z += num_zeros(int(n / 10))
    return z
