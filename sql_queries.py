import time
import jdatetime


def get_update_date():
    x = jdatetime.date.today()
    if len(str(x.month)) == 1:
        month = '0%s' % str(x.month)

    else:
        month = str(x.month)
    if len(str(x.day)) == 1:
        day = '0%s' % str(x.day)

    else:
        day = str(x.day)

    year = str(x.year)

    update_date = year + month + day

    return update_date


def replace_last(phrase, strToReplace=',', replacementStr=''):

    # Search for the last occurrence of substring in string
    pos = phrase.rfind(strToReplace)
    if pos > -1:
        # Replace last occurrences of substring 'is' in string with 'XX'
        phrase = phrase[:pos] + replacementStr + \
            phrase[pos + len(strToReplace):]

    return phrase


def table_name(report_type, year):

    if (report_type == 'ezhar'):
        table = '[testdb].[dbo].[tblGhateeSazi%s]' % year

    elif (report_type == 'tashkhis_sader_shode'):
        table = '[testdb].[dbo].[tblTashkhisSaderShode%s]' % year

    elif (report_type == 'tashkhis_eblagh_shode'):
        table = '[testdb].[dbo].[tblTashkhisEblaghShode%s]' % year

    elif (report_type == 'ghatee_sader_shode'):
        table = '[testdb].[dbo].[tblGhateeSaderShode%s]' % year

    elif (report_type == 'ghatee_eblagh_shode'):
        table = '[testdb].[dbo].[tblGhateeEblaghShode%s]' % year

    elif (report_type == '1000_parvande'):
        table = '[testdb].[dbo].[tbl1000Parvande%s]' % year

    elif (report_type == 'badvi_darjarian_dadrasi'):
        table = '[testdb].[dbo].[tblbadvidarjariandadrasi%s]' % year

    elif (report_type == 'badvi_takmil_shode'):
        table = '[testdb].[dbo].[tblbadvitakmilshode%s]' % year

    elif (report_type == 'tajdidnazer_darjarian_dadrasi'):
        table = '[testdb].[dbo].[tbltajdidnazerdarjariandadrasi%s]' % year

    elif (report_type == 'tajdidnazar_takmil_shode'):
        table = '[testdb].[dbo].[tbltajdidnazartakmilshode%s]' % year

    return table


def sql_delete(table):

    return """
                    BEGIN TRANSACTION
                            BEGIN TRY 
                        
                                IF Object_ID('%s') IS NOT NULL DROP TABLE %s
                        
                                COMMIT TRANSACTION;
                                
                            END TRY
                            BEGIN CATCH
                                ROLLBACK TRANSACTION;
                            END CATCH
                    """ % (table, table)


def create_sql_table(table, columns):

    temp = ''

    for c in columns:
        temp += '[%s] NVARCHAR(MAX) NULL,\n' % c

    sql_query = """
    BEGIN TRANSACTION
    BEGIN TRY 

        IF Object_ID('%s') IS NULL
        
        CREATE TABLE %s
        (
         [ID] [int] IDENTITY(1,1) NOT NULL,
         PRIMARY KEY (ID),
         %s
                                  
       
         )

        COMMIT TRANSACTION;
        
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
    END CATCH
    """ % (table, table, temp)

    # time.sleep(400)
    return sql_query


def insert_into(table, columns):
    temp = ''
    values = ''

    for c in columns:
        temp += '[%s],' % c

        values += '?,'

    values = replace_last(values)
    temp = replace_last(temp)
    # temp = temp.replace('[تاریخ بروزرسانی],', '[تاریخ بروزرسانی]', 1)

    sql_insert = """
    BEGIN TRANSACTION
    BEGIN TRY 

         INSERT INTO %s
           (
        %s         
            )
           
           VALUES
           (%s)

        COMMIT TRANSACTION;
        
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
    END CATCH
    """ % (table, temp, values)

    return sql_insert


def insert_into_tblAnbareKoliHist(year):

    sql_query = """
    
        
    
INSERT INTO tblAnbareKoliHist%s
SELECT 
%s AS [تاریخ بروزرسانی]
,Base.*
,hesabrasi.[سال عملکرد]
,hesabrasi.[tashkhisSadere]
,hesabrasi.[eblaghTashkhis]
,hesabrasi.[ghateeSadere]
,hesabrasi.[eblaghGhatee]

 FROM 

(SELECT 
[کد اداره]
,[نام اداره]
,ISNULL([مالیات بر درآمد شرکت ها],0)AS[مالیات بر درآمد شرکت ها]
,ISNULL([مالیات بر درآمد مشاغل],0)AS[مالیات بر درآمد مشاغل]
,ISNULL([مالیات بر ارزش افزوده],0)AS[مالیات بر ارزش افزوده]

 FROM
(SELECT 
[کد اداره]
,[نام اداره]
,[منبع مالیاتی]
,count([منبع مالیاتی]) AS [tedad]
 FROM

(SELECT main.*
,[tblTashkhisSaderShode%s].[تاریخ صدور برگه تشخیص]
,[dbo].[tblTashkhisEblaghShode%s].[تاریخ ابلاغ تشخیص] as [تاریخ ابلاغ تشخیص]
,[dbo].[tblGhateeSaderShode%s].[تاریخ برگ قطعی صادر شده] as [تاریخ برگ قطعی]
,[dbo].[tblGhateeEblaghShode%s].[تاریخ ابلاغ برگ قطعی]
,1 as tedad
FROM
(SELECT * FROM [dbo].[tblGhateeSazi%s]
WHERE 
[سال عملکرد]=%s
and [منبع مالیاتی] IN(N'مالیات بر درآمد شرکت ها',N'مالیات بر درآمد مشاغل')
and [نوع ریسک اظهارنامه] IN (
N'اظهارنامه برآوردی صفر'
,
N'انتخاب شده بدون اعمال معیار ریسک'
,
N'رتبه ریسک بالا'
,
N'مودیان مهم با ریسک بالا'
)
UNION
SELECT * FROM [dbo].[tblGhateeSazi%s]
WHERE [منبع مالیاتی]=N'مالیات بر ارزش افزوده' and [سال عملکرد]=%s
and [شناسه ملی / کد ملی (TIN)] IN
(SELECT [شناسه ملی / کد ملی (TIN)] FROM [dbo].[tblGhateeSazi%s] WHERE [سال عملکرد]=%s and [منبع مالیاتی] IN(N'مالیات بر درآمد شرکت ها',N'مالیات بر درآمد مشاغل')and [نوع ریسک اظهارنامه] IN (N'اظهارنامه برآوردی صفر',N'انتخاب شده بدون اعمال معیار ریسک',N'رتبه ریسک بالا',N'مودیان مهم با ریسک بالا'))
) as main
LEFT JOIN
[dbo].[tblTashkhisSaderShode%s]
ON 
[dbo].[tblTashkhisSaderShode%s].[شناسه اظهارنامه]=main.[شناسه اظهارنامه] and [tblTashkhisSaderShode%s].[سال عملکرد]=%s
LEFT JOIN
[dbo].[tblTashkhisEblaghShode%s]
ON
[dbo].[tblTashkhisEblaghShode%s].[شناسه اظهارنامه]=main.[شناسه اظهارنامه] and [tblTashkhisEblaghShode%s].[سال عملکرد]=%s
LEFT JOIN
[dbo].[tblGhateeSaderShode%s]
ON 
[dbo].[tblGhateeSaderShode%s].[شناسه اظهارنامه]=main.[شناسه اظهارنامه]and [tblGhateeSaderShode%s].[سال عملکرد]=%s
LEFT JOIN
[dbo].[tblGhateeEblaghShode%s]
ON
[dbo].[tblGhateeEblaghShode%s].[شناسه اظهارنامه]=main.[شناسه اظهارنامه]and [tblGhateeEblaghShode%s].[سال عملکرد]=%s
)as a
group by 

[کد اداره]
,[نام اداره]
,[منبع مالیاتی]

)
 src
pivot
(
  sum(tedad)
  for [منبع مالیاتی] in ([مالیات بر درآمد شرکت ها],[مالیات بر درآمد مشاغل],[مالیات بر ارزش افزوده])
) piv) AS base

LEFT JOIN


(SELECT 
[کد اداره]
,[نام اداره]
,[سال عملکرد]
,count([تاریخ صدور برگه تشخیص]) AS  [tashkhisSadere]
,count([تاریخ ابلاغ تشخیص]) AS  [eblaghTashkhis]
,count([تاریخ برگ قطعی]) AS [ghateeSadere]
,count([تاریخ ابلاغ برگ قطعی]) AS [eblaghGhatee]
 FROM

(SELECT main.*
,[tblTashkhisSaderShode%s].[تاریخ صدور برگه تشخیص]
,[dbo].[tblTashkhisEblaghShode%s].[تاریخ ابلاغ تشخیص] as [تاریخ ابلاغ تشخیص]
,[dbo].[tblGhateeSaderShode%s].[تاریخ برگ قطعی صادر شده] as [تاریخ برگ قطعی]
,[dbo].[tblGhateeEblaghShode%s].[تاریخ ابلاغ برگ قطعی]
,1 as tedad
FROM
(SELECT * FROM [dbo].[tblGhateeSazi%s]
WHERE 
[سال عملکرد]=%s
and [منبع مالیاتی] IN(N'مالیات بر درآمد شرکت ها',N'مالیات بر درآمد مشاغل')
and [نوع ریسک اظهارنامه] IN (
N'اظهارنامه برآوردی صفر'
,
N'انتخاب شده بدون اعمال معیار ریسک'
,
N'رتبه ریسک بالا'
,
N'مودیان مهم با ریسک بالا'
)
UNION
SELECT * FROM [dbo].[tblGhateeSazi%s]
WHERE [منبع مالیاتی]=N'مالیات بر ارزش افزوده' and [سال عملکرد]=%s
and [شناسه ملی / کد ملی (TIN)] IN
(SELECT [شناسه ملی / کد ملی (TIN)] FROM [dbo].[tblGhateeSazi%s] WHERE [سال عملکرد]=%s and [منبع مالیاتی] IN(N'مالیات بر درآمد شرکت ها',N'مالیات بر درآمد مشاغل')and [نوع ریسک اظهارنامه] IN (N'اظهارنامه برآوردی صفر',N'انتخاب شده بدون اعمال معیار ریسک',N'رتبه ریسک بالا',N'مودیان مهم با ریسک بالا'))
) as main
LEFT JOIN
[dbo].[tblTashkhisSaderShode%s]
ON 
[dbo].[tblTashkhisSaderShode%s].[شناسه اظهارنامه]=main.[شناسه اظهارنامه] and [tblTashkhisSaderShode%s].[سال عملکرد]=%s
LEFT JOIN
[dbo].[tblTashkhisEblaghShode%s]
ON
[dbo].[tblTashkhisEblaghShode%s].[شناسه اظهارنامه]=main.[شناسه اظهارنامه] and [tblTashkhisEblaghShode%s].[سال عملکرد]=%s
LEFT JOIN
[dbo].[tblGhateeSaderShode%s]
ON 
[dbo].[tblGhateeSaderShode%s].[شناسه اظهارنامه]=main.[شناسه اظهارنامه]and [tblGhateeSaderShode%s].[سال عملکرد]=%s
LEFT JOIN
[dbo].[tblGhateeEblaghShode%s]
ON
[dbo].[tblGhateeEblaghShode%s].[شناسه اظهارنامه]=main.[شناسه اظهارنامه]and [tblGhateeEblaghShode%s].[سال عملکرد]=%s
)as a
group by 

[کد اداره]
,[نام اداره]
,[سال عملکرد]
) AS hesabrasi
ON base.[کد اداره]=Hesabrasi.[کد اداره]
    """ % (year, get_update_date(), year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year)
    return sql_query


def insert_into_tblAnbare99Mashaghel(year):
    sql_query = """
    INSERT INTO AnbareMashaghel%s
SELECT 
%s as [تاریخ بروزرسانی]
,ezhar.*
, [تعداد تشخیص-اظهارنامه برآوردی صفر]
, [تعداد تشخیص-انتخاب شده بدون اعمال معیار ریسک]
, [تعداد تشخیص-رتبه ریسک بالا]
, [تعداد تشخیص-مودیان مهم با ریسک بالا]
FROM
(SELECT 
[کد اداره]
,[نام اداره]
,[سال عملکرد]
,ISNULL([اظهارنامه برآوردی صفر],0) AS [اظهارنامه برآوردی صفر]
,ISNULL([انتخاب شده بدون اعمال معیار ریسک],0) AS [انتخاب شده بدون اعمال معیار ریسک]
,ISNULL([رتبه ریسک بالا],0) AS [رتبه ریسک بالا]
,ISNULL([مودیان مهم با ریسک بالا],0) AS [مودیان مهم با ریسک بالا]
 FROM
(SELECT [کد اداره]
,[نام اداره]
,[سال عملکرد]
,[نوع ریسک اظهارنامه] 
,count(*)as tedad
FROM [dbo].[tblGhateeSazi%s]
WHERE 
[سال عملکرد]=%s
and [منبع مالیاتی]= N'مالیات بر درآمد مشاغل'
and [نوع ریسک اظهارنامه] IN (
N'اظهارنامه برآوردی صفر'
,
N'انتخاب شده بدون اعمال معیار ریسک'
,
N'رتبه ریسک بالا'
,
N'مودیان مهم با ریسک بالا'
)
GROUP BY [کد اداره]
,[نام اداره]
,[سال عملکرد]
,[نوع ریسک اظهارنامه] )
 src
pivot
(
  sum(tedad)
  for [نوع ریسک اظهارنامه] in ([اظهارنامه برآوردی صفر],[انتخاب شده بدون اعمال معیار ریسک],[رتبه ریسک بالا],[مودیان مهم با ریسک بالا])
)piv1)ezhar


LEFT JOIN



 (SELECT 
 [کد اداره]
,[نام اداره]
,ISNULL([اظهارنامه برآوردی صفر],0) AS [تعداد تشخیص-اظهارنامه برآوردی صفر]
,ISNULL([انتخاب شده بدون اعمال معیار ریسک],0) AS [تعداد تشخیص-انتخاب شده بدون اعمال معیار ریسک]
,ISNULL([رتبه ریسک بالا],0) AS [تعداد تشخیص-رتبه ریسک بالا]
,ISNULL([مودیان مهم با ریسک بالا],0) AS [تعداد تشخیص-مودیان مهم با ریسک بالا]
 FROM
 (SELECT 
ezhar.[کد اداره]
,ezhar.[نام اداره]
,ezhar.[نوع ریسک اظهارنامه]
,count([تاریخ صدور برگه تشخیص]) as [tedad]
FROM
(SELECT [کد اداره]
,[سال عملکرد]
,[نام اداره]
,[نوع ریسک اظهارنامه] 
,[شناسه اظهارنامه]
FROM [dbo].[tblGhateeSazi%s] 
WHERE 
[سال عملکرد]=%s
and [منبع مالیاتی]= N'مالیات بر درآمد شرکت ها'
and [نوع ریسک اظهارنامه] IN (
N'اظهارنامه برآوردی صفر'
,
N'انتخاب شده بدون اعمال معیار ریسک'
,
N'رتبه ریسک بالا'
,
N'مودیان مهم با ریسک بالا'
))as ezhar LEFT JOIN
[dbo].[tblTashkhisSaderShode%s] ON ezhar.[شناسه اظهارنامه]=[tblTashkhisSaderShode%s].[شناسه اظهارنامه] and [tblTashkhisSaderShode%s].[سال عملکرد]=%s
group by ezhar.[کد اداره]
,ezhar.[نام اداره]
,ezhar.[نوع ریسک اظهارنامه]
)
 src
pivot
(
  sum(tedad)
  for [نوع ریسک اظهارنامه] in ([اظهارنامه برآوردی صفر],[انتخاب شده بدون اعمال معیار ریسک],[رتبه ریسک بالا],[مودیان مهم با ریسک بالا])
) piv2)tashkhis
ON ezhar.[کد اداره]=tashkhis.[کد اداره]
    """ % (year, get_update_date(), year, year, year, year, year, year, year, year)

    return sql_query


def insert_into_tblAnbare99Sherkatha(year):
    sql_query = """
    
INSERT INTO AnbareSherkatha%s
SELECT 
%s as [تاریخ بروزرسانی]
,ezhar.*
, [تعداد تشخیص-اظهارنامه برآوردی صفر]
, [تعداد تشخیص-انتخاب شده بدون اعمال معیار ریسک]
, [تعداد تشخیص-رتبه ریسک بالا]
, [تعداد تشخیص-مودیان مهم با ریسک بالا]
FROM
(SELECT 
[کد اداره]
,[نام اداره]
,[سال عملکرد]
,ISNULL([اظهارنامه برآوردی صفر],0) AS [اظهارنامه برآوردی صفر]
,ISNULL([انتخاب شده بدون اعمال معیار ریسک],0) AS [انتخاب شده بدون اعمال معیار ریسک]
,ISNULL([رتبه ریسک بالا],0) AS [رتبه ریسک بالا]
,ISNULL([مودیان مهم با ریسک بالا],0) AS [مودیان مهم با ریسک بالا]
 FROM
(SELECT [کد اداره]
,[نام اداره]
,[سال عملکرد]
,[نوع ریسک اظهارنامه] 
,count(*)as tedad
FROM [dbo].[tblGhateeSazi%s]
WHERE 
[سال عملکرد]=%s
and [منبع مالیاتی]= N'مالیات بر درآمد شرکت ها'
and [نوع ریسک اظهارنامه] IN (
N'اظهارنامه برآوردی صفر'
,
N'انتخاب شده بدون اعمال معیار ریسک'
,
N'رتبه ریسک بالا'
,
N'مودیان مهم با ریسک بالا'
)
GROUP BY [کد اداره]
,[نام اداره]
,[سال عملکرد]
,[نوع ریسک اظهارنامه] )
 src
pivot
(
  sum(tedad)
  for [نوع ریسک اظهارنامه] in ([اظهارنامه برآوردی صفر],[انتخاب شده بدون اعمال معیار ریسک],[رتبه ریسک بالا],[مودیان مهم با ریسک بالا])
)piv1)ezhar


LEFT JOIN



 (SELECT 
 [کد اداره]
,[نام اداره]
,ISNULL([اظهارنامه برآوردی صفر],0) AS [تعداد تشخیص-اظهارنامه برآوردی صفر]
,ISNULL([انتخاب شده بدون اعمال معیار ریسک],0) AS [تعداد تشخیص-انتخاب شده بدون اعمال معیار ریسک]
,ISNULL([رتبه ریسک بالا],0) AS [تعداد تشخیص-رتبه ریسک بالا]
,ISNULL([مودیان مهم با ریسک بالا],0) AS [تعداد تشخیص-مودیان مهم با ریسک بالا]
 FROM
 (SELECT 
ezhar.[کد اداره]
,ezhar.[نام اداره]
,ezhar.[نوع ریسک اظهارنامه]
,count([تاریخ صدور برگه تشخیص]) as [tedad]
FROM
(SELECT [کد اداره]
,[نام اداره]
,[نوع ریسک اظهارنامه] 
,[شناسه اظهارنامه]
FROM [dbo].[tblGhateeSazi%s] 
WHERE 
[سال عملکرد]=%s
and [منبع مالیاتی]= N'مالیات بر درآمد شرکت ها'
and [نوع ریسک اظهارنامه] IN (
N'اظهارنامه برآوردی صفر'
,
N'انتخاب شده بدون اعمال معیار ریسک'
,
N'رتبه ریسک بالا'
,
N'مودیان مهم با ریسک بالا'
))as ezhar LEFT JOIN
[dbo].[tblTashkhisSaderShode%s] ON ezhar.[شناسه اظهارنامه]=[tblTashkhisSaderShode%s].[شناسه اظهارنامه] and [tblTashkhisSaderShode%s].[سال عملکرد]=%s
group by ezhar.[کد اداره]
,ezhar.[نام اداره]
,ezhar.[نوع ریسک اظهارنامه]
)
 src
pivot
(
  sum(tedad)
  for [نوع ریسک اظهارنامه] in ([اظهارنامه برآوردی صفر],[انتخاب شده بدون اعمال معیار ریسک],[رتبه ریسک بالا],[مودیان مهم با ریسک بالا])
) piv2)tashkhis
ON ezhar.[کد اداره]=tashkhis.[کد اداره]
    """ % (year, get_update_date(), year, year, year, year, year, year, year, year)

    return sql_query


def insert_into_tblHesabrasiArzeshAfzoode(year):
    sql_query = """
    
INSERT INTO tblHesabrasiArzeshAfzode%s
SELECT
      %s AS  [تاریخ بروزرسانی]
      ,[کد اداره]
      ,[نام اداره]
      ,[سال عملکرد]
	  ,COUNT([شناسه اظهارنامه]) AS [تعداد اظهارنامه]
	  ,count([تاریخ صدور برگه تشخیص]) AS  [tashkhisSadere]
      ,count([تاریخ ابلاغ تشخیص]) AS  [eblaghTashkhis]
      ,count([تاریخ برگ قطعی]) AS [ghateeSadere]
      ,count([تاریخ ابلاغ برگ قطعی]) AS [eblaghGhatee]

 FROM

(SELECT main.*
,[tblTashkhisSaderShode%s].[تاریخ صدور برگه تشخیص]
,[dbo].[tblTashkhisEblaghShode%s].[تاریخ ابلاغ تشخیص] as [تاریخ ابلاغ تشخیص]
,[dbo].[tblGhateeSaderShode%s].[تاریخ برگ قطعی صادر شده] as [تاریخ برگ قطعی]
,[dbo].[tblGhateeEblaghShode%s].[تاریخ ابلاغ برگ قطعی]
 FROM
(SELECT [کد اداره]
      ,[نام اداره]
      ,[سال عملکرد]
      ,[شناسه اظهارنامه]

  FROM [TestDb].[dbo].[tblGhateeSazi%s]
  where  [منبع مالیاتی]=N'مالیات بر ارزش افزوده'
  ) AS main
  LEFT JOIN
[dbo].[tblTashkhisSaderShode%s]
ON 
[dbo].[tblTashkhisSaderShode%s].[شناسه اظهارنامه]=main.[شناسه اظهارنامه] and [tblTashkhisSaderShode%s].[سال عملکرد]=main.[سال عملکرد]
LEFT JOIN
[dbo].[tblTashkhisEblaghShode%s]
ON
[dbo].[tblTashkhisEblaghShode%s].[شناسه اظهارنامه]=main.[شناسه اظهارنامه] and [tblTashkhisEblaghShode%s].[سال عملکرد]=main.[سال عملکرد]
LEFT JOIN
[dbo].[tblGhateeSaderShode%s]
ON 
[dbo].[tblGhateeSaderShode%s].[شناسه اظهارنامه]=main.[شناسه اظهارنامه] and [tblGhateeSaderShode%s].[سال عملکرد]=main.[سال عملکرد]
LEFT JOIN
[dbo].[tblGhateeEblaghShode%s]
ON
[dbo].[tblGhateeEblaghShode%s].[شناسه اظهارنامه]=main.[شناسه اظهارنامه] and [tblGhateeEblaghShode%s].[سال عملکرد]=main.[سال عملکرد]
)as a
 GROUP BY 
[کد اداره]
      ,[نام اداره]
      ,[سال عملکرد]
    """ % (year, get_update_date(), year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year)

    return sql_query


def linked_server():

    return """

if not exists(select * from sys.servers where name = N'10.52.0.114')
BEGIN
EXEC sp_addlinkedserver @server='10.52.0.114'

EXEC sp_addlinkedsrvlogin '10.52.0.114', 'false', NULL, 'sa', '14579Ali'
END

"""


def get_badvi_tables():

    return """

SELECT table_name FROM [10.52.0.114].testdb.INFORMATION_SCHEMA.TABLES
where table_name like 'tblbadvi%'

"""


def get_sql_mashaghelsonati():

    return """
select 
case
when  ghabln_inf.cod_hozeh  =168141 then 'هويزه'
 when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1601 then 'اهواز کد يک'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1602 then 'اهواز کد دو'
 when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,5) =16439 then 'هنديجان'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,5) =16649 then 'لالي'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,5) =16718 then 'رامشير'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1603 then 'اهواز کد سه'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1604 then 'اهواز کد چهار '
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1605 then 'اهواز کد پنج'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1606 then 'اهواز کد شش'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1607 then 'اهواز کد هفت'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1608 then 'اهواز کد هشت'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1609 then 'اهواز کد نه'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1610 then 'اهواز کد 10'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1611 then 'اهواز کد 11'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1615 then 'اهواز کد 15'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1631 then 'آبادان کد 31'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1632 then 'آبادان کد 32'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1633 then 'آبادان کد 33'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1626 then 'دزفول'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1627 then 'دزفول'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1628 then 'دزفول'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1643 then 'ماهشهر کد43'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1644 then 'ماهشهر کد44'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1636 then 'بهبهان'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1639 then 'شوشتر'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1641 then 'گتوند'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1648 then 'بندر امام'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1649 then 'بندر امام'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1651 then 'انديمشک'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1654 then 'خرمشهر'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1659 then 'شادگان'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1661 then 'اميديه'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1663 then 'آغاجاري'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1664 then 'مسجد سليمان'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1668 then 'شوش'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1671 then 'رامهرمز'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1676 then 'ايذه'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1678 then 'هفتگل'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1679 then 'باغملک'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1681 then 'دشت آزاداگان'
else 'نامشخص' end as 'شهرستان'
,
case 
 when ghabln_inf.cod_hozeh  IN (168141) then '168141'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,5) IN ('16439','16649','16718') then SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,5) else SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) end as 'کد اداره'
,
namee as 'نام',
family as 'نام خانوادگي',
ghabln_inf.Sal as 'عملکرد',
ghabln_inf.cod_hozeh as 'کد حوزه',
ghabln_inf.k_parvand as 'کلاسه پرونده',
tashkhis_inf.motamam as 'متمم',
case when KMLink_Inf.have_ezhar=1 then 'داراي اظهارنامه' else 'فاقد اظهارنامه' end as 'وضعيت ارائه اظهارنامه',
Shohr_kasb as 'شهرت کسبي',
tabl_inf.S_des as 'شرح فعاليت',
modi_inf.modi_seq as 'شماره مودي',
modi_inf.cod_meli  'کد ملي',
tashkhis_inf.dar_maliat_mash as 'درآمد ماليات مشاغل',
tashkhis_inf.mafiat101 as 'ميزان معافيت 101',
tashkhis_inf.moaf_sayer as 'ساير معافيت',
tashkhis_inf.asl_maliat as 'ماليات تشخيص',
tashkhis_inf.ghanony_maliat as 'ماليات قانوني',
tashkhis_inf.pardakht_mab as 'مبلغ پرداختي',
tashkhis_inf.mandeh_pardakht as 'مانده پرداختي',
tashkhis_inf.sabt_no as 'شماره ثبت برگ تشخيص',
tashkhis_inf.sabt_date as 'تاريخ ثبت برگ تشخيص',
tashkhis_inf.eblag_date as 'تاريخ ابلاغ برگ تشخيص',

case
when nahve_eblag=1 then 'به مودي' 
when nahve_eblag=2 then 'به بستگان' 
when nahve_eblag=3 then 'به مستخدم' 
when nahve_eblag=4 then 'قانوني' 
when nahve_eblag=5 then 'روزنامه اي' 
when nahve_eblag=6 then 'پست' 
when nahve_eblag=7 then 'غيره' else 'فاقد اطلاعات نحوه ابلاغ'
end as 'نحوه ابلاغ',
tashkhis_inf.Eblagh_Sabt_No as 'شماره ثبت ابلاغ برگ تشخيص',
tashkhis_inf.Eblagh_Sabt_Date as 'تاريخ ثبت ابلاغ برگ تشخيص' ,
 case when tashkhis_inf.aks_modi =1 then 'تمکين' 
 when tashkhis_inf.aks_modi =2 then 'اعتراض' else 'فاقد عکس العمل' end as 'عکس العمل مودي به برگ تشخيص',
 tashkhis_inf.aks_sabt_no as 'شماره ثبت عکس العمل برگ تشخيص',
 tashkhis_inf.aks_sabt_date as 'تاريخ ثبت عکس العمل برگ تشخيص' ,
 tashkhis_inf.Eblagh_Namek as 'ابلاغ کننده',
 tashkhis_inf.Eblagh_NameG as 'گيرنده برگ تشخيص'
 ,
 case when KMLink_Inf.have_ezhar=1
 and exists(Select Rahgiri_No  from Ezhar_Inf ee where ee.Cod_Hozeh=KMLink_Inf.Cod_Hozeh and ee.K_Parvand=KMLink_Inf.K_Parvand and ee.Sal=KMLink_Inf.sal and len(ee.Sabt_Date)>2--and LEN(Rahgiri_No)>2
 ) then 'اظهارنامه به مودي الصاق شده' 
 when (KMLink_Inf.have_ezhar !=1 OR KMLink_Inf.have_ezhar ='' or KMLink_Inf.have_ezhar IS null) 
 and exists(Select Rahgiri_No  from Ezhar_Inf ee where ee.Cod_Hozeh=KMLink_Inf.Cod_Hozeh and ee.K_Parvand=KMLink_Inf.K_Parvand and ee.Sal=KMLink_Inf.sal and len(ee.Sabt_Date)>2--and LEN(Rahgiri_No)>2
 )then 'پرونده داراي اظهارنامه' 
 
   else 'فاقد اظهارنامه' end as 'وضعيت اظهارنامه'
   
from ghabln_inf 
inner join 
KMLink_Inf on
ghabln_inf.Sal=KMLink_Inf.sal and ghabln_inf.cod_hozeh=KMLink_Inf.Cod_Hozeh and ghabln_inf.k_parvand=KMLink_Inf.K_Parvand
inner join modi_inf on
modi_inf.modi_seq=KMLink_Inf.Modi_Seq
inner join tashkhis_inf on
tashkhis_inf.sal=KMLink_Inf.sal and tashkhis_inf.cod_hozeh=KMLink_Inf.Cod_Hozeh and tashkhis_inf.k_parvand=KMLink_Inf.K_Parvand and tashkhis_inf.modi_seq=KMLink_Inf.Modi_Seq
left join [tabl_inf] on
ghabln_inf.Faliat_sharh=tabl_inf.S_code and G_code=1

where 

LEN(modi_inf.modi_seq)>8
and tashkhis_inf.serial=(select max(tt.serial)from tashkhis_inf tt where tashkhis_inf.sal=tt.sal and tashkhis_inf.cod_hozeh=tt.cod_hozeh and tashkhis_inf.k_parvand=tt.k_parvand and tashkhis_inf.modi_seq=tt.modi_seq)
and ghabln_inf.Sal in (1390,1391,1392,1393,1394,1395)

and LEN(sabt_date)>2
and exists (select * from GoResd_Inf tt where tashkhis_inf.sal=tt.sal and tashkhis_inf.cod_hozeh=tt.cod_hozeh and tashkhis_inf.k_parvand=tt.k_parvand and KMLink_Inf.Goresd_seq=tt.Goresd_seq and tt.Mab_Tash=5)

"""


def get_sql_mashaghelsonati_ghatee():

    return """
select 
case
when  ghabln_inf.cod_hozeh  =168141 then 'هويزه'
 when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1601 then 'اهواز کد يک'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1602 then 'اهواز کد دو'
 when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,5) =16439 then 'هنديجان'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,5) =16649 then 'لالي'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,5) =16718 then 'رامشير'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1603 then 'اهواز کد سه'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1604 then 'اهواز چهار '
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1605 then 'اهواز کد پنج'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1607 then 'اهواز کد هفت'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1608 then 'اهواز کد هشت'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1610 then 'اهواز'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1611 then 'اهواز'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1631 then 'آبادان کد 31'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1632 then 'آبادان کد 32'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1633 then 'آبادان کد 33'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1626 then 'دزفول'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1627 then 'دزفول'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1628 then 'دزفول'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1643 then 'ماهشهر کد43'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1644 then 'ماهشهر کد44'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1636 then 'بهبهان'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1639 then 'شوشتر'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1641 then 'گتوند'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1648 then 'بندر امام'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1649 then 'بندر امام'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1651 then 'انديمشک'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1654 then 'خرمشهر'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1659 then 'شادگان'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1661 then 'اميديه'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1663 then 'آغاجاري'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1664 then 'مسجد سليمان'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1668 then 'شوش'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1671 then 'رامهرمز'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1676 then 'ايذه'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1678 then 'هفتگل'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1679 then 'باغملک'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) =1681 then 'دشت آزاداگان'
else 'نامشخص' end as 'شهرستان'
,
case 
 when ghabln_inf.cod_hozeh  IN (168141) then '168141'
when SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,5) IN ('16439','16649','16718') then SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,5) else SUBSTRING( cast (ghabln_inf.cod_hozeh as varchar(20) ),1,4) end as 'کد اداره'
,
namee as 'نام',
family as 'نام خانوادگی',
ghabln_inf.Sal as 'عملکرد',
ghabln_inf.cod_hozeh as 'کد حوزه',
ghabln_inf.k_parvand as 'کلاسه پرونده',
ghatee_inf.motamam as 'متمم',
case when KMLink_Inf.have_ezhar=1 then 'دارای اظهارنامه' else 'فاقد اظهارنامه' end as 'وضعیت ارائه اظهارنامه',
Shohr_kasb as 'شهرت کسبی',
tabl_inf.S_des as 'شرح فعالیت',
modi_inf.modi_seq as 'شماره مودی',
ghatee_inf.dar_maliat_mash as 'درآمد مالیات مشاغل',
ghatee_inf.mafiat101 as 'میزان معافیت 101',
ghatee_inf.mandeh_pardakht as 'مانده پرداخت',
ghatee_inf.asl_maliat as 'مالیات قطعی',
ghatee_inf.pardakht_mab as 'مبلغ پرداختی',
ghatee_inf.mandeh_pardakht as 'مانده پرداختی',
ghatee_inf.sabt_no as 'شماره ثبت برگ قطعی',
ghatee_inf.sabt_date as 'تاریخ ثبت برگ قطعی',
ghatee_inf.eblag_date as 'تاریخ ابلاغ برگ قطعی',
modi_inf.cod_meli as 'کدملی',
case
when nahve_eblag=1 then 'به مودی' 
when nahve_eblag=2 then 'به بستگان' 
when nahve_eblag=3 then 'به مستخدم' 
when nahve_eblag=4 then 'قانونی' 
when nahve_eblag=5 then 'روزنامه ای' 
when nahve_eblag=6 then 'پست' 
when nahve_eblag=7 then 'غیره' else 'فاقد اطلاعات نحوه ابلاغ'
end as 'نحوه ابلاغ',
ghatee_inf.Eblagh_Sabt_No as 'شماره ثبت ابلاغ برگ قطعی',
ghatee_inf.Eblagh_Sabt_Date as 'تاریخ ثبت ابلاغ برگ قطعی' ,
 case when ghatee_inf.aks_modi =1 then 'تمکین' 
 when ghatee_inf.aks_modi =2 then 'اعتراض' else 'فاقد عکس العمل' end as 'عکس العمل مودی به برگ قطعی',
 ghatee_inf.aks_sabt_no as 'شماره ثبت عکس العمل برگ قطعی',
 ghatee_inf.aks_sabt_date as 'تاریخ ثبت عکس العمل برگ قطعی' ,
 ghatee_inf.Eblagh_Namek as 'ابلاغ کننده',
 ghatee_inf.Eblagh_NameG as 'گیرنده برگ قطعی',
  ghatee_inf.jarimeh_mab as 'مبلغ جریمه برگ قطعی'

from ghabln_inf 
inner join 
KMLink_Inf on
ghabln_inf.Sal=KMLink_Inf.sal and ghabln_inf.cod_hozeh=KMLink_Inf.Cod_Hozeh and ghabln_inf.k_parvand=KMLink_Inf.K_Parvand
inner join modi_inf on
modi_inf.modi_seq=KMLink_Inf.Modi_Seq
inner join ghatee_inf on
ghatee_inf.sal=KMLink_Inf.sal and ghatee_inf.cod_hozeh=KMLink_Inf.Cod_Hozeh and ghatee_inf.k_parvand=KMLink_Inf.K_Parvand and ghatee_inf.modi_seq=KMLink_Inf.Modi_Seq
left join [tabl_inf] on
ghabln_inf.Faliat_sharh=tabl_inf.S_code and G_code=1

where 

LEN(modi_inf.modi_seq)>8
and ghatee_inf.serial=(select max(tt.serial)from ghatee_inf tt where ghatee_inf.sal=tt.sal and ghatee_inf.cod_hozeh=tt.cod_hozeh and ghatee_inf.k_parvand=tt.k_parvand and ghatee_inf.motamam=tt.motamam)


and LEN(sabt_date)>2

"""


def get_sql_mashaghelsonati_amadeersalbeheiat(date):
    return """
            DECLARE @tazaman int
            SET @tazaman = %s
            select 
            case
            when  mm.cod_hozeh  =168141 then 'هويزه'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1601 then 'اهواز کد يک'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1602 then 'اهواز کد دو'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,5) =16439 then 'هنديجان'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,5) =16649 then 'لالي'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,5) =16718 then 'رامشير'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1603 then 'اهواز کد سه'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1604 then 'اهواز کد چهار '
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1605 then 'اهواز کد پنج'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1606 then 'اهواز کد شش'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1607 then 'اهواز کد هفت'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1608 then 'اهواز کد هشت'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1609 then 'اهواز کد نه'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1610 then 'اهواز کد 10'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1611 then 'اهواز کد 11'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1615 then 'اهواز کد 15'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1631 then 'آبادان کد 31'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1632 then 'آبادان کد 32'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1633 then 'آبادان کد 33'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1626 then 'دزفول'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1627 then 'دزفول'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1628 then 'دزفول'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1643 then 'ماهشهر کد43'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1644 then 'ماهشهر کد44'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1636 then 'بهبهان'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1639 then 'شوشتر'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1641 then 'گتوند'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1648 then 'بندر امام'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1649 then 'بندر امام'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1651 then 'انديمشک'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1654 then 'خرمشهر'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1659 then 'شادگان'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1661 then 'اميديه'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1663 then 'آغاجاري'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1664 then 'مسجد سليمان'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1668 then 'شوش'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1671 then 'رامهرمز'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1676 then 'ايذه'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1678 then 'هفتگل'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1679 then 'باغملک'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1681 then 'دشت آزاداگان'
            else 'نامشخص' end as 'شهرستان'
            ,
            case
            when mm.cod_hozeh  IN (168141) then '168141'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,5) IN ('16439','16649','16718') then SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,5) else SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) end as 'کد اداره'
            ,
            mm.Cod_Hozeh as 'کد حوزه',
            mm.sal as 'عملکرد',
            mm.K_Parvand as 'کلاسه پرونده',
            TAa.motamam AS 'متمم',
            modi_inf.namee AS 'نام',
            modi_inf.family AS 'نام خانوادگي',
            taa.asl_maliat as 'ماليات تشخيص' ,
            taa.dar_maliat_mash as 'درآمد تشخيص',
            case
            when taa.nahve_eblag=1 then 'به مودي' 
            when taa.nahve_eblag=2 then 'به بستگان' 
            when taa.nahve_eblag=3 then 'به مستخدم' 
            when taa.nahve_eblag=4 then 'قانوني' 
            when taa.nahve_eblag=5 then 'روزنامه اي' 
            when taa.nahve_eblag=6 then 'پست' 
            when taa.nahve_eblag=7 then 'غيره' else 'فاقد اطلاعات نحوه ابلاغ'
            end as 'نحوه ابلاغ',
            taa.sabt_date as 'تاريخ ثبت برگ تشخيص',
            taa.aks_sabt_date as 'تاريخ ثبت عکس العمل',
            case when( aks_modi =1) then 'تمکين'   when( aks_modi =2) then 'اعتراض' end  AS 'عکس العمل مودي به برگ تشخيص',

            case 
            when exists (select cod_hozeh from tavafogh_mcol ta where ta.cod_hozeh=hh.cod_hozeh and ta.sal=hh.Sal and ta.k_parvand=hh.k_parvand and TA.modi_seq=taa.modi_seq and len(ta.sabt_date)>2  and nazar_mcol=4 and TA.motamam=taa.motamam)then 'عدم توافق با مميز کل'
            when  exists (select cod_hozeh from tashkhis_inf ta where ta.cod_hozeh=hh.cod_hozeh and ta.sal=hh.Sal and ta.k_parvand=hh.k_parvand and TA.modi_seq=taa.modi_seq and len(ta.sabt_date)>2  and nahve_eblag in (4 ,5)and TA.motamam=taa.motamam) then ' ابلاغ روزنامه اي و قانوني برگ تشخيص'
            when 
            ( exists (select cod_hozeh from tashkhis_inf ta where ta.cod_hozeh=hh.cod_hozeh 
            --==========================----------------==========================-----------------==========================--------------
            and cast(aks_sabt_date as float)<@tazaman
            --========================------------------- --==========================----------------- --=======================================
            and ta.sal=hh.Sal and ta.k_parvand=hh.k_parvand and TA.modi_seq=taa.modi_seq and len(ta.sabt_date)>2  and aks_modi=2 and TA.motamam=taa.motamam)
            and
            not exists (select cod_hozeh from tavafogh_mcol ta where ta.cod_hozeh=hh.cod_hozeh and ta.sal=hh.Sal and ta.k_parvand=hh.k_parvand and TA.modi_seq=taa.modi_seq and len(ta.sabt_date)>2  
            and TA.motamam=taa.motamam)
            ) then 'اعتراض مودي و عدم ادامه مراحل' end as  'دليل ارسال به هيات'
            
            --hh.sal as 'عملکرد' ,hh.cod_hozeh as 'کد حوزه' , hh.k_parvand as 'کلاسه پرونده' , ta.motamam as 'متمم', namee as 'نام' , family as 'نام خانوادگي'
            from ghabln_inf hh inner join KMLink_Inf mm on hh.Sal=mm.sal and hh.cod_hozeh=mm.Cod_Hozeh and hh.k_parvand=mm.K_Parvand
            inner join modi_inf on modi_inf.modi_seq=mm.Modi_Seq
            inner join tashkhis_inf taa on taa.sal=mm.sal and taa.cod_hozeh=mm.Cod_Hozeh and taa.k_parvand =mm.K_Parvand and taa.modi_seq=mm.Modi_Seq
            where
            (CONNECTIONPROPERTY('local_net_address' )!= '10.53.32.130' or (CONNECTIONPROPERTY('local_net_address' )= '10.53.32.130' and hh.cod_hozeh !=168141))
            and
            (CONNECTIONPROPERTY('local_net_address' )!= '10.53.48.130' or (CONNECTIONPROPERTY('local_net_address' )= '10.53.48.130' and hh.cod_hozeh =168141))
            and
            LEN(taa.sabt_date)>2 and LEN(taa.eblag_date)>2

            --and  Vaziat_Falie not in(2)
            and hh.sal>=1389

            and
            not exists (select cod_hozeh from adam_faliat_inf ta where ta.cod_hozeh=hh.cod_hozeh and ta.sal=hh.Sal and ta.k_parvand=hh.k_parvand and len(ta.sabt_no)>1  and isnull(ebtal, 0) = 0 )
            AND
            not exists (select cod_hozeh from ghatee_inf ta where ta.cod_hozeh=hh.cod_hozeh and ta.sal=hh.Sal and ta.k_parvand=hh.k_parvand and TA.modi_seq=taa.modi_seq and TA.motamam=taa.motamam)
            AND
            not exists (select cod_hozeh from Badvi_inf ta where ta.cod_hozeh=hh.cod_hozeh and ta.sal=hh.Sal and ta.k_parvand=hh.k_parvand and TA.modi_seq=taa.modi_seq and LEN([davat_date])>3 and TA.motamam=taa.motamam)
            AND
            (
            exists (select cod_hozeh from tavafogh_mcol ta where ta.cod_hozeh=hh.cod_hozeh and ta.sal=hh.Sal and ta.k_parvand=hh.k_parvand and TA.modi_seq=taa.modi_seq and len(ta.sabt_date)>2  and nazar_mcol=4 and TA.motamam=taa.motamam)
            or
            exists (select cod_hozeh from tashkhis_inf ta where ta.cod_hozeh=hh.cod_hozeh and ta.sal=hh.Sal and ta.k_parvand=hh.k_parvand and TA.modi_seq=taa.modi_seq and len(ta.sabt_date)>2  and nahve_eblag in (4 ,5)and TA.motamam=taa.motamam)
            or
            ( exists (select cod_hozeh from tashkhis_inf ta where ta.cod_hozeh=hh.cod_hozeh and ta.sal=hh.Sal and ta.k_parvand=hh.k_parvand and TA.modi_seq=taa.modi_seq and len(ta.sabt_date)>2 
            --==========================----------------==========================-----------------==========================--------------
            and cast(aks_sabt_date as float)<@tazaman
            --========================------------------- --==========================----------------- --=======================================

            and aks_modi=2 and TA.motamam=taa.motamam)
            and
            not exists (select cod_hozeh from tavafogh_mcol ta where ta.cod_hozeh=hh.cod_hozeh and ta.sal=hh.Sal and ta.k_parvand=hh.k_parvand and TA.modi_seq=taa.modi_seq and len(ta.sabt_date)>2   and TA.motamam=taa.motamam)
            )
            )
            and taa.serial=(select max(serial)from tashkhis_inf where taa.cod_hozeh=cod_hozeh and taa.k_parvand=k_parvand and taa.sal=sal and taa.motamam=motamam and taa.modi_seq=modi_seq)
""" % date


def get_sql_mashaghelsonati_tashkhisEblaghNashode():
    return """
            select 
            case
            when  mm.cod_hozeh  =168141 then 'هويزه'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1601 then 'اهواز کد يک'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1602 then 'اهواز کد دو'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,5) =16439 then 'هنديجان'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,5) =16649 then 'لالي'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,5) =16718 then 'رامشير'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1603 then 'اهواز کد سه'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1604 then 'اهواز کد چهار '
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1605 then 'اهواز کد پنج'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1606 then 'اهواز کد شش'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1607 then 'اهواز کد هفت'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1608 then 'اهواز کد هشت'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1609 then 'اهواز کد نه'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1610 then 'اهواز کد 10'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1611 then 'اهواز کد 11'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1615 then 'اهواز کد 15'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1631 then 'آبادان کد 31'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1632 then 'آبادان کد 32'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1633 then 'آبادان کد 33'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1626 then 'دزفول'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1627 then 'دزفول'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1628 then 'دزفول'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1643 then 'ماهشهر کد43'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1644 then 'ماهشهر کد44'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1636 then 'بهبهان'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1639 then 'شوشتر'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1641 then 'گتوند'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1648 then 'بندر امام'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1649 then 'بندر امام'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1651 then 'انديمشک'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1654 then 'خرمشهر'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1659 then 'شادگان'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1661 then 'اميديه'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1663 then 'آغاجاري'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1664 then 'مسجد سليمان'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1668 then 'شوش'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1671 then 'رامهرمز'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1676 then 'ايذه'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1678 then 'هفتگل'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1679 then 'باغملک'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1681 then 'دشت آزاداگان'
            else 'نامشخص' end as 'شهرستان'
            ,
            case 
            when mm.cod_hozeh  IN (168141) then '168141'
            when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,5) IN ('16439','16649','16718') then SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,5) else SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) end as 'کد اداره'
            ,
            mm.Cod_Hozeh as 'کد حوزه',
            mm.sal as 'عملکرد',
            mm.K_Parvand as 'کلاسه پرونده',
            TA.motamam AS 'متمم',
            modi_inf.namee AS 'نام',
            modi_inf.family AS 'نام خانوادگي',
            ta.asl_maliat as 'ماليات تشخيص' ,
            ta.dar_maliat_mash as 'درآمد تشخيص',
            ta.sabt_date as 'تاريخ ثبت برگ تشخيص'
            
            --hh.sal as 'عملکرد' ,hh.cod_hozeh as 'کد حوزه' , hh.k_parvand as 'کلاسه پرونده' , ta.motamam as 'متمم', namee as 'نام' , family as 'نام خانوادگي'
            from ghabln_inf hh inner join KMLink_Inf mm on hh.Sal=mm.sal and hh.cod_hozeh=mm.Cod_Hozeh and hh.k_parvand=mm.K_Parvand
            inner join modi_inf on modi_inf.modi_seq=mm.Modi_Seq
            inner join tashkhis_inf ta on ta.sal=mm.sal and ta.cod_hozeh=mm.Cod_Hozeh and ta.k_parvand =mm.K_Parvand and ta.modi_seq=mm.Modi_Seq
            where
            (CONNECTIONPROPERTY('local_net_address' )!= '10.53.32.130' or (CONNECTIONPROPERTY('local_net_address' )= '10.53.32.130' and hh.cod_hozeh !=168141))
            and
            (CONNECTIONPROPERTY('local_net_address' )!= '10.53.48.130' or (CONNECTIONPROPERTY('local_net_address' )= '10.53.48.130' and hh.cod_hozeh =168141))
            and
            LEN(ta.sabt_date)>2 and (len (Eblagh_Sabt_Date) <2  or Eblagh_Sabt_Date is null  or Eblagh_Sabt_Date ='')
            --(LEN(ta.eblag_date)<2 or (ta.eblag_date is null) )
            and  Vaziat_Falie not in(2) and
            not exists (select cod_hozeh from adam_faliat_inf ta where ta.cod_hozeh=hh.cod_hozeh and ta.sal=hh.Sal and ta.k_parvand=hh.k_parvand and len(ta.sabt_no)>1  and isnull(ebtal, 0) = 0 )
            and
            not exists (select cod_hozeh from tashkhis_inf taaa where taaa.cod_hozeh=hh.cod_hozeh and taaa.sal=hh.Sal and taaa.k_parvand=hh.k_parvand and len(taaa.sabt_date)>1  and taaa.modi_seq=mm.modi_seq  and ta.motamam=taaa.motamam and len(taaa.eblag_date)>2)
            and ta.serial=(select max(serial)from tashkhis_inf where ta.cod_hozeh=cod_hozeh and ta.k_parvand=k_parvand and ta.sal=sal and ta.motamam=motamam and ta.modi_seq=modi_seq)
"""


def get_sql_mashaghelsonati_ghateeEblaghNashode():

    return """
           select 
case
when  mm.cod_hozeh  =168141 then 'هويزه'
 when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1601 then 'اهواز کد يک'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1602 then 'اهواز کد دو'
 when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,5) =16439 then 'هنديجان'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,5) =16649 then 'لالي'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,5) =16718 then 'رامشير'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1603 then 'اهواز کد سه'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1604 then 'اهواز کد چهار '
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1605 then 'اهواز کد پنج'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1606 then 'اهواز کد شش'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1607 then 'اهواز کد هفت'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1608 then 'اهواز کد هشت'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1609 then 'اهواز کد نه'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1610 then 'اهواز کد 10'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1611 then 'اهواز کد 11'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1615 then 'اهواز کد 15'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1631 then 'آبادان کد 31'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1632 then 'آبادان کد 32'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1633 then 'آبادان کد 33'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1626 then 'دزفول'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1627 then 'دزفول'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1628 then 'دزفول'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1643 then 'ماهشهر کد43'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1644 then 'ماهشهر کد44'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1636 then 'بهبهان'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1639 then 'شوشتر'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1641 then 'گتوند'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1648 then 'بندر امام'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1649 then 'بندر امام'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1651 then 'انديمشک'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1654 then 'خرمشهر'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1659 then 'شادگان'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1661 then 'اميديه'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1663 then 'آغاجاري'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1664 then 'مسجد سليمان'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1668 then 'شوش'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1671 then 'رامهرمز'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1676 then 'ايذه'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1678 then 'هفتگل'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1679 then 'باغملک'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) =1681 then 'دشت آزاداگان'
else 'نامشخص' end as 'شهرستان'
,
case 
when mm.cod_hozeh IN (168141) then '168141'
when SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,5) IN ('16439','16649','16718') then SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,5) else SUBSTRING( cast (mm.cod_hozeh as varchar(20) ),1,4) end as 'کد اداره'
,
mm.Cod_Hozeh as 'کد حوزه',
mm.sal as 'عملکرد',
mm.K_Parvand as 'کلاسه پرونده',
TA.motamam AS 'متمم',
modi_inf.namee AS 'نام',
modi_inf.family AS 'نام خانوادگي',
ta.asl_maliat as 'ماليات قطعي' ,
ta.dar_maliat_mash as 'درآمد قطعي',
ta.sabt_date as 'تاريخ ثبت برگ قطعي'
 
 from ghabln_inf hh inner join KMLink_Inf mm on hh.Sal=mm.sal and hh.cod_hozeh=mm.Cod_Hozeh and hh.k_parvand=mm.K_Parvand
inner join modi_inf on modi_inf.modi_seq=mm.Modi_Seq
inner join ghatee_inf ta on ta.sal=mm.sal and ta.cod_hozeh=mm.Cod_Hozeh and ta.k_parvand =mm.K_Parvand and ta.modi_seq=mm.Modi_Seq
where
 (CONNECTIONPROPERTY('local_net_address' )!= '10.53.32.130' or (CONNECTIONPROPERTY('local_net_address' )= '10.53.32.130' and hh.cod_hozeh !=168141))
and
 (CONNECTIONPROPERTY('local_net_address' )!= '10.53.48.130' or (CONNECTIONPROPERTY('local_net_address' )= '10.53.48.130' and hh.cod_hozeh =168141))
and
LEN(ta.sabt_date)>2 and 
 (len (Eblagh_Sabt_Date) <2  or Eblagh_Sabt_Date is null  or Eblagh_Sabt_Date ='')
and  Vaziat_Falie not in(2) and
not exists (select cod_hozeh from adam_faliat_inf ta where ta.cod_hozeh=hh.cod_hozeh and ta.sal=hh.Sal and ta.k_parvand=hh.k_parvand and len(ta.sabt_no)>1  and isnull(ebtal, 0) = 0 )
and
not exists (select cod_hozeh from ghatee_inf taaa where taaa.cod_hozeh=hh.cod_hozeh and taaa.sal=hh.Sal and taaa.k_parvand=hh.k_parvand and len(taaa.sabt_date)>1  and taaa.modi_seq=mm.modi_seq  and ta.motamam=taaa.motamam and len(taaa.Eblagh_Sabt_Date)>2)
and ta.serial=(select max(serial)from ghatee_inf where ta.cod_hozeh=cod_hozeh and ta.k_parvand=k_parvand and ta.sal=sal and ta.motamam=motamam and ta.modi_seq=modi_seq)

"""


def get_sql_alleterazat():
    return """

SELECT
    cr01_internal_id,
    current_office,
    ca02_tax_year,
    ca02_return_id,
    ca02_return_version,
    ca09_tax_type_code,
    cstd_return_type,
    co01_request_no,
    cstd_request_status,
    cstd_request_type,
    co01_request_ref_num,
    cstd_request_ref_type,
    co01_request_ref_date,
    co01_pre_notice_date,
    cstd_withdraw_status,
    co01_withdrawal_to,
    co01_withdraw_received_on,
    co01_request_received_on,
    max_co03_id,
    co03_hearing_date,
    cstd_hearing_status,
    co03_outcome,
    rulling_date,
    rulling_approved,
    closed_date,
    assign_to_name,
    tp_agree,
    inta_attendee_name,
    inta_attendee_type,
    co03_inta_attendee,
    co01_previous_request_no,
    previous_request_type,
    ta_agree,
    agree,
    gharar,
    co03_decision_deadline,
    tadil,
    raf_taroz,
    taid,
    rulling_performer_name,
    co03_decision_assignee1,
    co03_decision_assignee1_name,
    cstd_letter_type_rrn,
    article_169,
    max_co01_request_no,
    cs10_id_assign_to_name,
    cs10_id_inta_attendee_name,
    national_id_ruling_prfrmr_name,
    cs10_id_decision_assigne1_name,
    min_co03_id,
    gharar_reg_cmpl_date,
    max_co03_id_has_otcm,
    outcome_max_co03_id_has_otcm,
    min_co03_hearing_date,
    movafeghat_gharar_sadere_date,
    ca02_return_version_dest,
    cc03_id_ruling_letter,
    co03_decision,
    co01_portal_channel,
    gto_id
FROM
    reports.v_obj60_khozestan

"""


def get_sql_allhesabrasi():
    return """

SELECT
    cr01_internal_id,
    current_office,
    ca02_tax_year,
    ca02_return_id,
    ca02_return_version,
    ca09_tax_type_code,
    cstd_return_type,
    max_cu05_id,
    min_cu05_id,
    count_cu05_id,
    cstd_audit_status,
    cu05_audit_review_flag,
    cu05_audit_type,
    cu05_risk_band,
    cu05_report_num,
    cu05_createdate,
    cu05_rpt_approved_date,
    auditor_name1,
    auditor_name2,
    davat_number,
    davat_sent_date,
    davat_create_date,
    davat_eblagh_date,
    max_case_refrence,
    min_case_refrence,
    max_stage,
    ce06_case_type_id,
    ce02_date_created,
    cstd_case_status,
    ce02_case_status_date,
    general_closure_date,
    general_close_date,
    review_closure_date,
    review_close_date,
    closure_97_date,
    close_97_date,
    closure_evasion_date,
    close_evasion_date,
    auditor_name,
    closure_date,
    closed_date,
    cu05_startdate,
    soratmajles_num,
    end_aud_report_num,
    general_step5_date,
    review_step5_date,
    step5_97_date,
    step5_evasion_date,
    step5_date,
    cu05_invitation_type,
    aditor_name_case,
    cs10_national_id,
    aditor_name_asli,
    cs10_national_id_asli,
    gto_id
FROM
    reports.v_aud35_khozestan

"""


def get_sql_sanimusers():
    return """
    
SELECT
    cs10_id,
    cs10_name,
    cs10_national_id,
    cs04_id,
    cs08_id,
    code_desc,
    gto_id
FROM
    reports.v_users_khozestan

    """


def get_sql_allsanim():

    return """
            SELECT "CR01_INTERNAL_ID", "CR01_TIN_ID", "TPNAME", "CR04_FATHER_NAME", "CR01_ACT_START_DATE",
            "ADDRESS", "CR25_FIXED_PHONE", "CR13_TRADE_NAME", "CSTD_TAXPAYER_SIZE", "CR04_BIRTH_DATE",
            "CR12_NATIONAL_ID", "CSTD_GENDER", "CSTD_LEGAL_ENTITY_TYPE", "CR01_NATURAL_PER_FLAG",
            "CSTD_TAXPAYER_STATUS", "CR01_FOLLOW_CODE", "ISIC_CODE_LEVEL_5", "DESC_ACTIVITY_LEVEL_5", 
            "GTO_ID", "DIRECTORATE", "OFFICE", "CS04_NAME", "TAX_RETURN_NO", "YEAR", "CA09_TAX_TYPE_CODE", 
            "CA02_TAX_PERIOD", "TAXRETURN_DATE", "CSTD_FILING_CHANNEL", "CA02_DUE_DATE", "AUTHORISE_NO", 
            "AUTHORISE_DATE", "INVITATION_DATE", "INV_REC_DATE", "AUD_SORATMAJLES_DATE", "ASSESS_DATE", 
            "ASS_REC_DATE", "CO01_REQUEST_RECEIVED_ON", "CSTD_REQUEST_TYPE", "CO03_HEARING_DATE", "CO03_OUTCOME", 
            "RULLING_DATE", "RULLING_APPROVED", "CLOSED_DATE", "ASSIGN_TO_NAME", "INTA_ATTENDEE_NAME", "INTA_ATTENDEE_TYPE", 
            "AGREE", "GHARAR", "TADIL", "RAF_TAROZ", "TAID", "RULLING_PERFORMER_NAME", "BADVI_DAVAT_CREATE_DATE", "OBJ1_RESULT_DATE", 
            "TJDID_DAVAT_CREATE_DATE", "OBJ2_RESULT_DATE", "FINAL_DATE", "TAXRETURN_INCOME", "TAXRETURN_TAX", "ASSESS_INCOME", 
            "ASSESS_TAX", "DARAMAD_ETERAZ", "OBJ1_RESULT_INCOME", "OBJ2_RESULT_INCOME", "FINAL_INCOME", "FINAL_TAX", "AMOUNT", 
            "TALIGH_ADAMFAAL", "MANBA_SABTNAM", "VAZIYAT_MANBA_SABTNAM", "ZIAN", "EJRA_BAND3_NUM", "EJRA_BAND3_CREATE_DATE", 
            "EJRA_BAND3_EBLAGH_DATE", "TASHKHIS_NUM", "TAMKIN_NUM", "TAMKIN_CREATE_DATE", "ETERAZ_REQUEST_NUM", 
            "ETERAZ_RAY_APPROVE_DATE", "ETERAZ_NAMAYANDE_NAME", "ETERAZ_NAMAYANDE_SEMAT", "TAVAFOGH", "ETERAZ_RAY_EBLAGH_DATE", 
            "BADVI_MEETING_DATE", "BADVI_DAVAT_EBLAGH_DATE", "BADVI_RAY_EBLAGH_DATE", "TAJDID_MEETING_DATE", 
            "TJDID_DAVAT_EBLAGH_DATE", "TAJDID_RAY_EBLAGH_DATE", "GHATI_NUM", "GHATI_EBLAGH_DATE", "PENALTY", "PENALTY_RPP", 
            "RECEIVING", "PENALTY_169", "PENALTY_WITH_OUT_169", "PENALTY_RPP_169", "PENALTY_RPP_WITH_OUT_169", "TAX", "MALIYAT_ETERAZ", 
            "DARAMAT_ETERAZ_KASR", "MALIAT_BADVI", "DARAMAD_BADVI_KASR", "MALIYAT_TAJDID", "DARAMAD_TAJDID_KASR", "BARGE_EJRA_NUM", 
            "BARGE_EJRA_CREATE_DATE", "BARGE_EJRA_DELIVERED_DATE", "RET_PSTD", "RET_PSTD_SOURCE", "RET_PSTD_SOURCE_DESC", 
            "HAMARZ_REQUEST_NUM", "HAMARZ_MEETING_DATE", "HAMARZ_RAY_APPROVE_DATE", "HAMARZ_DAVAT_CREATE_DATE", 
            "HAMARZ_DAVAT_EBLAGH_DATE", "HAMARZ_RAY_EBLAGH_DATE", "MOKARAR251_REQUEST_NUM", "MOKARAR251_MEETING_DATE", 
            "MOKARAR251_RAY_APPROVE_DATE", "MOKARAR251_DAVAT_CREATE_DATE", "MOKARAR251_DAVAT_EBLAGH_DATE", "MOKARAR251_RAY_EBLAGH_DATE", 
            "MOKARAR169_REQUEST_NUM", "MOKARAR169_MEETING_DATE", "MOKARAR169_RAY_APPROVE_DATE", "MOKARAR169_DAVAT_CREATE_DATE", 
            "MOKARAR169_DAVAT_EBLAGH_DATE", "MOKARAR169_RAY_EBLAGH_DATE", "MALIYAT_HAMARZ", "DARAMAD_HAMRAZ", "DARAMAD_HAMARZ_KASR", 
            "MALIYAT_MOKARAR251", "DARAMAD_MOKARAR251", "DARAMAD_MOKARAR251_KASR", "MALIYAT_MOKARAR169", "DARAMAD_MOKARAR169", 
            "DARAMAD_MOKARAR169_KASR", "CA02_TAX_DUE", "REQUEST_RECEIVED_ON_BADVI", "REQUEST_RECEIVED_ON_TAJDID", 
            "REQUEST_RECEIVED_ON_HAMARZ", "REQUEST_RECEIVED_ON_NOKARAR251", "REQUEST_RECEIVED_ON_MOKARAR169", "MALIYAT_ESLAH_SAZMAN", 
            "DARAMAD_ESLAH_SAZMAN", "DARAMAD_ESLAH_SAZMAN_KASR", "TAX_GHATI", "PAYMENT_GHATI", "REMAINED_GHATI", 
            "DECISION_ASSIGNEE_BADVI", "DECISION_ASSIGNEE_TAJDID", "CSTD_REQUEST_CHANNEL", "CSTD_NATIONALITY", "CSTD_REG_COUNTRY", 
            "CR10_OLD_REG_NUMBER", "CR19_AREA_CODE", "RULLING_DATE_TO", "RULLING_DATE_B1", "MIN_TXP_CA02_STATUS_MOD_DATE", 
            "CA02_EXTERNAL_ID_TXP_MAX", "CSTD_RETURN_TYPE", "AUDITOR_NAME", "BADVI_REQUEST_NUM", "TAJDID_REQUEST_NUM", 
            "CS10_ID_ASSIGN_TO_NAME", "CS10_ID_INTA_ATTENDEE_NAME", "NATIONAL_ID_RULING_PRFRMR_NAME", "PERFORMER_TASHKHIS_NUM", 
            "CS10_ID_ETERAZ_NAMAYANDE_NAME", "PERFORMER_GHATI_NUM", "CS10_ID_DECISION_ASIGNE_BADVI", "CS10_ID_DECISION_ASIGNE_TAJDID", 
            "MANBA_GHATIAT", "CA02_PARCEL_NO", "RULING_DESC_TO", "RULING_DESC_B1", "EBRAZI_SALE", "TASHKHIS_SALE", "GHATI_SALE", 
            "EBRAZI_AVAREZ", "TASHKHIS_AVAREZ", "ETERAZ_AVAREZ", "BADVI_AVAREZ", "TAJDID_AVAREZ", "GHATI_AVAREZ", "PERFORMER_NAME_TASH", 
            "EBLAGH_TYPE_TASH", "ELECTRONIC_NOTIFICATION_TASH", "PERFORMER_TASH", "PERFORMER_NAME_GHAT", "EBLAGH_TYPE_GHAT", 
            "ELECTRONIC_NOTIFICATION_GHAT", "PERFORMER_GHAT", "PERFORMER_NAME_EJRA", "EBLAGH_TYPE_EJRA", "ELECTRONIC_NOTIFICATION_EJRA", 
            "PERFORMER_EJRA", "BAKHSHODEGI" FROM(
    SELECT /*+ no_parallel("V_PORTAL_KHOZESTAN") */  * FROM "REPORTS"."V_PORTAL_KHOZESTAN"
    )d"""


def get_sql_allbakhshodegi():

    return """
    SELECT
        cr01_internal_id,
        ct01_posting_date,
        ct01_period,
        ct01_tax_year,
        cstd_tax_type,
        ct01_amount,
        cstd_liability_type,
        cstd_tran_type,
        ct01_desc,
        cstd_entity,
        gto_id
    FROM
        reports.v_impunity_khozestan

"""


def get_sql_allhesabdari():

    return """

SELECT
    ca02_return_id,
    is_169,
    remaind_all,
    remaind_tax,
    remaind_duty,
    remaind_other,
    remaind_pen_tax,
    remaind_pen_duty,
    remaind_169,
    remaind_169r,
    tax_assesment,
    pay_va_rpp,
    tax_tax,
    tax_duty,
    tax_other,
    pen_tax,
    pen_duty,
    pen_other,
    pen_169,
    pen_169r,
    intres,
    intresd,
    pay_tax,
    rpp_tax,
    pay_duty,
    rpp_duty,
    pay_other,
    rpp_other,
    pay_pen_tax,
    rpp_pen_tax,
    pay_pen_duty,
    rpp_pen_duty,
    pay_pen_169,
    rpp_pen_169,
    pay_pen_169r,
    rpp_pen_169r,
    pay_intres,
    rpp_intres,
    pay_intresd,
    rpp_intresd,
    gto_id
FROM
    reports.v_ehmoadi_khozestan

"""


def get_sql_allanbare():

    return """

SELECT
    cr01_tin_id,
    cr01_internal_id,
    cstd_audit_status,
    cu05_auditor,
    gto_id
FROM
    reports.v_audpool_khozestan

"""


def get_sql_sanimDarjariabBadvi():

    return """

    SELECT [شماره اقتصادی],[نام اداره],obj.* FROM
    (SELECT  [ID]
        ,[شناسه داخلی سامانه سنیم]
        ,[اداره فعلي]
        ,[سال عملکرد اظهارنامه]
        ,[شماره اظهارنامه]
        ,[آخرين ورژن POSTED اظهارنامه]
        ,[کد منبع مالياتي اظهارنامه]
        ,[کد نوع اظهارنامه]
        ,[شماره درخواست اعتراض / شکایت]
        ,[کد وضعيت درخواست اعتراض / شکایت]
        ,[کد نوع درخواست اعتراض / شکایت]
        ,[شماره منبع درخواست اعتراض / شکایت]
        ,[نوع قرار / نوع برگه ای که به آن اعتراض / شکایت شده است]
        ,[تاریخ منبع درخواست اعتراض / شکایت]
        ,[CO01_PRE_NOTICE_DATE]
        ,[کد وضعيت بازپس گیری]
        ,[CO01_WITHDRAWAL_TO]
        ,[تاريخ دريافت بازپس گيري]
        ,[تاريخ دريافت درخواست اعتراض / شکايت]
        ,[بیشترین شناسه ی ثبت شده ی جلسه استماع به ازای یک شماره درخواست اعتراض / شکایت]
        ,[تاريخ برگزاري جلسه استماع (آخرین جلسه استماع)]
        ,[کد وضعیت برگزاري جلسه استماع (آخرین جلسه استماع)]
        ,[کد نتیجه جلسه استماع (آخرین جلسه استماع)]
        ,[تاريخ رای]
        ,[تاريخ تاييد رای]
        ,[تاريخ بسته شدن اعتراض / شکايت]
        ,[نام کارمندی که کيس اعتراض به او تخصیص داده شده]
        ,[TP_AGREE]
        ,[نام نماينده سازمان]
        ,[سمت نماينده سازمان]
        ,[کد نماينده سازمان (آخرین جلسه استماع)]
        ,[شماره کيس اعتراض / شکایت قبلی]
        ,[نوع کيس اعتراض / شکایت قبلی]
        ,[TA_AGREE]
        ,[توافق ]
        ,[قرار ]
        ,[مهلت اجرای قرار]
        ,[تعديل ]
        ,[رفع تعرض]
        ,[تاييد]
        ,[نام فرد تاييد کننده رای]
        ,[نام کاربری مجری قرار ]
        ,[نام و نام خانوادگی مجری قرار ]
        ,[کد نامه منبع درخواست اعتراض]
        ,[آیا اعتراض / شکایت مربوط به ماده 169 هست یا عادی]
        ,[MAX_CO01_REQUEST_NO]
        ,[کد کاربری کارمندی که کيس اعتراض به او تخصیص داده شده]
        ,[کد کاربری نماينده سازمان]
        ,[کد کاربری  تاييد کننده رای]
        ,[کد کاربری مجری قرار]
        ,[کمترین شناسه ی ثبت شده ی جلسه استماع به ازای یک شماره درخواست اعتراض / شکایت]
        ,[تاریخ ثبت تکمیل اجرای قرار]
        ,[آخرین جلسه استماع دارای نتیجه، به ازای یک شماره درخواست اعتراض / شکایت]
        ,[نتیجه ی جلسه ی استماع (آخرین جلسه استماع دارای نتیجه، به ازای یک شماره درخواست اعتراض/شکایت)]
        ,[تاریخ کمترین شناسه ی ثبت شده ی جلسه استماع به ازای یک شماره درخواست اعتراض / شکایت]
        ,[تاریخ موافقت با قرار صادره جلسه استماع]
        ,[CA02_RETURN_VERSION_DEST]
        ,[CC03_ID_RULING_LETTER]
        ,[CO03_DECISION]
        ,[CO01_PORTAL_CHANNEL]
        ,[کد اداره کل]
        ,[تاریخ بروزرسانی]
    FROM [TestDb].[dbo].[V_OBJ60] 
    WHERE [کد نوع درخواست اعتراض / شکایت]='02' and [کد وضعيت درخواست اعتراض / شکایت]<>'OBJ_CPLT' 
    and [کد وضعيت درخواست اعتراض / شکایت]<>'OBJ_CLSD'
    and [تاريخ برگزاري جلسه استماع (آخرین جلسه استماع)]='NaT')
    as obj

    LEFT JOIN

    (SELECT DISTINCT [کد یکتای داخلی مؤدی],[شماره اقتصادی], [نام اداره]
    FROM [dbo].[V_PORTAL]) as portal ON obj.[شناسه داخلی سامانه سنیم]=portal.[کد یکتای داخلی مؤدی]

"""
