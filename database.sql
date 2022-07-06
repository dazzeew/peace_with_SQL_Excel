CREATE TABLE IF NOT EXISTS company(
	id SERIAL PRIMARY KEY NOT NULL,
	name_company varchar(50) NOT NULL unique
);

CREATE TABLE IF NOT EXISTS types(
	id SERIAL PRIMARY KEY NOT NULL,
	name_type varchar(50) unique NOT NULL
);

CREATE TABLE IF NOT EXISTS product(
	id SERIAL PRIMARY KEY NOT NULL,
	name_product varchar(50) NOT NULL,
	price_for_unit real NOT NULL,
	id_type int,
	FOREIGN KEY(id_type) REFERENCES types(id),
	count int NOT NULL check (count >= 0) default 0
);

CREATE TABLE IF NOT EXISTS sale_order(
	id SERIAL PRIMARY KEY NOT NULL,
	id_company int NOT NULL,
	FOREIGN KEY(id_company) REFERENCES company(id),
	id_product int NOT NULL,
	FOREIGN KEY(id_product) REFERENCES product(id),
	date_sale date NOT NULL check (date_sale <= now()),
	count int NOT NULL,
	sale_price real NOT NULL
);

CREATE TABLE IF NOT EXISTS buy_order(
	id SERIAL PRIMARY KEY NOT NULL,
	id_company int NOT NULL,
	FOREIGN KEY(id_company) REFERENCES company(id),
	id_product int NOT NULL,
	FOREIGN KEY(id_product) REFERENCES product(id),
	date_buy date NOT NULL check (date_buy <= now()),
	count int NOT NULL
);


CREATE FUNCTION trigg_count_plus() returns trigger as $$
begin
UPDATE product set count = count + NEW.count where id = NEW.id_product;
return new;
end;
$$ LANGUAGE plpgsql;

CREATE FUNCTION trigg_count_minus() returns trigger as $$
begin
UPDATE product set count = count - NEW.count where id = NEW.id_product;
return new;
end;
$$ LANGUAGE plpgsql;

CREATE TRIGGER up_count_plus
AFTER INSERT ON buy_order
FOR EACH ROW EXECUTE PROCEDURE trigg_count_plus();

CREATE TRIGGER up_count_minus
AFTER INSERT ON sale_order
FOR EACH ROW EXECUTE PROCEDURE trigg_count_minus();
--------------Test insert----------------
-- INSERT INTO company(name_company) VALUES('TEST#1');
-- INSERT INTO company(name_company) VALUES('TEST#2');
-- INSERT INTO company(name_company) VALUES('TEST#3');
-- INSERT INTO company(name_company) VALUES('TEST#4');

-- INSERT INTO types(name_type) VALUES('Резина');
-- INSERT INTO types(name_type) VALUES('Пластик');
-- INSERT INTO types(name_type) VALUES('Саморезы');
-- INSERT INTO types(name_type) VALUES('Ручки');

-- INSERT INTO product(name_product,price_for_unit,id_type,count) VALUES('PRODUCT#1',4.3,2,5);
-- INSERT INTO product(name_product,price_for_unit,id_type,count) VALUES('PRODUCT#2',0.3,4,6);
-- INSERT INTO product(name_product,price_for_unit,id_type,count) VALUES('PRODUCT#3',2.5,3,7);
-- INSERT INTO product(name_product,price_for_unit,id_type,count) VALUES('PRODUCT#4',3.2,2,8);
-- INSERT INTO product(name_product,price_for_unit,id_type,count) VALUES('PRODUCT#3',10.5,1,9);


-- INSERT INTO buy_order(id_company,id_product,date_buy,count) VALUES(1,1,'20220401',10000);
-- INSERT INTO buy_order(id_company,id_product,date_buy,count) VALUES(1,2,'20220401',800);
-- INSERT INTO buy_order(id_company,id_product,date_buy,count) VALUES(3,4,'20220401',345);
-- INSERT INTO buy_order(id_company,id_product,date_buy,count) VALUES(2,3,'20220401',450);
-- INSERT INTO buy_order(id_company,id_product,date_buy,count) VALUES(3,1,'20220401',6000);

-- INSERT INTO sale_order(id_company,id_product,date_sale,count,sale_price) VALUES(ran,1,'20220401',13000,2.13);
-- INSERT INTO sale_order(id_company,id_product,date_sale,count,sale_price) VALUES(3,2,'20220401',200,4.2);
-- INSERT INTO sale_order(id_company,id_product,date_sale,count,sale_price) VALUES(1,3,'20220401',300,6);
-- INSERT INTO sale_order(id_company,id_product,date_sale,count,sale_price) VALUES(4,4,'20220401',100,10.57);
-- INSERT INTO sale_order(id_company,id_product,date_sale,count,sale_price) VALUES(2,1,'20220401',100,13.10);

