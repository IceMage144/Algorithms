import math
import importlib

# import click

from mathLib import *
from stringLib import *

def run_collatz(num=None):
    '''
    Applies Collatz's operations from an initial number, prints out the
    numbers found while applying them and points out the numbers of the
    form 6n + 4.
    At the end, prints out some useful information.

    -----------------------------------------------------

    Time complexity: O(a + w)
    Memory complexity: O(1)

    -----------------------------------------------------

    Inputs:
    1. The initial number
    '''
    if num is None:
        num = int(input('Input a number: '))

    odd_count = 0
    even_count = 0

    initial_even = 0
    smooth_array = [0]

    for parity, partial in iterated_collatz(num):
        partial_b2 = '(' + str(bin(partial))[2:] + ')_2'
        partial_b3 = '(' + ''.join(map(str, number_to_base(partial, 3))) + ')_3'
        if parity == 0:
            print('Even', partial, partial_b2, partial_b3, end='')
            even_count += 1

            if partial % 6 == 4:
                print(' <=== 6n + 4')
            else:
                print()

            if len(smooth_array) == 1:
                initial_even = even_count
            else:
                smooth_array[0] += 1
        else:
            print('Odd ', partial, partial_b2, partial_b3)
            if partial == 1:
                break
            odd_count += 1
            smooth_array.insert(0, even_count - initial_even)
    
    smooth_array.pop(0)
    
    print('============= Final results =============')
    print('- Initial number:            ', num)
    print('- Even rules applied:        ', even_count)
    print('- Odd rules applied:         ', odd_count)
    print('- Sum of steps:              ', even_count + odd_count)
    print('- Difference of the steps:   ', even_count - odd_count)
    print('- 3-smooth associated:       ', 2 ** even_count - num * 3 ** odd_count,
          '( 2^' + str(initial_even), '*', smooth_array, ')')
    
    return [even_count, odd_count, (initial_even, smooth_array)]


def run_batch_collatz():
    '''
    Run Collatz's operations from 3 to a maximum number, and, for
    each number, prints out some information about its path.

    -----------------------------------------------------

    Time complexity: O(max_num * (a + w))
    Memory complexity: O(1)

    -----------------------------------------------------

    Inputs:
    1. The maximum number
    '''
    max_num = int(input('Input the maximum number: '))

    print('number    evens     odds      sum       diff      3-smooth')
    for i in range(3, max_num, 2):
        even_count, odd_count = collatz(i)
        print_spaced(i, 10, end='')
        print_spaced(even_count, 10, end='')
        print_spaced(odd_count, 10, end='')
        print_spaced(even_count + odd_count, 10, end='')
        print_spaced(even_count - odd_count, 10, end='')
        print(2 ** even_count - i * 3 ** odd_count)


def run_find_smooth_a_w():
    '''
    Given the desired numbers of even and odd rules applications,
    calculates all the possible 3-smooths.
    At the end prints out the 3-smooths and the array of powers
    of two used to create it.

    -----------------------------------------------------

    This function solve the set of equations of the form:
    3^w*x + z = 2^a mod 3^k, 1 <= k < w
    which can be changed to
    z = 2^a mod 3^k, 1 <= k < w
    since the powers of three are smaller than w.

    Note that the equation becomes independent of x.

    Since 2^a = 2^(a + j * 3^w) mod 3^w, for all j >= 0, also
    note that the 3-smooth found here can also be used for
    bigger powers of two of this form.

    -----------------------------------------------------

    Time complexity: O(2^(w-1)) [sum 1 <= k <= w of (w choose k)]
    Memory complexity: O(w) [its a bit bigger, but I don't know how to calculate it :P]

    -----------------------------------------------------

    Inputs:
    1. The number of even rule applications
    2. The number of odd rule applications
    '''
    even_count = int(input('Input the number of even steps: '))
    odd_count = int(input('Input the number of odd steps: '))

    results = []
    def find_smooth_a_w_r(stack):
        three_exp = len(stack)
        three_power = 3 ** three_exp
        reminder = sum([
            (power_mod(2, el, 3, three_exp) * 3 ** i) % three_power
            for i, el in enumerate(stack)
        ]) % three_power

        even_reminder = power_mod(2, even_count, 3, three_exp)
        if reminder != even_reminder:
            return

        if len(stack) == odd_count:
            if stack[-1] == 0:
                results.append(stack)
            return

        last_pow = stack[-1]
        for i in range(last_pow - 1, odd_count - three_exp - 2, -1):
            find_smooth_a_w_r(stack + [i])

    for init_two_exp in range(even_count, odd_count - 2, -1):
        find_smooth_a_w_r([init_two_exp])
    
    print('3-smooth                    twos\' powers')
    for two_powers in results:
        print_spaced(calculate_smooth(two_powers), 28, end='')
        print(two_powers)


def run_find_smooth(max_num=None, print_output=False):
    '''
    Finds all the 3-smooths smaller than a maximum.

    -----------------------------------------------------

    Note that if b and c are both 3-smooths, then, depending on the
    powers of two of both of them, b*c can be a 3-smooth, and is a
    little easier to find.

    -----------------------------------------------------

    w ~ O(log_3(max_num)) [Appendix 1]
    Time complexity: O(2^(w-1))
    Memory complexity: O(max_num * w)

    -----------------------------------------------------

    Inputs:
    1. The maximum number (>=1)
    '''
    print_output = (max_num is None) or print_output
    max_num = max_num or int(input('Input the maximum number: '))

    results = [(1, [0])]
    def find_smooth_r(stack):
        smooth_stack = stack + [0]
        smooth = calculate_smooth(stack + [0])

        if smooth > max_num:
            return

        results.append((smooth, smooth_stack))

        last_pow = stack[-1]
        for i in range(last_pow - 1, 0, -1):
            find_smooth_r(stack + [i])

    max_two_power = math.floor(math.log2(max_num))
    for init_two_exp in range(max_two_power, 0, -1):
        find_smooth_r([init_two_exp])
    
    results = sorted(results, key=lambda x: x[0])

    if print_output:
        print('3-smooth    twos\' powers              factors')
        for smooth, two_powers in results:
            print_spaced(smooth, 12, end='')
            print_spaced(two_powers, 26, end='')
            print(get_factors(smooth))
    
    return results


def run_mod_two_collatz(input_num=None, odd_count=None):
    '''
    Uses a different algorithm, based on modularity of powers of 2,
    to find the solutions.

    -----------------------------------------------------

    Note that for the right odd_count, the resulted even_count will be an integer,
    but it will also be an integer for all multiples of that odd_count.

    -----------------------------------------------------

    Inputs:
    1. The starting number
    2. The number of odd steps required to get to one
    '''
    if input_num is None:
        input_num = int(input('Input a number: '))
    if odd_count is None:
        odd_count = int(input('Input the number of odd steps: '))

    smooth = calculate_smooth(two_exps) * 2 ** two_factor_count
    even_count = math.log2(input_num * 3 ** odd_count + smooth)

    print("- Even rules applied:  ", even_count)
    print("- 3-smooth associated: ", smooth, '( 2^' + str(two_factor_count), '*', two_exps, ')')

    return even_count, smooth


def run_syracuse(num=None):
    if num is None:
        num = int(input('Input a number: '))

    odd_count = 0
    even_count = 0

    initial_even = 0
    smooth_array = []

    odd_num = num
    while odd_num % 2 == 0:
        odd_num = odd_num // 2
        initial_even += 1
        even_count += 1

    for partial, partial_even_count in iterated_syracuse(odd_num):
        partial_b2 = '(' + str(bin(partial))[2:] + ')_2'
        partial_b3 = '(' + ''.join(map(str, number_to_base(partial, 3))) + ')_3'
        print(partial, partial_b2, partial_b3)
        even_count += partial_even_count
        if partial == 1:
            break
        odd_count += 1
        smooth_array.insert(0, even_count - initial_even)
    
    
    print('============= Final results =============')
    print('- Initial number:            ', num)
    print('- Even rules applied:        ', even_count)
    print('- Odd rules applied:         ', odd_count)
    print('- Sum of steps:              ', even_count + odd_count)
    print('- Difference of the steps:   ', even_count - odd_count)
    print('- 3-smooth associated:       ', 2 ** even_count - num * 3 ** odd_count,
          '( 2^' + str(initial_even), '*', smooth_array, ')')
    
    return [even_count, odd_count, (initial_even, smooth_array)]


if __name__ == '__main__':
    # run_binomial_decomposition()
    # run_mod_two_collatz()
    run_batch_collatz()
    # run_collatz()
    # run_find_smooth()
    # run_syracuse()
    # run_find_smooth_a_w()
    # run_print_pow2_base3()

'''
Appendix 1

2^k + 3*2^(k-1) + 3^2*2^(k-2) + ... + 3^(k-1)*2 + 3^k
3^(k*log(2, 3)) + 3^(1+(k-1)*log(2, 3)) + 3^(2+(k-2)*log(2, 3)) + ... + 3^(k-1+log(2, 3)) + 3^k
3^(k*log(2, 3))*(1 + 3^(1-log(2, 3)) + 3^(2-2*log(2, 3)) + ... + 3^(k-1-(k-1)*log(2, 3)) + 3^(k-k*log(2,3)))
3^(k*log(2, 3))*(1 + 3^(1-log(2, 3)) + 3^(2*(1-log(2, 3))) + ... + 3^((k-1)*(1-log(2, 3))) + 3^(k*(1-log(2,3))))
3^(k*log(2, 3))*(1 + 3^(1-log(2, 3))*(1 + 3^2 + ... + 3^(k-1) + 3^k))
3^(k*log(2, 3))*(1 + 3^(1-log(2, 3))*(3^(k+1) - 1))
3^(k*log(2, 3))*(1 + 3^(k+2-log(2, 3)) - 3^(1-log(2, 3)))
3^(k+2+(k-1)*log(2, 3)) + 3^(k*log(2, 3))*(1 - 3^(1-log(2, 3)))

max_num ~ 3^(k * (1 + log(2, 3)) + 2 - log(2, 3))
log(max_num, 3) - 2 + log(2, 3) ~ k * (1 + log(2, 3))
(log(max_num, 3) - 2 + log(2, 3)) / (1 + log(2, 3)) ~ k
(log(2 * max_num, 3) - 2) / log(6, 3) ~ k
'''

'''
19  =>  [4, 0]          <-> [2, 1, 0]
65  =>  [5, 3, 0]       <-> [3, 2, 1, 0]        (19 3=> 65)
85  =>  [6, 2, 0]       <-> [4, 3, 1, 0]
89  =>  [5, 4, 0]       <-> [5, 2, 1, 0]        ([19, 1] 1=> 89)
121 =>  [6, 4, 0]       <-> [6, 2, 1, 0]        ([19, 2] 1=> 121)
143 =>  [7, 1, 0]       <-> [5, 4, 2, 0]
185 =>  [7, 4, 0]       <-> [7, 2, 1, 0]        ([19, 3] 1=> 185)
211 =>  [6, 4, 3, 0]    <-> [4, 3, 2, 1, 0]     (65 3=> 65)
259 =>  [8, 0]          <-> [6, 5, 3, 0]    <-> [6, 3, 2, 1, 0]  ([65, 1] 1=> 259)
287 =>  [7, 5, 2, 0]    <-> [5, 4, 3, 1, 0]
313 =>  [8, 4, 0]       <-> [8, 2, 1, 0]        ([19, 4] 1=> 313)
323 =>  [7, 5, 3, 0]    <-> [7, 3, 2, 1, 0]     ([65, 2] 1=> 323)
331 =>  [6, 5, 4, 0]    <-> [6, 5, 2, 1, 0]     ([89, 1] 1=> 331)
367 =>  [8, 4, 2, 0]    <-> [6, 5, 3, 1, 0]
383 =>  [7, 6, 2, 0]    <-> [7, 4, 3, 1, 0]     ([85, 1] 1=> 383)
395 =>  [7, 5, 4, 0]    <-> [7, 5, 2, 1, 0]     ([89, 2] 1=> 395)
451 =>  [8, 5, 3, 0]    <-> [8, 3, 2, 1, 0]     ([65, 3] 1=> 451)
491 =>  [7, 6, 4, 0]    <-> [7, 6, 2, 1, 0]     ([121, 1] 1=> 491)
493 =>  [8, 6, 1, 0]    <-> [6, 5, 4, 2, 0]
511 =>  [8, 6, 2, 0]    <-> [8, 4, 3, 1, 0]     ([85, 2] 1=> 511)
523 =>  [8, 5, 4, 0]    <-> [8, 5, 2, 1, 0]     ([89, 3] 1=> 523)
527 =>  [9, 1, 0]       <-> [7, 6, 3, 1, 0]
569 =>  [9, 4, 0]       <-> [9, 2, 1, 0]        ([19, 5] 1=> 313)
581 =>  [9, 3, 1, 0]    <-> [7, 6, 3, 2, 0]
599 =>  [9, 3, 2, 0]    <-> [7, 6, 4, 1, 0]
619 =>  [8, 6, 4, 0]    <-> [8, 6, 2, 1, 0]     ([121, 2] 1=> 619)
653 =>  [9, 5, 1, 0]    <-> [7, 6, 4, 2, 0]
665 =>  [7, 5, 4, 3, 0] <-> [5, 4, 3, 2, 1, 0]  (221 3=> 65)
685 =>  [8, 7, 1, 0]    <-> [8, 5, 4, 2, 0]     ([143, 1] 1=> 685)

Rule 1 [x, c]
[x_1, x_2, x_3, ...] = [y_1, y_2, y_3, ...]
then
[max(x_1, y_1) + c, x_1, x_2, x_3, ...] = [max(x_1, y_1) + c, y_1, y_2, y_3, ...]
c >= 1
or
if z is 3-smooth, then 2^{b_0 + c} + 3*z, for c >= 1, is also a 3-smooth

Rule 2 [x, i, c]
[x_1, ..., x_{i-1}, b, x_{i+1}, ...] = [y_1, ..., y_{i-1}, b, y_{i+1}, ...]
then
[x_1, ..., x_{i-1}, b + c, x_{i+1}, ...] = [y_1, ..., y_{i-1}, b + c, y_{i+1}, ...]
min(x_{i-1}, y_{i-1}) - b < c < min(x_{i+1}, y_{i+1}) - b
or
if z is a 3-smooth and b_i + 1 < b_{i+1}, then z + 2^{b_i}*3^i is also a 3-smooth [apply this rule c >= 1 times to get the observed pattern]

Rule 3
[x_1, x_2, x_3, ...] = [y_1, y_2, y_3, ...]
if x_1 = y_1 + 2 then
[x_1 + 1, x_1 - 1, x_2, ...] = [y_1 + 1, y_1, y_2, ...]


2^{h_0 + 1} - 3 * 2^{h_0 - 1} + 3 * z = 2^{b_0 + 1} + 3 * z
2^{h_0 + 1} - 3 * 2^{h_0 - 1} = 2^{b_0 + 1}
4 * 2^{h_0 - 1} - 3 * 2^{h_0 - 1} = 2 * 2^{b_0}
2^{h_0 - 1} = 2^{b_0 + 1}
h_0 - 1 = b_0 + 1


[4, 0]          <-> [2, 1, 0]
[5, 3, 0]       <-> [3, 2, 1, 0]
[6, 4, 3, 0]    <-> [4, 3, 2, 1, 0]

[7, 1, 0]       <-> [5, 4, 2, 0]
[8, 6, 1, 0]    <-> [6, 5, 4, 2, 0]

[6, 2, 0]       <-> [4, 3, 1, 0]
[7, 5, 2, 0]    <-> [5, 4, 3, 1, 0]

[9, 3, 1, 0]    <-> [7, 6, 3, 2, 0]
[9, 3, 2, 0]    <-> [7, 6, 4, 1, 0]
'''