import matplotlib.pyplot as plt
import numpy as np


# Calculates sum of digits
def sum(number):
    s = 0
    n = number
    while n >= 9:
        s += n % 10
        n //= 10
    return s + n

# Calculates maximum sum of digits possible taken from all numbers less than or equal to num. Number of digits in num is given
def max_sum(num, n_digits):
    if n_digits == 1:
        return num

    first_d = num // (10 ** (n_digits - 1))
    first = first_d - 1 + 9 * (n_digits - 1)
    second = first_d + max_sum(num - first_d * 10 ** (n_digits - 1), n_digits - 1)
    if first > second:
        return first
    else:
        return second

# Calculates maximum sum of digits possible taken from all numbers in range (num1 , num2)
def max_sum_with_bounds(num1, num2, n_digits1, n_digits2):
    if n_digits2 == 1:
        return num2

    first_d2 = num2 // (10 ** (n_digits2 - 1))
    first_d1 = num1 // (10 ** (n_digits1 - 1))

    if n_digits2 > n_digits1 or first_d2 > first_d1:
        first = first_d2 - 1 + 9 * (n_digits2 - 1)
        second = first_d2 + max_sum(num2 - first_d2 * 10 ** (n_digits2 - 1), n_digits2 - 1)
        if first > second:
            return first
        else:
            return second

    elif first_d2 == first_d1:
        return first_d2 + max_sum_with_bounds(num1 - first_d1 * 10 ** (n_digits1 - 1),num2 - first_d2 * 10 ** (n_digits2 - 1),n_digits1 - 1, n_digits2 - 1)

# Calculates minimum sum of digits possible taken from all numbers in range (num1 , num2)
def min_sum_with_bounds(num1, num2, n_digits1, n_digits2):
    if n_digits1 == 1:
        return num1

    first_d2 = num2 // (10 ** (n_digits2 - 1))
    first_d1 = num1 // (10 ** (n_digits1 - 1))

    if n_digits2 > n_digits1:
        return 1
    elif first_d2 > first_d1:
        if num1 - first_d1 * 10 ** (n_digits1 - 1) == 0:
            return first_d1
        else:
            return first_d1 + 1
    elif first_d2 == first_d1:
        return first_d2 + min_sum_with_bounds(num1 - first_d1 * 10 ** (n_digits1 - 1),num2 - first_d2 * 10 ** (n_digits2 - 1),n_digits1 - 1, n_digits2 - 1)



# Calculates count of all n-digit numbers which which add up to s
def count(s, n_digits):
    if s > n_digits * 9:
        return 0
    elif s == 0:
        return 1
    elif n_digits == 1:
        return 1
    t = 0
    i = 0
    while i <= s and i < 10:
        t += count(s - i, n_digits - 1)
        i += 1
    return t

# Optimized count using symmetry
def count2(s, n_digits):
    max_sum = n_digits * 9
    if s > max_sum:
        return 0
    elif s > max_sum / 2:
        return count2(max_sum - s, n_digits)
    elif s == 0:
        return 1
    elif n_digits == 1:
        return 1

    t = 0
    i = 0
    while i <= s and i < 10:
        t += count2(s - i, n_digits - 1)
        i += 1
    return t








#Two functions below are supposed to be the answer to the task

#Calculates count of all n-digit numbers less than or equal to max_ind which add up to s
def count_max(s, max_ind, n_digits):
    if s > max_sum(max_ind, n_digits):
        return 0
    if s == 0:
        return 1
    if n_digits == 1:
        return 1
    first_d = max_ind // (10 ** (n_digits - 1))
    rest_dgts = max_ind - first_d * 10 ** (n_digits - 1)
    t = 0
    i = 0
    while i <= s and i < first_d and i < 10:
        t += count2(s - i, n_digits - 1)
        i += 1
    if first_d <= s:
        t += count_max(s - first_d, rest_dgts, n_digits - 1)
    return t

#Calculates count of all numbers less than or equal to max_ind but more than or equal to min_ind which add up to s
def count_minmax(s, min_ind, max_ind, n_digits_min, n_digits_max):
    mx_sm = max_sum_with_bounds(min_ind, max_ind, n_digits_min, n_digits_max)
    mn_sm = min_sum_with_bounds(min_ind, max_ind, n_digits_min, n_digits_max)
    if s > mx_sm or s < mn_sm:
        return 0
    #if s == mn_sm:
    #    return 1
    if n_digits_max == 1:
        return 1
    first_d_max = max_ind // (10 ** (n_digits_max - 1))
    rest_dgts_max = max_ind - first_d_max * 10 ** (n_digits_max - 1)
    first_d_min = min_ind // (10 ** (n_digits_min - 1))
    rest_dgts_min = min_ind - first_d_min * 10 ** (n_digits_min - 1)
    t = 0
    n_digits = n_digits_min
    i = first_d_min + 1
    if first_d_min <= s:
        t += count_minmax(s - first_d_min, rest_dgts_min, 10**(n_digits_min - 1) - 1, n_digits_min - 1, n_digits_min - 1)
    while n_digits < n_digits_max:
        while i <= s and i < 10:
            t += count2(s - i, n_digits - 1)
            i += 1
        i = 1
        n_digits+=1

    while i <= s and i < first_d_max and i < 10:
        t += count2(s - i, n_digits_max - 1)
        i += 1
    if first_d_max <= s:
        t += count_max(s - first_d_max,rest_dgts_max, n_digits_max - 1)
    return t


#Checking
if __name__ == "__main__":
    number1 = 988
    number2 = 49109
    n_dgts1 = 3
    n_dgts2 = 5
    mx_sm = max_sum(number2, n_dgts2)
    nums = np.zeros(mx_sm + 1)
    nums2 = np.zeros(mx_sm + 1)

    # Obvious lazy method
    for i in range(number1, number2 + 1):
        nums[sum(i)] += 1

    # Solved
    for i in range(0, mx_sm + 1):
        nums2[i] = count_minmax(i,number1,number2, n_dgts1,n_dgts2)
        #Yet another method
        #nums2[i] = count_max(i,number2, n_dgts2) - count_max(i,number1, n_dgts1)



    print(count_minmax(20,number1,number2, n_dgts1,n_dgts2))
    print(nums2)
    print(nums)

    # Visualize
    plt.plot(np.arange(mx_sm + 1), nums)
    plt.plot(np.arange(mx_sm + 1), nums2)
    plt.show()
