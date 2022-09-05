def count_chars(num):
    return len(str(num))

def print_spaced(num, space, *args, **kwargs):
    digits = count_chars(num)
    extra_space = max(0, space - digits - 1)
    
    align = kwargs.get('align')
    if align is not None:
        del kwargs['align']
    else:
        align = 'left'
    
    if align == 'left':
        print(num, ' ' * extra_space, *args, **kwargs)
    elif align == 'right':
        print(' ' * extra_space, num, *args, **kwargs)