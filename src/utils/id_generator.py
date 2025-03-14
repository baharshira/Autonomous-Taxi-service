# Generator function for unique taxi IDs
def id_generator():
    id = 1
    while True:
        yield id
        id += 1