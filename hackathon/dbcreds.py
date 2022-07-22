USERNAME : str = 'dbmasteruser'
PASSWORD : str = 'c)mXy>ml(^mppU06AxEq(6$(wBpiaX~u'
ENDPOINT : str = 'ls-5d10316d4c2b154c1238f6ca9678d73c9337d14d.c5ytruwzr1p7.ap-southeast-1.rds.amazonaws.com'
PORT : int = 3306
DATABASE : str = 'multicurrency'

DIALECT_DRIVER : str = 'mysql'

ENGINE_STR : str = f'{DIALECT_DRIVER}://{USERNAME}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}'