#


# int-str converters
def int_list_to_str(l):
    return ','.join(map(str, l))


def str_list_to_in(l):
    return list(map(int, l.split(",")))

# -- print (sorted(str_list_to_in('1,2,5,4,3,0,6')))
