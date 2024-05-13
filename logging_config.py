import logging
from logging.handlers import RotatingFileHandler

#рывень логування
logging.basicConfig(level=logging.DEBUG)

# крейт логгера
logger = logging.getLogger('my_logger')

# крейт форматеру
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Створення хендлера для запису до файлу
file_handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# додаю хендлер до логгера !!!!!
logger.addHandler(file_handler)

# логгер для запису повідомлень аааааа
logger.debug('Це повідомлення з рівнем DEBUG')
logger.info('Це повідомлення з рівнем INFO')
logger.warning('Це повідомлення з рівнем WARNING')
logger.error('Це повідомлення з рівнем ERROR')
logger.critical('Це повідомлення з рівнем CRITICAL')
