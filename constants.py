from selenium import webdriver
import socket

scrape_from = {'sanim': 'sanim',
               'arzeshafzoodeh': 'arzeshafzoodeh'}


def scrape_from():
    return scrape_from


def get_months():

    months = ['01', '02', '03', '04', '05',
              '06', '07', '08', '09', '10', '11', '12']

    return months


def get_table_names():
    table_names = [
        'tblGhateeSazi',
        'tblTashkhisSaderShode',
        'tblTashkhisEblaghShode',
        'tblGhateeSaderShode',
        'tblGhateeEblaghShode',
        'tblbadvitakmilshode',
        'tblbadvidarjariandadrasi',
        'tbltajdidnazerdarjariandadrasi',
        'tbltajdidnazartakmilshode',
        'tblEjraeeSaderShode',
        'tblEjraeeEblaghShode'
    ]

    return table_names


def get_server_namesV1():

    server_names = [
        {'ahwaz': r'10.52.0.50\ahwaz'},
        {'abadan': r'10.52.112.130\abadan'},
        {'khoramshahr': r'10.52.224.130\khoramshahr'},
        {'shadegan': r'10.53.64.130\SHADEGAN'},
        {'mahshahr': r'10.53.128.130\mahshahr'},
        {'bandaremam': r'10.53.208.130\BANDAREMAM'},
        {'hendijan': r'10.53.192.130\HENDIJAN'},
        {'shooshtar': r'10.53.96.130\SHOOSHTAR'},
        {'mis': r'10.53.144.130\MIS'},
        {'gotvand': r'10.53.112.130\GOTVAND'},
        {'shuosh': r'10.53.80.130\SHUOSH'},
        {'dezful': r'10.52.240.130\Dezful'},
        {'andimeshk': r'10.52.160.130\Andimeshk'},
        {'behbahan': r'10.52.208.130\Behbahan'},
        {'izeh': r'10.52.176.130\Izeh'},
        {'baghmalek': r'10.52.192.130\BAGHMALEK'},
        {'ramhormoz': r'10.53.16.130\ramhormoz'},
        {'haftkel': r'10.53.176.130\HAFTKEL'},
        {'omidieh': r'10.52.144.130\OMIDIEH'},
        {'aghajari': r'10.52.128.130\Aghajari'},
        {'ramshir': r'10.53.0.130\ramshir'},
        {'sosangerd': r'10.53.32.130\Sosangerd'},
        {'lali': r'10.53.160.130\lali'},
        {'hoveyze': r'10.53.48.130\hoveyze'},
    ]

    return server_names


def get_server_namesV2():

    server_names = [
        ('ahwaz', r'10.52.0.50\ahwaz'),
        ('abadan', r'10.52.112.130\abadan'),
        ('khoramshahr', r'10.52.224.130\khoramshahr'),
        ('shadegan', r'10.53.64.130\SHADEGAN'),
        ('mahshahr', r'10.53.128.130\mahshahr'),
        ('bandaremam', r'10.53.208.130\BANDAREMAM'),
        ('hendijan', r'10.53.192.130\HENDIJAN'),
        ('shooshtar', r'10.53.96.130\SHOOSHTAR'),
        ('mis', r'10.53.144.130\MIS'),
        ('gotvand', r'10.53.112.130\GOTVAND'),
        ('shuosh', r'10.53.80.130\SHUOSH'),
        ('dezful', r'10.52.240.130\Dezful'),
        ('andimeshk', r'10.52.160.130\Andimeshk'),
        ('behbahan', r'10.52.208.130\Behbahan'),
        ('izeh', r'10.52.176.130\Izeh'),
        ('baghmalek', r'10.52.192.130\BAGHMALEK'),
        ('ramhormoz', r'10.53.16.130\ramhormoz'),
        ('haftkel', r'10.53.176.130\HAFTKEL'),
        ('omidieh', r'10.52.144.130\OMIDIEH'),
        ('aghajari', r'10.52.128.130\Aghajari'),
        ('ramshir', r'10.53.0.130\ramshir'),
        ('sosangerd', r'10.53.32.130\Susangerd'),
        ('lali', r'10.53.160.130\lali'),
        ('hoveyze', r'10.53.48.130\hoveyze'),
    ]

    return server_names


years = [
    ('all', '0'),
    ('common_years', '1'),
    ('1392', '92'),
    ('1393', '93'),
    ('1394', '94'),
    ('1395', '95'),
    ('1396', '96'),
    ('1397', '97'),
    ('1398', '98'),
    ('1399', '99'),
    ('1400', '00'),
    ('1401', '01'),
]

dict_years = {
    'all': '0',
    'common_years': '1',
    '1387': '87',
    '1388': '88',
    '1389': '89',
    '1390': '90',
    '1391': '91',
    '1392': '92',
    '1393': '93',
    '1394': '94',
    '1395': '95',
    '1396': '96',
    '1397': '97',
    '1398': '98',
    '1399': '99',
    '1400': '00',
    '1401': '01',
}


def get_dict_years():
    return dict_years


all_years = years[0][1]
common_years = years[1][1]


def get_all_years():
    return all_years


def get_common_years():
    return common_years


lst_reports = [
    ('common_reports', '0'),
    ('heiat_reports', '00'),
    ('ezhar', '1'),
    ('hesabrasi_darjarian_before5', '2'),
    ('hesabrasi_darjarian_after5', '3'),
    ('hesabrasi_takmil_shode', '4'),
    ('tashkhis_sader_shode', '5'),
    ('tashkhis_eblagh_shode', '6'),
    ('tashkhis_eblagh_nashode', '7'),
    ('tashkhis_motamam', '8'),
    ('eteraz_darjarian_dadrasi', '9'),
    ('eteraz_takmil_shode', '10'),
    ('badvi_darjarian_dadrasi', '11'),
    ('badvi_takmil_shode', '12'),
    ('tajdidnazer_darjarian_dadrasi', '13'),
    ('tajdidnazar_takmil_shode', '14'),
    ('ghatee_sader_shode', '15'),
    ('ghatee_eblagh_shode', '16'),
    ('ghatee_eblagh_nashode', '17'),
    ('ejraee_sader_shode', '18'),
    ('ejraee_eblagh_shode', '19'),
    ('case_ejraee', '20'),
    ('1000_parvande', '21')
]

comm_reports = lst_reports[0][1]
heiat = lst_reports[1][1]


def get_comm_reports():
    return comm_reports


def get_heiat():
    return heiat


common_reports = [
    'ezhar',
    'tashkhis_sader_shode',
    'tashkhis_eblagh_shode',
    'ghatee_sader_shode',
    'ghatee_eblagh_shode',
]

heiat_reports = lst_reports[12:16]


def get_heiat_reports():
    return heiat_reports


common_years = years[5:]
comm_years = years[1][1]


def get_common_years():
    return common_years


def get_comm_years():
    return comm_years


def get_common_reports():
    return common_reports


def get_lst_reports():
    return lst_reports


def get_years():
    return years[2:]


def get_str_years():
    str_years = 'types:\n'
    for year in years:
        str_years += '%s=%s\n' % (year[0], year[1])

    return str_years


def get_str_help():
    str_help = 'Report types:'
    for item in lst_reports:
        str_help += '%s=%s,\n' % (item[0], item[1])

    return str_help


def get_ip():
    host_name = socket.gethostname()
    ip_addr = socket.gethostbyname(host_name)

    return ip_addr


def geck_location(set_save_dir=False, driver_type='firefox'):

    ip_addr = get_ip()

    if (set_save_dir and (ip_addr == '10.52.99.131')):
        return r'H:\پروژه اتوماسیون گزارشات\monthly_reports\saved_dir'

    if (set_save_dir and (ip_addr == '10.52.0.114')):
        return r'E:\automating_reports_V2\saved_dir'

    if ip_addr == '10.52.99.131' and driver_type == 'chrome':
        return r'E:\automating_reports_V2\chromedriver.exe'

    if ip_addr == '10.52.0.114' and driver_type == 'chrome':
        return r'E:\automating_reports_V2\chromedriver.exe'

    if ip_addr == '10.52.99.131':
        return r'H:\driver\geckodriver.exe'

    else:
        return r'C:\Users\alkav\Desktop\python codes\geckodriver.exe'


def set_gecko_prefs(pathsave):
    fp = webdriver.FirefoxProfile()
    fp.set_preference('browser.download.folderList', 2)
    fp.set_preference('browser.download.manager.showWhenStarting', False)
    fp.set_preference('browser.download.dir', pathsave)
    fp.set_preference('browser.helperApps.neverAsk.openFile',
                      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    fp.set_preference('browser.helperApps.neverAsk.saveToDisk',
                      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    fp.set_preference('browser.helperApps.alwaysAsk.force', False)
    fp.set_preference('browser.download.manager.alertOnEXEOpen', False)
    fp.set_preference('browser.download.manager.focusWhenStarting', False)
    fp.set_preference('browser.download.manager.useWindow', False)
    fp.set_preference('browser.download.manager.showAlertOnComplete', False)
    fp.set_preference('browser.download.manager.closeWhenDone', False)

    return fp


def get_sql_con(server='.', database='testdb', username='sa', password='14579Ali'):

    constr = 'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + \
        database + ';UID=' + username + ';PWD=' + password

    return constr


def get_remote_sql_con():
    server = '10.52.0.114'
    database = 'TestDb'
    username = 'sa'
    password = '14579Ali'
    constr = 'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + \
        database + ';UID=' + username + ';PWD=' + password

    return constr
