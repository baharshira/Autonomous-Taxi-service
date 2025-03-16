def id_generator():
    """Generator function for unique request IDs"""
    id = 1
    while True:
        yield id
        id += 1