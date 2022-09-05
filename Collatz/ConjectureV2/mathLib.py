def get_factors(num):
    factor = 2
    array = []
    while num != 1:
        while num % factor == 0:
            num //= factor
            array.append(factor)
        factor += 1
    return array

def even_rule(num):
    return num // 2

def odd_rule(num):
    return 3 * num + 1

def iterated_collatz(num):
    while num != 1:
        if num % 2 == 0:
            yield 0, num
            num = even_rule(num)
        else:
            yield 1, num
            num = odd_rule(num)
    yield 1, 1

def collatz(num):
    odd_count = 0
    even_count = 0

    for parity, partial in iterated_collatz(num):
        if parity == 0:
            even_count += 1
        elif partial != 1:
            odd_count += 1
    
    return even_count, odd_count

def calculate_smooth(power_list):
    smooth = 0
    for three_power, two_power in enumerate(power_list):
        smooth += 3 ** three_power * 2 ** two_power
    return smooth

def power_mod(base1, exp1, base2, exp2):
    '''
    Given two powers, b_1^{e_1} and b_2^{e_2}, calculates b_1^{e_1} mod b_2^{e_2}.
    '''
    power2 = base2 ** exp2
    reminder = 1

    for _ in range(exp1):
        reminder *= base1
        reminder %= power2
    
    return reminder

def pascal(num_lines):
    lines = [[1]]

    for i in range(num_lines - 1):
        prev_line = lines[i]
        line = [1, 1]
        for i in range(1, len(prev_line)):
            line.insert(1, prev_line[i] + prev_line[i - 1])
        lines.append(line)
    
    return lines

def number_to_base(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]

def iterated_syracuse(num):
    even_count = 0
    for parity, partial in iterated_collatz(num):
        if parity == 1:
            yield partial, even_count
            even_count = 0
        else:
            even_count += 1

def smooth_power_reminder(starting_number, smooth_exps):
    next_two_exp = smooth_exps[0] + 1
    next_two_power = 2 ** next_two_exp
    smooth_size = len(smooth_exps)
    return (sum([
        (2 ** two_exp * power_mod(3, smooth_size - i - 1, 2, next_two_exp)) % next_two_power
        for i, two_exp in enumerate(reversed(smooth_exps))
    ]) + starting_number * power_mod(3, smooth_size, 2, next_two_exp)) % next_two_power

def iterated_mod_2_syracuse(starting_number):
    two_factor_count = 0
    odd_count = 0

    while starting_number % 2 == 0:
        starting_number //= 2
        two_factor_count += 1

    yield starting_number, odd_count, two_factor_count, [0]
    
    partial_number = starting_number
    while partial_number != 1:
        two_exp_counter = 1
        smooth_exps = [0]
        for _ in range(odd_count - 1):
            smooth_exps.insert(0, two_exp_counter)
            reminder = -1
            while reminder != 0:
                smooth_exps[0] = two_exp_counter
                two_exp_counter += 1
                reminder = smooth_power_reminder(starting_number, smooth_exps)
        two_exp = 0
        partial_number = calculate_smooth(smooth_exps) + starting_number * 3 ** odd_count
        while partial_number % 2 == 0:
            partial_number //= 2
            two_exp += 1
        odd_count += 1
        yield partial_number, odd_count, two_exp + two_factor_count, smooth_exps