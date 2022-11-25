from import_tgju import import_tgju
sys, pd, Scrape, maybe_make_dir, get_update_date, \
    drop_into_db, get_sql_con, time, \
    datetime, log, internet_on, done_log, run_tgju_log, get_shared_var = import_tgju()

path = r'D:\projects\win_automation\saved_dir\tgju'
dates = []
golds = []
dollars = []
coins = []
eng_dates = []
g_last_coin = '0'
last_gold = 0
last_dollar = 0
maybe_make_dir([path])


@log
def compare_prices(coin, last_coin):
    if abs(coin - last_coin) > 100_000:
        return True
    return False


def createdf_and_dropToSql(*args):
    df = pd.DataFrame(
        {'date': args[0], 'eng_date': args[1], 'gold': args[2], 'coin': args[3], 'dollar': args[4]})

    drop_into_db('tblTgju', df.columns.tolist(), df.values.tolist(),
                 sql_con=get_sql_con(password='14579Ali.'),
                 append_to_prev=True)


@done_log
def set_done(done=False):
    return done


@run_tgju_log
def run_tgju(done=False, headless=True):
    global g_last_coin
    while not done:
        if get_shared_var():
            break
        try:
            time.sleep(1)
            if internet_on():
                try:
                    x = Scrape()
                    coin, dollar, gold = x.scrape_tgju(
                        path=path, headless=headless)
                    if compare_prices(coin=int(coin.replace(',', '')), last_coin=int(g_last_coin.replace(',', ''))):
                        g_last_coin, last_gold, last_dollar = coin, gold, dollar
                        eng_date = str(datetime.datetime.now())
                        date = get_update_date()
                        dates.append(date)
                        golds.append(gold)
                        dollars.append(dollar)
                        coins.append(coin)
                        eng_dates.append(eng_date)

                        time.sleep(1)

                    if len(dates) == 1:
                        createdf_and_dropToSql(
                            dates, eng_dates, golds, coins, dollars)
                        eng_dates.clear(), dollars.clear(), coins.clear(), golds.clear(), dates.clear()

                    continue
                except KeyboardInterrupt:
                    done = set_done(done=True)
                except Exception as e:
                    if len(dates) > 0:
                        createdf_and_dropToSql(
                            dates, eng_dates, golds, coins, dollars)
                        eng_dates.clear(), dollars.clear(), coins.clear(), golds.clear(), dates.clear()
                    print(e)
                    continue

            else:
                continue
        except KeyboardInterrupt:
            done = set_done(done=True)


if __name__ == '__main__':
    try:
        run_tgju(headless=True)
    except KeyboardInterrupt:
        set_done(done=True)
