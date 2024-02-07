def find_same_maincoin_pair(network, app1, app2):
    light = True
    logger.info('empty arbi mark')

    # empty valueable mark
    q = orm.Pair.update({
        'arbi': 0,
    }).where(orm.Pair.network == network)
    q.execute()

    test = SwapApp(network, app1)
    logger.info(f'find {app1} {app2} same maincoin pair, mark arbi pair.')
    maincoin_list = test.get_maincoin_and_stable_token_addrs_from_db()
    for pair_obj1 in orm.Pair().select().where(orm.Pair.network == network, orm.Pair.app == app1).iterator():
        # logger.info(f'trying pair No: {pair_obj1.uid} in app {app1}')
        str1 = pair_obj1.token0 + pair_obj1.token1
        for pair_obj2 in orm.Pair().select().where(orm.Pair.network == network, orm.Pair.app == app2).iterator():
            str2 = pair_obj2.token0 + pair_obj2.token1
            if str1 == str2 and light and (pair_obj1.token0 in maincoin_list) and (pair_obj1.token1 in maincoin_list):
                print(pair_obj2.token0, pair_obj2.token1)
                q = orm.Pair.update({
                    'arbi': 1
                }).where(orm.Pair.network == network, orm.Pair.token0 == pair_obj2.token0,
                         orm.Pair.token1 == pair_obj2.token1, orm.Pair.arbi == 0)
                q.execute()


def clear_all_valueable_token_pair(network):
    logger.info('empty valueable mark')

    # empty valueable mark
    q = orm.Token.update({
        'valueable': 0,
    }).where(orm.Token.network == network, orm.Token.valueable == 1)
    q.execute()

    # empty valueable mark
    q = orm.Pair.update({
        'valueable': 0,
    }).where(orm.Pair.network == network)
    q.execute()


def find_valueable_token_and_pair(network, app):
    logger.info(f'find valueable token network : {network} \t app: {app}')
    test = SwapApp(network, app)
    maincoin_list = test.get_maincoin_and_stable_token_addrs_from_db()
    for pair_obj in orm.Pair().select().where(orm.Pair.network == network, orm.Pair.app == app).iterator():
        if pair_obj.token0 in maincoin_list:
            if pair_obj.reserve0 * test.get_maincoin_token_price_from_db(pair_obj.token0) > VALUEABLE_COIN_LIQT:
                q = orm.Pair.update({
                    'valueable': 1
                }).where(orm.Pair.network == network, orm.Pair.pair == pair_obj.pair, orm.Pair.valueable == 0)
                q.execute()

                q = orm.Token.update({
                    'valueable': 1,
                }).where(orm.Token.network == network, orm.Token.address == pair_obj.token1, orm.Token.valueable == 0)
                q.execute()


        elif pair_obj.token1 in maincoin_list:
            if pair_obj.reserve1 * test.get_maincoin_token_price_from_db(pair_obj.token1) > VALUEABLE_COIN_LIQT:
                q = orm.Pair.update({
                    'valueable': 1
                }).where(orm.Pair.network == network, orm.Pair.pair == pair_obj.pair, orm.Pair.valueable == 0)
                q.execute()

                q = orm.Token.update({
                    'valueable': 1,
                }).where(orm.Token.network == network, orm.Token.address == pair_obj.token0, orm.Token.valueable == 0)
                q.execute()


def find_stable_token(network):
    logger.info('set stable coin through wconfig')

    for k, v in STABLECOIN[network].items():
        q = orm.Token.update({
            'stable': 1,
        }).where(orm.Token.address == v, orm.Token.stable != 1)
        q.execute()


def clear_all_maincoin_token(network):
    logger.info('empty maincoin mark')
    # empty maincoin mark
    q = orm.Token.update({
        'maincoin': 0,
    }).where(orm.Token.network == network)
    q.execute()


# usdt valueable token必然有一个稳定币/主流币的交易对
def calc_valueable_token_price(network, app, token_addr):
    test = SwapApp(network, app)
    # if token_addr == '0x1e6395E6B059fc97a4ddA925b6c5ebf19E05c69f':
    #     print('debug')
    logger.info(f'calc valueable token {token_addr} using {app} :')
    stable_token_list = test.get_stable_token_addrs_from_db()
    maincoin_list = test.get_maincoin_token_addrs_from_db()

    if token_addr in stable_token_list:
        token_price = 1
        return token_price

    if token_addr in maincoin_list:
        token_price = test.get_maincoin_token_price_from_db(token_addr)
        return token_price

    for pair_obj in orm.Pair().select().where(orm.Pair.network == network, orm.Pair.app == app,
                                              orm.Pair.valueable == 1).iterator():
        if (pair_obj.token0 in maincoin_list) and (pair_obj.token1 == token_addr):
            maincoin_price = test.get_maincoin_token_price_from_db(pair_obj.token0)
            _rate = test.get_token_pair_rate(pair_obj.pair)
            if _rate > 0:
                token_price = float(maincoin_price) / _rate
                return token_price
            else:
                return 0
        if (pair_obj.token1 in maincoin_list) and (pair_obj.token1 == token_addr):
            maincoin_price = test.get_maincoin_token_price_from_db(pair_obj.token1)
            if maincoin_price > 0:
                token_price = test.get_token_pair_rate(pair_obj.pair) / float(maincoin_price)
                return token_price
            else:
                return 0
    return 0


# usdt valueable token必然有一个usdt或者husd的交易对
def calc_maincoin_token_price(network, app, token_addr):
    test = SwapApp(network, app)
    logger.debug(f'calc maincoin  {token_addr} ')
    stable_token_list = test.get_stable_token_addrs_from_db()

    if token_addr in stable_token_list:
        token_price = 1
        return token_price
    for pair_obj in orm.Pair().select().where(orm.Pair.network == network, orm.Pair.app == app).iterator():
        # logger.info(pair_obj.uid)
        # if pair_obj.uid < 991:
        #     return
        if (pair_obj.token0 in stable_token_list) and (pair_obj.token1 == token_addr):
            _rate = test.get_token_pair_rate(pair_obj.pair)
            if _rate > 0:
                token_price = 1 / test.get_token_pair_rate(pair_obj.pair)
                return token_price
            else:
                return 0
        if (pair_obj.token1 in stable_token_list) and (pair_obj.token1 == token_addr):
            token_price = test.get_token_pair_rate(pair_obj.pair)
            return token_price
    return 0


def calc_all_maincoin_price(network, app):
    test = SwapApp(network, app)
    logger.info('calc all maincoin token price...')
    valueable_token_list = test.get_maincoin_token_addrs_from_db()
    for token_addr in valueable_token_list:
        p = calc_maincoin_token_price(network, app, token_addr)
        logger.debug(f'token:  {token_addr} price: {p}')
        q = orm.Token.update({
            'price': p,
        }).where(orm.Token.network == network, orm.Token.address == token_addr)
        q.execute()


def calc_all_valueable_price(network, app):
    test = SwapApp(network, app)
    logger.info('calc all valueable token price...')
    valueable_token_list = test.get_valueable_token_addrs_from_db()
    for token_addr in valueable_token_list:
        p = calc_valueable_token_price(network, app, token_addr)
        logger.info(f'token:  {token_addr} price: {p}')
        q = orm.Token.update({
            'price': p,
        }).where(orm.Token.network == network, orm.Token.address == token_addr)
        q.execute()


def find_maincoin_token(network, app):
    logger.info(f'find maincoin token network : {network} \t app: {app}')
    test = SwapApp(network, app)
    stable_coin_list = test.get_stable_token_addrs_from_db()

    for pair_obj in orm.Pair().select().where(orm.Pair.network == network, orm.Pair.app == app).iterator():
        if pair_obj.token0 in stable_coin_list:
            if pair_obj.reserve0 * test.get_maincoin_token_price_from_db(pair_obj.token0) > MAIN_COIN_LIQT:
                q = orm.Token.update({
                    'maincoin': 1,
                    'valueable': 1
                }).where(orm.Token.network == network, orm.Token.address == pair_obj.token1,
                         orm.Token.valueable == 0 or orm.Token.maincoin == 0)
                q.execute()

        elif pair_obj.token1 in stable_coin_list:
            if pair_obj.reserve1 * test.get_maincoin_token_price_from_db(pair_obj.token1) > MAIN_COIN_LIQT:
                q = orm.Token.update({
                    'maincoin': 1,
                    'valueable': 1
                }).where(orm.Token.network == network, orm.Token.address == pair_obj.token0,
                         orm.Token.valueable == 0 or orm.Token.maincoin == 0)
                q.execute()


def update_pair_rate(network, app):
    test = SwapApp(network, app)
    logger.info(f'updating pair rate.{network} - {app}..')
    for pair_obj in orm.Pair().select().where(orm.Pair.network == network, orm.Pair.app == app).iterator():
        # debug
        rate = test.get_token_pair_rate(pair_obj.pair)
        logger.info(f'updating pair rate.{network} - {app} - {pair_obj.uid} - {pair_obj.pair}..')
        q = orm.Pair.update({
            'rate': rate
        }).where(orm.Pair.network == network, orm.Pair.app == app, orm.Pair.pair == pair_obj.pair)
        q.execute()


def get_token_price_from_db(network, token_addr):
    token = orm.Token().select().where(orm.Token.network == network, orm.Token.address == token_addr)
    return token[0].price
