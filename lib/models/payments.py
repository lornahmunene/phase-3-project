from config.connection import conn, cursor

class Payments:
    all = {}
    def __init__(self, id, tenant_number, payment_code, amount, house_id, house_name, payment_date, payment_method):
        self.id = id
        self.tenant_number = tenant_number
        self.payment_code = payment_code
        self.amount = amount
        self.house_id = house_id
        self.house_name = house_name
        self.payment_date = payment_date
        self.payment_method = payment_method 

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        if value <= 0:
            raise ValueError("Amount must be positive")
        self._amount = value

    # @property
    # def payment_date(self):
    #     return self._payment_date

    # @payment_date.setter
    # def payment_date(self, value):
    #     if not isinstance(value, str) or len(value) != 10 or value[4] != '-' or value[7] != '-':
    #         raise ValueError("Payment date must be in the format YYYY-MM-DD")
    #     self._payment_date = value 

    @classmethod
    def drop_table(cls):
        sql = """DROP TABLE IF EXISTS payments"""
        cursor.execute(sql)
        conn.commit()

    @classmethod
    def create_table(cls):
        sql = """
        CREATE TABLE payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tenant_number INTEGER,
            payment_code TEXT,
            amount INTEGER,
            house_id INTEGER,
            house_name TEXT,
            payment_date DATE,
            payment_method TEXT,
            FOREIGN KEY (house_id) REFERENCES houses(house_id)
        )
        """
        cursor.execute(sql)
        conn.commit()

    def save(self):
        sql = """
        INSERT INTO payments (
            tenant_number,
            payment_code,
            amount,
            house_id,
            house_name,
            payment_date,
            payment_method
        ) VALUES (?, ?, ?, ?, ?, ?,?)
        """
        cursor.execute(
            sql,
            (
                self.tenant_number,
                self.payment_code,
                self.amount,
                self.house_id,
                self.house_name,
                self.payment_date,
                self.payment_method
            )
        )
        conn.commit()
        self.payment_id = cursor.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, tenant_number, payment_code, amount, house_id, house_name, payment_date, payment_method):
        payment = cls(None,tenant_number, payment_code, amount, house_id, house_name, payment_date, payment_method)
        payment.save()
        return payment

    def delete(self):
        sql = """
           DELETE FROM payments
           WHERE id = ?
        """
        cursor.execute(sql, (self.payment_id,))
        conn.commit()
        del type(self).all[self.payment_id]

    @classmethod
    def instance_from_db(cls, row):
        # the line below unpacks or rather separates into individual variables
        id, tenant_number, payment_code, amount, house_id, house_name, payment_date, payment_method = row
        # for the dictionary that has all instances we use a getter method to check the existence of an instance or rather an object
        payment = cls.all.get(id)
        # if an instance already exists its values are updated to match the values from the database row
        if payment:
            payment.tenant_number = tenant_number
            payment.payment_code = payment_code
            payment.amount = amount
            payment.house_id = house_id
            payment.house_name = house_name
            payment.payment_date = payment_date
            payment.payment_method = payment_method
            # if no instances a new instance is added to the dictionary all
        else:
            payment = cls(id, tenant_number, payment_code, amount, house_id, house_name, payment_date, payment_method)
            cls.all[id] = payment
            # finally the method returns the instance 
        return payment

    @classmethod
    def get_all(cls):
        sql = """
           SELECT *
           FROM payments
        """
        rows = cursor.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]
    @classmethod
    def get_all_with_tenants(cls):
        sql = """
            SELECT payments.id, payments.tenant_number, payments.payment_code, payments.amount, payments.house_id, payments.house_name, payments.payment_date, payments.payment_method, tenants.name AS tenant_name, tenants.phone_number
            FROM payments
            INNER JOIN tenants ON tenants.tenant_number = payments.tenant_number
        """
        rows = cursor.execute(sql).fetchall()
        return [cls.instance_from_db_with_tenant(row) for row in rows]

    @classmethod
    def instance_from_db_with_tenant(cls, row):
        id, tenant_number, payment_code, amount, house_id, house_name, payment_date, payment_method, tenant_name, phone_number = row
        payment = cls.all.get(id)
        if payment:
            payment.tenant_number = tenant_number
            payment.payment_code = payment_code
            payment.amount = amount
            payment.house_id = house_id
            payment.house_name = house_name
            payment.payment_date = payment_date
            payment.payment_method = payment_method
            payment.tenant_name = tenant_name
            payment.phone_number = phone_number
        else:
            payment = cls(id, tenant_number, payment_code, amount, house_id, house_name, payment_date, payment_method)
            payment.tenant_name = tenant_name
            payment.phone_number = phone_number
            cls.all[id] = payment
        return payment

    @classmethod
    def get_all_with_houses(cls):
        sql = """
            SELECT payments.id, payments.tenant_number, payments.payment_code, payments.amount, payments.house_id, payments.payment_date, payments.payment_method, houses.house_name, houses.address, houses.capacity
            FROM payments
            INNER JOIN houses ON payments.house_id = houses.id
        """
        rows = cursor.execute(sql).fetchall()
        return [cls.instance_from_db_with_house(row) for row in rows]

    @classmethod
    def instance_from_db_with_house(cls, row):
        id, tenant_number, payment_code, amount, house_id, payment_date, payment_method, house_name, address, capacity = row
        payment = cls.all.get(id)
        if payment:
            payment.tenant_number = tenant_number
            payment.payment_code = payment_code
            payment.amount = amount
            payment.house_id = house_id
            payment.payment_date = payment_date
            payment.payment_method = payment_method
            payment.house_name = house_name
            payment.address = address
            payment.capacity = capacity
        else:
            payment = cls(id, tenant_number, payment_code, amount, house_id, house_name, payment_date, payment_method)
            payment.address = address
            payment.capacity = capacity
            cls.all[id] = payment
        return payment

    