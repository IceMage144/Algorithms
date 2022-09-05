import math

from mathLib import *
from stringLib import *
from main import *

def run_find_not_smooth_factors():
    '''
    Finds the factors of the 3-smooths that are not 3-smooths, for
    3-smooths bellow a maximum number.

    -----------------------------------------------------

    This is just a test function.

    -----------------------------------------------------

    Inputs:
    1. The maximum 3-smooth
    '''
    max_num = int(input('Input the maximum number: '))

    find_result = run_find_smooth(max_num)

    smooths = set()
    not_smooth_factors = set()
    for smooth, _ in find_result:
        factors = get_factors(smooth)
        if len(factors) == 1:
            smooths.add(smooth)
        else:
            for factor in factors:
                if factor not in smooths:
                    not_smooth_factors.add(factor)
    
    print(sorted(smooths))
    print(sorted(not_smooth_factors))

def run_binomial_decomposition():
    '''
    Run collatz and prints out a decomposition of the terms based on the fact
    that 3^w can be expressed by the Newton's Polynomial (2 + 1)^w.

    -----------------------------------------------------


    -----------------------------------------------------

    Inputs:
    1. The starting number
    '''
    num = int(input('Input a number: '))

    odd_count = 0
    even_count = 0

    initial_even = 0
    smooth_array = [0]

    for _, parity, _ in iterated_collatz(num):
        if parity == 0:
            even_count += 1
            if len(smooth_array) == 1:
                initial_even = even_count
            else:
                smooth_array[0] += 1
        else:
            odd_count += 1
            smooth_array.insert(0, even_count - initial_even)
    
    smooth_array.pop(0)
    odd_num = num // (2 ** initial_even)
    
    pascal_triangle = pascal(len(smooth_array) + 1)
    digs = 1
    for line in pascal_triangle:
        for i in line:
            digs = max(digs, count_chars(i))
    for i in pascal_triangle[-1]:
        digs = max(digs, count_chars(i * odd_num))
    digs += 1
    
    print(odd_num)
    print(smooth_array)

    sum_array = []
    for i, two_exp in zip(range(len(smooth_array) - 1, -1, -1), reversed(smooth_array)):
        print(((' ' * digs) + '|') * two_exp, end='')
        pascal_line = pascal_triangle[i]
        for j, binomial in enumerate(pascal_line):
            print_spaced(binomial, digs, align='right', end='|')
            while len(sum_array) <= j + two_exp:
                sum_array.append(0)
            sum_array[j + two_exp] += binomial
        print()
    
    print("-" * ((digs + 1) * len(sum_array)))

    for i, binomial in enumerate(pascal_triangle[-1]):
        print_spaced(binomial * odd_num, digs, align='right', end='|')
        while len(sum_array) <= i:
            sum_array.append(0)
        sum_array[i] += binomial * odd_num
    print()

    print("-" * ((digs + 1) * len(sum_array)))

    for res in sum_array:
        print_spaced(res, digs, align='right', end='|')
    print()

def run_find_not_smooth():
    max_num = int(input('Input the maximum number: '))
    smooths = run_find_smooth(max_num)
    smooths_set = set(map(lambda x: x[0], smooths))
    not_smooth_set = set()
    num = 1
    i = 0
    while num <= max_num:
        num = 6 * i + 5
        if num not in smooths_set and num <= max_num:
            not_smooth_set.add(num)
        num = 6 * i + 1
        if num not in smooths_set and num <= max_num:
            not_smooth_set.add(num)
        i += 1
    print(sorted(not_smooth_set))

def run_find_power_diffs():
    '''
    A192110
    A075824
    A014121
    '''
    max_exp = int(input('Input the maximum exponent of 2: '))
    diffs = {}
    for i in range(max_exp):
        two_power = 2 ** i
        j = 0
        diff = two_power - 3 ** j
        while diff > 0:
            if diffs.get(diff) is not None:
                diffs[diff].append((i, j))
            else:
                diffs[diff] = [(i, j)]
            j += 1
            diff = two_power - 3 ** j
    
    for i in range(int(math.log(2**max_exp, 3))):
        three_power = 3 ** i
        j = 0
        diff = three_power - 2 ** j
        while diff > 0:
            if diffs.get(diff) is not None:
                diffs[diff].append((-j, -i))
            else:
                diffs[diff] = [(-j, -i)]
            j += 1
            diff = three_power - 2 ** j

    for diff, powers in sorted(diffs.items(), key=lambda x: x[0]):
        print(diff, powers)


def run_multiply_complement():
    '''
    2^{2k} - 3^{b} = c
    2^{2k} = 3^{b} + c
    2^{2k} - 2^{2*floor(log2(c)/2)} = 3^{b} + c - 2^{2*floor(log2(c)/2)}
    (2^{k} + 2^{floor(log2(c)/2)}) * (2^{k} - 2^{floor(log2(c)/2)}) = 3^{b} + c - 2^{2*floor(log2(c)/2)}
    "(11){k-floor(log2(c)/2)}(00){floor(log2(c)/2)}" = 3^{b} + c - "10{floor(log2(c)/2) - 1}"
    '''
    max_exp = int(input('Input the exponent of 2: '))
    max_power = 2 ** max_exp
    for i in range(max_exp):
        two_power = 2 ** i
        product = (max_power + two_power) * (max_power - two_power)
        print(str(bin(max_power + two_power))[2:], " * ", str(bin(max_power - two_power))[2:], " = ", str(bin(product))[2:])

def run_power_2_syracuse():
    pass

def run_base3_analysis(num=None):
    if num is None:
        num = int(input('Input a number: '))
    
    extra_one = False
    for parity, partial in iterated_collatz(num):
        if parity == 0:
            partial_b3 = ''.join(map(str, number_to_base(partial, 3)))
            print(partial)
            print(partial_b3)
            first_one = -1
            for i in range(len(partial_b3)):
                if partial_b3[i] == '1':
                    if first_one == -1:
                        first_one = i
                    else:
                        size = i - first_one - 1
                        print_spaced(size, size + 2, align='right', end='')
                        first_one = -1
                else:
                    if first_one == -1:
                        print(' ', end='')
                extra_one = False
            print("\n---------------------------------------")
        else:
            extra_one = True

class Combo:
    def __init__(self, pair, length=1):
        self.pair = pair
        self.length = length
    
    def __repr__(self):
        if self.length == 1:
            return f'({self.pair})'
        return f'({self.pair})*{self.length}'
    
    def to_num(self):
        return self.pair * self.length

def apply_pumping_rule(combo, carry_on):
    if combo.pair == '00':
        head_pair = carry_on
        tail_pair = '00'
        new_carry_on = '00'
    elif combo.pair == '01':
        if carry_on == '00':
            head_pair = '11'
            tail_pair = '11'
            new_carry_on = '00'
        elif carry_on == '01':
            head_pair = '00'
            tail_pair = '00'
            new_carry_on = '01'
        else: # carry_on == '10'
            head_pair = '01'
            tail_pair = '00'
            new_carry_on = '01'
    elif combo.pair == '10':
        if carry_on == '00':
            head_pair = '10'
            tail_pair = '11'
            new_carry_on = '01'
        elif carry_on == '01':
            head_pair = '11'
            tail_pair = '11'
            new_carry_on = '01'
        else: # carry_on == '10'
            head_pair = '00'
            tail_pair = '00'
            new_carry_on = '10'
    else: # combo.pair == '11'
        tail_pair = '11'
        new_carry_on = '10'
        if carry_on == '00':
            head_pair = '01'
        elif carry_on == '01':
            head_pair = '10'
        elif carry_on == '10':
            head_pair = '11'

    combo_list = [Combo(head_pair)]
    if tail_pair == head_pair:
        combo_list[0].length = combo.length
    elif combo.length > 1:
        combo_list.append(Combo(tail_pair, combo.length - 1))

    return (combo_list, new_carry_on)

def get_next_by_pumping(groups, default_carry_on='01', shifted_carry_on='10'):
    first_index = 0
    first_combo = groups[0]
    if first_combo.pair == '00':
        first_index = 1
        first_combo = groups[1]

    carry_on = default_carry_on if first_combo.pair[1] == '1' else shifted_carry_on
    new_groups = groups[:first_index]
    last_combo = None if len(new_groups) == 0 else new_groups[0]

    for combo in groups[first_index:]:
        new_combo_list, carry_on = apply_pumping_rule(combo, carry_on)
        if last_combo is None or new_combo_list[0].pair != last_combo.pair:
            new_groups += new_combo_list
            last_combo = new_combo_list[-1]
        else:
            last_combo.length += new_combo_list[0].length
            if len(new_combo_list) > 1:
                last_combo = new_combo_list[1]
                new_groups.append(last_combo)

    if last_combo.pair == carry_on:
        last_combo.length += 1
    else:
        last_combo = Combo(carry_on)
        new_groups.append(last_combo)
    
    if last_combo.pair == '00':
        new_groups.pop()
        last_combo = new_groups[-1]
    
    return new_groups

def number_to_groups(num):
    str_num = ''.join(map(str, number_to_base(num, 2)))
    if len(str_num) % 2 == 1:
        str_num = '0' + str_num
    pairs = list(reversed([str_num[i:i+2] for i in range(0, len(str_num), 2)]))
    groups = []
    last_combo = None
    for pair in pairs:
        if last_combo is None or last_combo.pair != pair:
            last_combo = Combo(pair)
            groups.append(last_combo)
        else:
            last_combo.length += 1
    
    return groups

def groups_to_number(groups):
    map_begin = 1 if groups[0].pair == '00' else 0
    return int(''.join(reversed(list(map(lambda x: x.to_num(), groups[map_begin:])))), 2)

def run_pumping_algorithm(num=None):
    # 1048575
    if num is None:
        num = int(input('Input a number: '))
    
    groups = number_to_groups(num)
    current_num = num
    print(current_num, groups)
    while current_num > 2:
        groups = get_next_by_pumping(groups)
        current_num = groups_to_number(groups)
        print(current_num, groups)

def run_custom_pumping():
    num = int(input('Input a number in binary: '), 2)
    default_carry_on = input('Input default carry on rule: ')
    shifted_carry_on = input('Input shifted carry on rule: ')
    iterations = int(input('Input the number of iterations: '))

    groups = number_to_groups(num)
    print(groups)
    for i in range(iterations):
        groups = get_next_by_pumping(groups, default_carry_on, shifted_carry_on)
        print(groups)
    
    # 10
    # 1000
    # 011010
    # 01010000
    # 11110010
    # 1011011000
    # 100010001010
    # 01100110100000
    # 0100110011100010
    # 1110011010101000
    # 101011001111111010
    # 10000001101111110000
    # 0110000101001111010010
    # 010010001111101101111000
    # 110110101111001001101010
    # 10100100001101011101000000
    # 0111101100101000010111000010
    # 010111000101111001000101001000

    # 0010 <-
    # 1000
    # 1010
    # 0000
    # 0010 ->

    # 3^k - 1
    # 000000000000000000000000000010: 2 X
    # 000000000000000000000000001000: 8
    # 000000000000000000000000011010: 26 X
    # 000000000000000000000001010000: 80
    # 000000000000000000000011110010: 242 X
    # 000000000000000000001011011000: 728
    # 000000000000000000100010001010
    # 000000000000000001100110100000
    # 000000000000000100110011100010
    # 000000000000001110011010101000
    # 000000000000101011001111111010
    # 000000000010000001101111110000
    # 000000000110000101001111010010
    # 000000010010001111101101111000
    # 000000110110101111001001101010
    # 000010100100001101011101000000
    # 000111101100101000010111000010
    # 010111000101111001000101001000

    # Se x_{0} = (h + 1)*2^{2*k} - 1, então depois de 2*(k-1) iterações vou atingir
    # x_{2*(k-1)} = h*4*3^{2*(k-1)} + (3^{2*(k-1)} - 1)*4 + 3
    #             = ((h + 1)*3^{2*(k-1)} - 1)*4 + 3
    #             = (h + 1)*3^{2*(k-1)}*4 - 1

    # h = 10 => (10 + 1) * 2^4 - 1

    # 10101111 -> 175
    # 526
    # 263
    # 790
    # 110001011 -> 395
    # 
    # 10*4*3^{2*(2-1)} + (3^{2*(2-1)} - 1)*4 + 3
    # 10*4*9 + 8*4 + 3
    # 360 + 32 + 3
    # 395


def main():
    # run_pumping_algorithm()
    run_custom_pumping()

if __name__ == "__main__":
    main()