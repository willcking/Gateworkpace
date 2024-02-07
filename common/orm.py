from peewee import *
from wconfig import MYSQL_CONF
from playhouse.pool import MySQLDatabase
from datetime import datetime

database = MySQLDatabase(MYSQL_CONF['db'], host=MYSQL_CONF['host'], port=3306, user=MYSQL_CONF['user'], password=MYSQL_CONF['password'])


class Pair(Model):
    id = AutoField(primary_key=True, unique=True)
    uid = IntegerField(default=0)
    network = CharField(20)
    app = CharField(30)
    pair = CharField(64, unique=True, default='')
    token0 = CharField(64, default='')
    token1 = CharField(64, default='')
    token0symbol = CharField(64, default='')
    token1symbol = CharField(64, default='')
    reserve0 = DecimalField(max_digits=65, decimal_places=0, default=0)
    reserve1 = DecimalField(max_digits=65, decimal_places=0, default=0)
    rate = DecimalField(max_digits=65, decimal_places=18, default=0)
    fee = DecimalField(max_digits=65, decimal_places=0, default=0)
    valueable = IntegerField(default=0)
    arbi = IntegerField(default=0)
    updatetime = DateTimeField(default=datetime.now)

    class Meta:
        database = database
        table_name = 'pair'


class Token(Model):
    id = AutoField(primary_key=True, unique=True)
    network = CharField(10)
    address = CharField(64, unique=True)
    symbol = CharField(10)
    stable = IntegerField(default=0)
    valueable = IntegerField(default=0)
    decimal = CharField(5)
    supply = IntegerField(default=0)
    price = DecimalField(max_digits=65, decimal_places=18, default=0)
    maincoin = IntegerField(default=0)

    class Meta:
        database = database
        table_name = 'token'


class CoinLists(Model):
    id = AutoField(primary_key=True, unique=True)
    token_address = CharField(255)
    symbol = CharField(10)
    network = CharField(10)
    dex = CharField(64, null=True)
    pair_address = CharField(255, null=True)
    gate_price = DecimalField(max_digits=65, decimal_places=18, default=0, null=True)
    dex_price = DecimalField(max_digits=65, decimal_places=18, default=0, null=True)

    class Meta:
        database = database
        table_name = 'coin_lists'


class PairInfo(Model):
    id = AutoField(primary_key=True, unique=True)
    symbol = CharField(max_length=255, null=True)
    network = CharField(max_length=255, null=True)
    token_address = CharField(max_length=255, null=True)
    pair_address = CharField(max_length=255, null=True)
    liquidity = DecimalField(max_digits=10, decimal_places=2, null=True)
    #volume_24h = DecimalField(max_digits=10, decimal_places=2, null=True)
    update_at = DateTimeField(default=datetime.now)
    overlook = IntegerField(default=0)
    last_update_at = DateTimeField(null=True)
    last_liquidity = DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        database = database  # 指定模型使用的数据库
        table_name = 'pair_infos'

if __name__ == '__main__':
    database.connect()
    Pair.create_table(fail_silently=True)
    Token.create_table(fail_silently=True)
    CoinLists.create_table(fail_silently=True)
    PairInfo.create_table(fail_silently=True)
    database.close()
