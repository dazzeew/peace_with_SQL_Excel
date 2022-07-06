import psycopg2
from contextlib import closing
month_list = {'Январь': 31,'Февраль': 28,'Март': 31,'Апрель': 30,'Май': 31,'Июнь': 30,'Июль': 31,'Август': 31,'Сентябрь': 30,'Октябрь': 31,'Ноябрь': 30,'Декабрь': 31}
month_list_pgl = {'Январь': '01','Февраль': '02','Март': '03','Апрель': '04','Май': '05','Июнь': '06','Июль': '07','Август': '08','Сентябрь': '09','Октябрь': '10','Ноябрь': '11','Декабрь': '12'}

db_name = 'batya'
user_name = 'postgres'
password = 'postgres'
host = 'localhost'

# db_name = 'karpovld_batya'
# user_name = 'postgres'
# password = '5gD*qt%l'
# host = 'localhost'

#pass 3N6j6R5l5Y

def check_company():
    conn = psycopg2.connect(dbname=db_name, user=user_name, 
                        password=password, host=host)
    cursor = conn.cursor()
    cursor.execute('select name_company from company order by name_company')
    list = []
    for row in cursor:
        list.append(row[0])
    cursor.close()
    conn.commit()
    return list

def check_type():
    conn = psycopg2.connect(dbname=db_name, user=user_name, 
                        password=password, host=host)
    cursor = conn.cursor()
    cursor.execute('select name_type from types order by name_type')
    list = []
    for row in cursor:
        list.append(row[0])
    cursor.close()
    conn.commit()
    return list

def check_product(types):
    conn = psycopg2.connect(dbname=db_name, user=user_name, 
                        password=password, host=host)
    cursor = conn.cursor()
    cursor.execute('select id from types where name_type = %s ',(types,))
    x = 0
    for row in cursor:
        x = row[0]
    cursor.execute('select distinct name_product from product where id_type = %s order by name_product',(x,))
    list = []
    for row in cursor:
        list.append(row[0])
    cursor.close()
    conn.commit()
    return list

def check_iprice(types,name):
    conn = psycopg2.connect(dbname=db_name, user=user_name, 
                        password=password, host=host)
    cursor = conn.cursor()
    cursor.execute('select id from types where name_type = %s ',(types,))
    x = 0
    for row in cursor:
        x = row[0]
    cursor.execute('select distinct price_for_unit from product where id_type = %s and name_product = %s order by price_for_unit',(x,name,))
    list = []
    for row in cursor:
        list.append(row[0])
    cursor.close()
    conn.commit()
    return list


def input_week():
    conn = psycopg2.connect(dbname=db_name, user=user_name, 
                        password=password, host=host)
    cursor = conn.cursor()
    cursor.execute('select c.name_company,$$|$$,p.name_product,$$|$$,b.count,$$|$$,(b.count * p.price_for_unit)::int as sum from buy_order b inner join company c on c.id = b.id_company inner join product p on p.id = b.id_product where b.date_buy <= now()::date and b.date_buy >= (now()::date - $$1 week$$::interval)::date group by c.name_company,p.name_product,b.count,sum;')
    list = []
    for row in cursor:
        list.append(row)
    cursor.close()
    conn.commit()
    return list    

def output_week():
    conn = psycopg2.connect(dbname=db_name, user=user_name, 
                        password=password, host=host)
    cursor = conn.cursor()
    cursor.execute('select c.name_company,$$|$$,p.name_product,$$|$$,s.count,$$|$$,(s.count * s.sale_price)::int as sum from sale_order s inner join company c on c.id = s.id_company inner join product p on p.id = s.id_product where s.date_sale <= now()::date and s.date_sale >= (now()::date - $$1 week$$::interval)::date group by c.name_company,p.name_product,s.count,sum;')
    list = []
    for row in cursor:
        list.append(row)
    cursor.close()
    conn.commit()
    return list

def input_month():
    conn = psycopg2.connect(dbname=db_name, user=user_name, 
                        password=password, host=host)
    cursor = conn.cursor()
    cursor.execute('select sum(b.count * p.price_for_unit) from buy_order b inner join product p on p.id = b.id_product where EXTRACT(MONTH FROM b.date_buy::date) = EXTRACT(MONTH FROM now()::date) and EXTRACT(YEAR FROM b.date_buy::date) = EXTRACT(YEAR FROM now()::date);')
    list = 0
    for row in cursor:
        if row[0] is None:
            list = 0
        else:
            list = int(row[0])
    cursor.close()
    conn.commit()
    return list
    # return 1
def output_month():
    conn = psycopg2.connect(dbname=db_name, user=user_name, 
                        password=password, host=host)
    cursor = conn.cursor()
    cursor.execute('select sum(count * sale_price) from sale_order where EXTRACT(MONTH FROM date_sale::date) = EXTRACT(MONTH FROM now()::date) and EXTRACT(YEAR FROM date_sale::date) = EXTRACT(YEAR FROM now()::date);')
    list = 0
    for row in cursor:
        if row[0] is None:
            list = 0
        else:
            list = int(row[0])
    cursor.close()
    conn.commit()
    return list

def id_types(types):
    conn = psycopg2.connect(dbname=db_name, user=user_name, 
                        password=password, host=host)
    cursor = conn.cursor()
    cursor.execute('select id from types where name_type = %s;',(types,))
    list = 0
    for row in cursor:
        list = int(row[0])
    cursor.close()
    conn.commit()
    return list

def id_company(company):
    conn = psycopg2.connect(dbname=db_name, user=user_name, 
                        password=password, host=host)
    cursor = conn.cursor()
    cursor.execute('select id from company where name_company = %s;',(company,))
    list = 0
    for row in cursor:
        list = int(row[0])
    cursor.close()
    conn.commit()
    return list

def id_product(product,types,iprice):
    conn = psycopg2.connect(dbname=db_name, user=user_name, 
                        password=password, host=host)
    cursor = conn.cursor()
    cursor.execute('select p.id from product p inner join types t on p.id_type = t.id where p.name_product = %s and t.id = %s and price_for_unit = %s;',(product,types,iprice,))
    list = 0
    for row in cursor:
        list = int(row[0])
    cursor.close()
    conn.commit()
    return list


def record(list):
    conn = psycopg2.connect(dbname=db_name, user=user_name, 
                        password=password, host=host)
    cursor = conn.cursor()
    typess = id_types(list[6])
    id_comp = id_company(list[5])
    id_prod = id_product(list[7],typess,list[8])
    if (list[1] == 0):
        if (list[0]):
            cursor.execute('INSERT INTO buy_order(id_company,id_product,date_buy,count) VALUES(%s,%s,now()::date,%s);',(id_comp,id_prod,list[9],))
        else:
            if int(list[2]) < 10:
                list[2] = '0' + list[2]
            date = list[4] + month_list_pgl[list[3]] + list[2]
            cursor.execute('INSERT INTO buy_order(id_company,id_product,date_buy,count) VALUES(%s,%s,%s,%s);',(id_comp,id_prod,date,list[9],))
    else:
        if (list[0]):
            cursor.execute('INSERT INTO sale_order(id_company,id_product,date_sale,count,sale_price) VALUES(%s,%s,now()::date,%s,%s);',(id_comp,id_prod,list[9],list[10],))
        else:
            if int(list[2]) < 10:
                list[2] = '0' + list[2]
            date = list[4] + month_list_pgl[list[3]] + list[2]
            cursor.execute('INSERT INTO sale_order(id_company,id_product,date_sale,count,sale_price) VALUES(%s,%s,%s,%s,%s);',(id_comp,id_prod,date,list[9],list[10],))
    cursor.close()
    conn.commit()

def plus_co(company):
    conn = psycopg2.connect(dbname=db_name, user=user_name, 
                        password=password, host=host)
    cursor = conn.cursor()
    cursor.execute('select count(id) from company where name_company = %s;',(company,))
    exc = 0
    for row in cursor:
        exc = int(row[0])
    if exc > 0:
        return False
    else:
        cursor.execute('INSERT INTO company(name_company) VALUES(%s);',(company,))
        cursor.close()
        conn.commit()
        return True

def minus_co(company):
    conn = psycopg2.connect(dbname=db_name, user=user_name, 
                        password=password, host=host)
    cursor = conn.cursor()
    cursor.execute('delete from company where name_company = %s;',(company,))
    cursor.close()
    conn.commit()

def plus_pro(product,types,iprice):
    conn = psycopg2.connect(dbname=db_name, user=user_name, 
                        password=password, host=host)
    cursor = conn.cursor()
    typess = id_types(types)
    cursor.execute('select count(id) from product where name_product = %s and price_for_unit = %s and id_type = %s;',(product,str(iprice),typess))
    exc = 0
    for row in cursor:
        exc = int(row[0])
    if exc > 0:
        return False
    else:
        cursor.execute('INSERT INTO product(name_product,price_for_unit,id_type) VALUES(%s,%s,%s);',(product,iprice,typess))
        cursor.close()
        conn.commit()
        return True

def minus_pro(product,types,iprice):
    conn = psycopg2.connect(dbname=db_name, user=user_name, 
                        password=password, host=host)
    cursor = conn.cursor()
    typess = id_types(types)
    cursor.execute('delete from product where name_product = %s and id_type = %s and price_for_unit = %s;',(product,typess,iprice,))
    cursor.close()
    conn.commit()

def plus_type(typess):
    conn = psycopg2.connect(dbname=db_name, user=user_name, 
                        password=password, host=host)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO types(name_type) VALUES (%s);',(typess,))
    cursor.close()
    conn.commit()

def minus_type(typess):
    conn = psycopg2.connect(dbname=db_name, user=user_name, 
                        password=password, host=host)
    cursor = conn.cursor()
    cursor.execute('delete from types where name_type = %s;',(typess,))
    cursor.close()
    conn.commit()
# select sum(b.count * p.price_for_unit) from buy_order b inner join product p on p.id = b.id_product where b.date_buy >= now()::date - '1 month'::interval and b.date_buy <= now()::date;
# record(True,1,'24','February','2022','TEST#1','Резина','PRODUCT#3',20,20,10)
def info_count(name,types,iprice):
    conn = psycopg2.connect(dbname=db_name, user=user_name, 
                        password=password, host=host)
    cursor = conn.cursor()
    result = 0
    typess = id_types(types)
    cursor.execute('select count from product where name_product = %s and price_for_unit = %s and id_type = %s;',(name,iprice,typess,))
    for row in cursor:
        result = (row[0])
    cursor.close()
    conn.commit()
    return result

#Excel
def storage():
    conn = psycopg2.connect(dbname=db_name, user=user_name, 
                        password=password, host=host)
    cursor = conn.cursor()
    result = []
    cursor.execute('select p.name_product, t.name_type, p.price_for_unit, p.count from product p inner join types t on p.id_type = t.id;')
    for row in cursor:
        result.append(row)
    cursor.close()
    conn.commit()
    return result

def io_listing(list):
    conn = psycopg2.connect(dbname=db_name, user=user_name, 
                        password=password, host=host)
    cursor = conn.cursor()
    id_comp = id_company(list[6])
    if (list[5] == 0):
        if ((list[3] is False) and (list[2] is False)):
            typess = id_types(list[7])
            id_prod = id_product(list[8],typess,list[9])
            cursor.execute('select c.name_company, p.name_product, b.date_buy::varchar, b.count, p.price_for_unit, (p.price_for_unit*b.count) as sum from buy_order b inner join product p on p.id = b.id_product inner join company c on c.id = b.id_company where (b.date_buy between %s and (%s::date + $$1 month$$::interval - $$1 day$$::interval)) and c.id = %s and b.id_product = %s order by b.date_buy;',(list[0],list[1],id_comp,id_prod,))
        elif ((list[3] is False) and (list[2] is True)):
            cursor.execute('select c.name_company, p.name_product, b.date_buy::varchar, b.count, p.price_for_unit, (p.price_for_unit*b.count) as sum from buy_order b inner join product p on p.id = b.id_product inner join company c on c.id = b.id_company where (b.date_buy between %s and (%s::date + $$1 month$$::interval - $$1 day$$::interval)) and c.id = %s order by b.date_buy;',(list[0],list[1],id_comp,))  
        elif ((list[3] is True) and (list[2] is False)):
            typess = id_types(list[7])
            id_prod = id_product(list[8],typess,list[9])
            cursor.execute('select c.name_company, p.name_product, b.date_buy::varchar, b.count, p.price_for_unit, (p.price_for_unit*b.count) as sum from buy_order b inner join product p on p.id = b.id_product inner join company c on c.id = b.id_company where (b.date_buy between %s and (%s::date + $$1 month$$::interval - $$1 day$$::interval)) and b.id_product = %s order by b.date_buy;',(list[0],list[1],id_prod,))
        elif ((list[3] is True) and (list[2] is True)):
            cursor.execute('select c.name_company, p.name_product, b.date_buy::varchar, b.count, p.price_for_unit, (p.price_for_unit*b.count) as sum from buy_order b inner join product p on p.id = b.id_product inner join company c on c.id = b.id_company where (b.date_buy between %s and (%s::date + $$1 month$$::interval - $$1 day$$::interval)) order by b.date_buy;',(list[0],list[1],))
    elif (list[5] == 1):
        if ((list[3] is False) and (list[2] is False)):
            typess = id_types(list[7])
            id_prod = id_product(list[8],typess,list[9])
            cursor.execute('select c.name_company, p.name_product, s.date_sale::varchar, s.count, s.sale_price, (s.count*s.sale_price) as sum from sale_order s inner join product p on p.id = s.id_product inner join company c on c.id = s.id_company where (s.date_sale between %s and (%s::date + $$1 month$$::interval - $$1 day$$::interval)) and c.id = %s and s.id_product = %s order by s.date_sale;',(list[0],list[1],id_comp,id_prod,))
        elif ((list[3] is False) and (list[2] is True)):
            cursor.execute('select c.name_company, p.name_product, s.date_sale::varchar, s.count, s.sale_price, (s.count*s.sale_price) as sum from sale_order s inner join product p on p.id = s.id_product inner join company c on c.id = s.id_company where (s.date_sale between %s and (%s::date + $$1 month$$::interval - $$1 day$$::interval)) and c.id = %s order by s.date_sale;',(list[0],list[1],id_comp,))
        elif ((list[3] is True) and (list[2] is False)):
            typess = id_types(list[7])
            id_prod = id_product(list[8],typess,list[9])
            cursor.execute('select c.name_company, p.name_product, s.date_sale::varchar, s.count, s.sale_price, (s.count*s.sale_price) as sum from sale_order s inner join product p on p.id = s.id_product inner join company c on c.id = s.id_company where (s.date_sale between %s and (%s::date + $$1 month$$::interval - $$1 day$$::interval)) and s.id_product = %s order by s.date_sale;',(list[0],list[1],id_prod,))     
        elif ((list[3] is True) and (list[2] is True)):
            cursor.execute('select c.name_company, p.name_product, s.date_sale::varchar, s.count, s.sale_price, (s.count*s.sale_price) as sum from sale_order s inner join product p on p.id = s.id_product inner join company c on c.id = s.id_company where (s.date_sale between %s and (%s::date + $$1 month$$::interval - $$1 day$$::interval)) order by s.date_sale;',(list[0],list[1],))
    if (list[5] == 2):
        if ((list[3] is False) and (list[2] is False)):
            typess = id_types(list[7])
            id_prod = id_product(list[8],typess,list[9])
            cursor.execute('select sum(s.count * s.sale_price) from sale_order s inner join product p on p.id = s.id_product inner join company c on c.id = s.id_company where (s.date_sale between %s and (%s::date + $$1 month$$::interval - $$1 day$$::interval)) and c.id = %s and s.id_product = %s;',(list[0],list[1],id_comp,id_prod,))
        elif ((list[3] is False) and (list[2] is True)):
            cursor.execute('select sum(s.count * s.sale_price) from sale_order s inner join company c on c.id = s.id_company where (s.date_sale between %s and (%s::date + $$1 month$$::interval - $$1 day$$::interval)) and c.id = %s;',(list[0],list[1],id_comp,))
        elif ((list[3] is True) and (list[2] is False)):
            typess = id_types(list[7])
            id_prod = id_product(list[8],typess,list[9])
            cursor.execute('select sum(s.count * s.sale_price) from sale_order s inner join product p on p.id = s.id_product where (s.date_sale between %s and (%s::date + $$1 month$$::interval - $$1 day$$::interval)) and s.id_product = %s;',(list[0],list[1],id_prod))
        elif ((list[3] is True) and (list[2] is True)):
            cursor.execute('select sum(s.count * s.sale_price) from sale_order s where (s.date_sale between %s and (%s::date + $$1 month$$::interval - $$1 day$$::interval));',(list[0],list[1],))
    if (list[5] == 3):
        if ((list[3] is False) and (list[2] is False)):
            typess = id_types(list[7])
            id_prod = id_product(list[8],typess,list[9])
            cursor.execute('select sum(b.count * p.price_for_unit) from buy_order b inner join product p on p.id = b.id_product inner join company c on c.id = b.id_company where (b.date_buy between %s and (%s::date + $$1 month$$::interval - $$1 day$$::interval)) and c.id = %s and b.id_product = %s;',(list[0],list[1],id_comp,id_prod,))
        elif ((list[3] is False) and (list[2] is True)):
            cursor.execute('select sum(b.count * p.price_for_unit) from buy_order b inner join company c on c.id = b.id_company inner join product p on p.id = b.id_product where (b.date_buy between %s and (%s::date + $$1 month$$::interval - $$1 day$$::interval)) and c.id = %s;',(list[0],list[1],id_comp,))
        elif ((list[3] is True) and (list[2] is False)):
            typess = id_types(list[7])
            id_prod = id_product(list[8],typess,list[9])
            cursor.execute('select sum(b.count * p.price_for_unit) from buy_order b inner join product p on p.id = b.id_product where (b.date_buy between %s and (%s::date + $$1 month$$::interval - $$1 day$$::interval)) and b.id_product = %s;',(list[0],list[1],id_prod,))
        elif ((list[3] is True) and (list[2] is True)):
            cursor.execute('select sum(b.count * p.price_for_unit) from buy_order b inner join product p on p.id = b.id_product where (b.date_buy between %s and (%s::date + $$1 month$$::interval - $$1 day$$::interval));',(list[0],list[1],))
    result = []
    for row in cursor:
        result.append(row)
    cursor.close()
    conn.commit()
    return result


# conn = psycopg2.connect(dbname='batya', user='postgres', 
#                         password='postgres', host='localhost')
# cursor = conn.cursor()
# result = []
# cursor.execute('select sum(itog.count * itog.price_for_unit) from (select b.count,p.price_for_unit,b.id_product from buy_order b inner join product p on p.id = b.id_product inner join company c on c.id = b.id_company where (b.date_buy between %s and (%s::date + $$1 month$$::interval - $$1 day$$::interval)) group by b.count,p.price_for_unit,b.id_product) as itog where itog.id_product = %s;')
# for row in cursor:
#     result.append(row)
# cursor.close()
# conn.commit()
# print(result)