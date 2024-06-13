from config.connection import conn, cursor

class Houses:
    all={}
    def __init__(self, house_name, address, capacity, id=None):
        self.house_name = house_name
        self.address = address
        self.capacity = capacity
        self.id = id
    # @property
    # def capacity(self):
    #     return self._capacity

    # @capacity.setter
    # def capacity(self, value):
    #     if value < 0:
    #         raise ValueError("Capacity must be a non-negative integer")
    #     self._capacity = value

    @classmethod
    def drop_table(cls):
        sql = """DROP TABLE IF EXISTS houses"""
        cursor.execute(sql)
        conn.commit()  # Ensure the changes are committed

    @classmethod
    def create_table(cls):
        sql = """
        CREATE TABLE houses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            house_name TEXT,
            address TEXT,
            capacity INTEGER
        )
        """
        cursor.execute(sql)
        conn.commit()  

    def save(self):
        sql = """
        INSERT INTO houses (
            house_name,
            address,
            capacity
        ) VALUES (?, ?, ?)
        """
        cursor.execute(
            sql,
            (
                self.house_name,
                self.address,
                self.capacity
            )
        )
        conn.commit() 
        # get the id from the saved instance
        self.id=cursor.lastrowid
        type(self).all[self.id]=self
    @classmethod
    def create(cls,house_name,address,capacity):
        house=cls(house_name,address,capacity)
        house.save()
        return house
    
    def delete(self):
        sql="""
          DELETE FROM houses
          WHERE id=?
        """
        cursor.execute(sql,(self.id))
        conn.commit()
        del type(self).all[self.id]
    @classmethod
    def instance_from_db(cls,row):
        id,house_name,address,capacity=row
        house=cls.all.get(id)
        if house:
            house.house_name=house_name
            house.address=address
            house.capacity=capacity
        else:
            house=cls(id,house_name,address,capacity)
            cls.all[id]=house
        return house
    @classmethod
    def get_all(cls):
        sql="""
           SELECT *
           FROM houses
        """
        rows=cursor.execute(sql).fetchall()
        cls.all={}
        return [cls.instance_from_db(row) for row in rows]
    @classmethod
    def find_by_name(cls,house_name):
        sql="""
            SELECT *
            FROM houses
            WHERE house_name is ?
        """
        row=cursor.execute(sql,(house_name,)).fetchone()
        return cls.instance_from_db(row) if row else None

