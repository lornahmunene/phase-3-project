from config.connection import conn, cursor

class Tenants:
    all = {}

    def __init__(self, id, name, tenant_number, house_id, phone_number):
        self.id = id
        self.tenant_number = tenant_number
        self.name = name
        self.house_id = house_id
        self.phone_number = phone_number

    @property
    def tenant_number(self):
        return self._tenant_number

    @tenant_number.setter
    def tenant_number(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Tenant number must be a positive integer")
        self._tenant_number = value

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value):
        if not value.isdigit() or len(value) < 10 or len(value) > 15:
            raise ValueError("Phone number must contain only digits and be 10 to 15 characters long")
        self._phone_number = value
    @property
    def house_id(self):
        return self._house_id

    @house_id.setter
    def house_id(self, value):
        if not isinstance(value, int):
            raise ValueError("House ID must be a number")
        self._house_id = value

    @classmethod
    def drop_table(cls):
        sql = """DROP TABLE IF EXISTS tenants"""
        cursor.execute(sql)
        conn.commit()

    @classmethod
    def create_table(cls):
        sql = """
        CREATE TABLE tenants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            tenant_number INTEGER UNIQUE,
            house_id INTEGER,
            phone_number TEXT
            FOREIGN KEY (house_id) REFERENCES houses(house_id)
        )
        """
        cursor.execute(sql)
        conn.commit()

    def save(self):
        sql = """
        INSERT INTO tenants (
            name,
            tenant_number,
            house_id,
            phone_number
        ) VALUES (?, ?, ?, ?)
        """
        cursor.execute(
            sql,
            (
                self.name,
                self.tenant_number,
                self.house_id,
                self.phone_number
            )
        )
        conn.commit()
        self.id = cursor.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, tenant_number, house_id, phone_number):
        tenant = cls(None, name, tenant_number, house_id, phone_number)
        tenant.save()
        return tenant

    def delete(self):
        sql = """
            DELETE FROM tenants
            WHERE id = ?
        """
        cursor.execute(sql, (self.id,))
        conn.commit()
        del type(self).all[self.id]

    @classmethod
    def instance_from_db(cls, row):
        id, name, tenant_number, house_id, phone_number = row
        tenant = cls.all.get(id)
        if tenant:
            tenant.name = name
            tenant.tenant_number = tenant_number
            tenant.house_id = house_id
            tenant.phone_number = phone_number
        else:
            tenant = cls(id, name, tenant_number, house_id, phone_number)
            cls.all[id] = tenant
        return tenant

    @classmethod
    def get_all(cls):
        sql = """
           SELECT id, name, tenant_number, house_id, phone_number
           FROM tenants
        """
        rows = cursor.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT id, name, tenant_number, house_id, phone_number
            FROM tenants
            WHERE name = ?
        """
        row = cursor.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None
