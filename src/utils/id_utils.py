def create_id_generator():
    """Generator function for unique request IDs"""
    current_id = 1

    while True:
        yield current_id
        current_id += 1