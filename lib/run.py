from models.houses import Houses
from models.tenants import Tenants
from models.payments import Payments

Houses.drop_table()
Houses.create_table()

Tenants.drop_table()
Tenants.create_table()

Payments.drop_table()
Payments.create_table()



house1=Houses.create("Double Tree","Ngong Road",25)
tenant1=Tenants.create("Juliet Karimi",1001,1,"0722435678")
payment1=Payments.create(1001,"SDJ09JKL",20000,1,"Double Tree",2023-12-12,"mpesa")

payments_with_tenants=Payments.get_all_with_tenants()
for payment in payments_with_tenants:
    print(f"Payment ID:{payment.id},Tenant Name:{payment.tenant_name},Phone Number:{payment.phone_number}")
