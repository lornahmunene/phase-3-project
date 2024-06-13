from config.connection import conn,cursor
class Tenants:
    all={}

    def __init__(self, id, name,tenant_number, house_id, phone_number):
        self.id = id
        self.tenant_number=tenant_number
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
         # Simple check to ensure phone number contains only digits and is of a reasonable length
         if not value.isdigit() or len(value) < 10 or len(value) > 15:
             raise ValueError("Phone number must contain only digits and be 10 to 15 characters long")
         self._phone_number = value

    @classmethod
    def drop_table(cls):
        sql = """DROP TABLE IF EXISTS tenants"""
        cursor.execute(sql)
        conn.commit()

    @classmethod
    def create_table(cls):
        sql = """
        CREATE TABLE tenants (
            tenant_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            tenant_number INTEGER UNIQUE,
            house_id INTEGER,
            phone_number TEXT
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
        # this "type(self).all[self.id]=self" allocates the dictionary key using the row's primary key  
        type(self).all[self,id]=self
    @classmethod
    def create(cls,name,tenant_number,house_id,phone_number):
        tenant=cls(None,name,tenant_number,house_id,phone_number)
        tenant.save()
        return tenant
    def delete(self):
        sql="""
            DELETE FROM payments
            WHERE id=?
        """
        cursor.execute(sql,(self.id))
        conn.commit()
        del type(self).all[self.id]
    @classmethod
    def instance_from_db(cls,row):
        id,name,tenant_number,house_id,phone_number=row
        tenant=cls.all.get(id)
        if tenant:
            tenant.name=name
            tenant.tenant_number=tenant_number
            tenant.house_id=house_id
            tenant.phone_number=phone_number
        else:
            tenant=cls(id,tenant_number,house_id,phone_number)
            cls.all[id]=tenant
        return tenant
    @classmethod
    def get_all(cls):
        sql="""
           SELECT *
           FROM tenats
        """
        rows=cursor.execute(sql).fetchall()
        return [cls.instance_from_db(row)for row in rows]
    @classmethod
    def find_by_name(cls,name):
        sql="""
            SELECT *
            FROM tenants
            WHERE name is ?
        """
        row=cursor.execute(sql,(name,)).fetchone()
        return cls.instance_from_db(row) if row else None
    

        
            
