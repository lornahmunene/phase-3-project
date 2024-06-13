# lib/cli.py

from helpers import exit_program
from models.houses import Houses
from models.tenants import Tenants
from models.payments import Payments

def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            add_house()
        elif choice == "2":
            delete_house()
        elif choice == "3":
            list_houses()
        elif choice == "4":
            make_payment()
        elif choice == "5":
            list_payments()
        elif choice == "6":
            evict_tenant()
        else:
            print("Invalid choice")

def menu():
    print("Please select an option:")
    print("0. Exit the program")
    print("1. Add a new house")
    print("2. Delete a house")
    print("3. List all houses")
    print("4. Make a payment")
    print("5. List all payments")
    print("6. Evict a tenant")

def add_house():
    house_name = input("Enter house name: ")
    address = input("Enter house address: ")
    capacity = input("Enter house capacity: ")
    try:
        capacity = int(capacity)
        house = Houses.create(house_name, address, capacity)
        print(f"House {house.house_name} added successfully with ID {house.id}.")
    except ValueError:
        print("Capacity must be a number.")
    except Exception as e:
        print(f"Error: {e}")

def delete_house():
    house_id = input("Enter house ID to delete: ")
    try:
        house_id = int(house_id)
        house = Houses.all.get(house_id)
        if house:
            house.delete()
            print(f"House with ID {house_id} deleted successfully.")
        else:
            print(f"No house found with ID {house_id}.")
    except ValueError:
        print("House ID must be a number.")
    except Exception as e:
        print(f"Error: {e}")

def list_houses():
    houses = Houses.get_all()
    if houses:
        for house in houses:
            print(f"ID: {house.id}, Name: {house.house_name}, Address: {house.address}, Capacity: {house.capacity}")
    else:
        print("No houses found.")

def make_payment():
    tenant_number = input("Enter tenant number: ")
    payment_code = input("Enter payment code: ")
    amount = input("Enter payment amount: ")
    house_id = input("Enter house ID: ")
    house_name = input("Enter house name: ")
    payment_date = input("Enter payment date (YYYY-MM-DD): ")
    payment_method = input("Enter payment method: ")

    try:
        amount = int(amount)
        house_id = int(house_id)
        payment = Payments.create(tenant_number, payment_code, amount, house_id, house_name, payment_date, payment_method)
        print(f"Payment with ID {payment.id} made successfully.")
    except ValueError:
        print("Amount and house ID must be numbers.")
    except Exception as e:
        print(f"Error: {e}")

def list_payments():
    payments = Payments.get_all_with_tenants()
    if payments:
        for payment in payments:
            print(f"Payment ID: {payment.id}, Tenant Name: {payment.tenant_name}, Phone Number: {payment.phone_number}, Amount: {payment.amount}, Date: {payment.payment_date}, Method: {payment.payment_method}")
    else:
        print("No payments found.")

def evict_tenant():
    tenant_id = input("Enter tenant ID to evict: ")
    try:
        tenant_id = int(tenant_id)
        tenant = Tenants.all.get(tenant_id)
        if tenant:
            tenant.delete()
            print(f"Tenant with ID {tenant_id} evicted successfully.")
        else:
            print(f"No tenant found with ID {tenant_id}.")
    except ValueError:
        print("Tenant ID must be a number.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
