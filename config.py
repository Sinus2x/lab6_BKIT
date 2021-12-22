from enum import Enum

# Токент бота
TOKEN = "5078527545:AAHq88BwbHGOo2MGbysfrRbZWz5PfMsm47U"

# Файл базы данных Vedis
db_file = "db.vdb"

# Ключ записи в БД для текущего состояния
CURRENT_STATE = "CURRENT_STATE"

# Состояния автомата
class States(Enum):
    STATE_START = "STATE_START"  # Начало нового диалога
    STATE_RUBLE = "STATE_RUBLE"
    STATE_COURSE = "STATE_COURSE"
    STATE_CONV = "STATE_CONV"