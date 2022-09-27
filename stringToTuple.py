def str_tuple_decode_to_tuple( tuple_str: bytes) -> tuple:
    decode = tuple_str.decode()
    tup_data = decode[1:-1].split(",")
    ip = tup_data[0].split("'")[1]
    type = tup_data[1].split("'")[1]
    return ip, type