import logging

class Logger:
    
    def __init__(self) -> None:
        logging.basicConfig(
            format="%(asctime)s %(levelname)s %(message)s",
            encoding="utf-8",
            filename=r"F:\Others\Car Collection Project\Python API\app.log",
            datefmt="%d/%m/%Y %H:%M:%S",
            level=logging.DEBUG
        )
        self.logger = logging.getLogger()
        
    def debug(self, data) -> None:
        self.logger.debug(data)