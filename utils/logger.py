def setup_logger():
    import logging
    return logging.basicConfig(
        format='[%(filename)s:%(lineno)d] %(message)s',
        
    )