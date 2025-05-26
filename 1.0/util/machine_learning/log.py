from loguru import logger

logger.add('model-debug.log', level='DEBUG', rotation='5MB')
logger.add('model-info.log', level='INFO', rotation='5MB')
