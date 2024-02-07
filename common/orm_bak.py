# coding: utf-8
import peewee
import os
from playhouse.sqlite_ext import SqliteExtDatabase

from wconfig import DATA_PATH


# Set the path to the database file
database_path = DATA_PATH + 'swapbot.db'
print(database_path)

# Check if the path to the database file is correct
if not os.path.exists(database_path):
    raise Exception(f"The database file does not exist at the specified path: {database_path}")

# Check if the file is accessible and writable
if not os.access(database_path, os.R_OK):
    raise Exception(f"The database file at {database_path} is not readable. Check permissions.")

if not os.access(database_path, os.W_OK):
    raise Exception(f"The database file at {database_path} is not writable. Check permissions.")

# Check if the directory is accessible and writable
directory = os.path.dirname(database_path)
if not os.access(directory, os.W_OK):
    raise Exception(f"The directory at {directory} is not writable. Check permissions.")

print("The database file path and permissions are correct.")

db = SqliteExtDatabase(database_path)


class Pair(peewee.Model):
    id = peewee.IntegerField(primary_key=True, unique=True)
    uid = peewee.IntegerField(default=0)
    network = peewee.CharField(10)
    app = peewee.CharField(10)
    pair = peewee.CharField(64, unique=True, default='')
    token0 = peewee.CharField(64, default='')
    token1 = peewee.CharField(64, default='')
    token0symbol = peewee.CharField(64, default='')
    token1symbol = peewee.CharField(64, default='')
    reserve0 = peewee.DecimalField(max_digits=80, decimal_places=0, default=0)
    reserve1 = peewee.DecimalField(max_digits=80, decimal_places=0, default=0)
    rate = peewee.DecimalField(max_digits=80, decimal_places=18, default=0)
    valueable = peewee.IntegerField(default=0)
    arbi = peewee.IntegerField(default=0)

    # @classmethod
    # def list_by_port(cls, port) -> peewee.ModelSelect:
    #     """
    #     返回对应端口的所有用户
    #     :param port:
    #     :return:
    #     """
    #     return cls.select().where(cls.port == int(port)).order_by(cls.single_port_access_weight.desc())

    class Meta:
        database = db


class Token(peewee.Model):
    id = peewee.IntegerField(primary_key=True, unique=True)
    network = peewee.CharField(10)
    address = peewee.CharField(64, unique=True)
    symbol = peewee.CharField(10)
    stable = peewee.IntegerField(default=0)
    valueable = peewee.IntegerField(default=0)
    decimal = peewee.CharField(5)
    supply = peewee.IntegerField(default=0)
    price = peewee.DecimalField(max_digits=80, decimal_places=18, default=0)
    maincoin = peewee.IntegerField(default=0)

    class Meta:
        database = db



class CoinLists(peewee.Model):
    token_address = peewee.CharField(255)
    symbol = peewee.CharField(10)
    network = peewee.CharField(10)
    dex = peewee.CharField(64)
    pair_address = peewee.CharField(255)
    gate_price = peewee.DecimalField(max_digits=80, decimal_places=18, default=0)
    dex_price = peewee.DecimalField(max_digits=80, decimal_places=18, default=0)

    class Meta:
        database = db
        table_name = 'coin_lists'  # 如果数据库表名与模型类名不一致，需要指定table_name


db.connect()

# Pair.drop_table()
# Token.drop_table()

Pair.create_table(fail_silently=True)
Token.create_table(fail_silently=True)
