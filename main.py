import json
import os
from datetime import datetime

# --- Data Models ---

class Patient:
    """Represents a patient in the hospital."""
    def __init__(self, patient_id, name, contact):
        self.patient_id = patient_id
        self.name = name
        self.contact = contact

    def to_dict(self):
        """Converts patient object to a dictionary for JSON serialization."""
        return {
            'patient_id': self.patient_id,
            'name': self.name,
            'contact': self.contact
        }

    @staticmethod
    def from_dict(data):
        """Creates a patient object from a dictionary."""
        return Patient(data['patient_id'], data['name'], data['contact'])

    def __str__(self):
        return f"ID: {self.patient_id}, Name: {self.name}, Contact: {self.contact}"

class Service:
    """Represents a service or item offered by the hospital."""
    def __init__(self, service_id, name, price):
        self.service_id = service_id
        self.name = name
        self.price = price

    def to_dict(self):
        """Converts service object to a dictionary for JSON serialization."""
        return {
            'service_id': self.service_id,
            'name': self.name,
            'price': self.price
        }

    @staticmethod
    def from_dict(data):
        """Creates a service object from a dictionary."""
        return Service(data['service_id'], data['name'], data['price'])

    def __str__(self):
        return f"ID: {self.service_id}, Name: {self.name}, Price: ${self.price:.2f}"

class Bill:
    """Represents a bill for a patient."""
    def __init__(self, bill_id, patient_id, services_rendered, bill_date):
        self.bill_id = bill_id
        self.patient_id = patient_id
        self.services_rendered = services_rendered  # List of Service objects
        self.bill_date = bill_date
        self.total_amount = self.calculate_total()

    def calculate_total(self):
        """Calculates the total amount of the bill."""
        return sum(service.price for service in self.services_rendered)

    def to_dict(self):
        """Converts bill object to a dictionary for JSON serialization."""
        return {
            'bill_id': self.bill_id,
            'patient_id': self.patient_id,
            'services_rendered': [service.to_dict() for service in self.services_rendered],
            'bill_date': self.bill_date,
            'total_amount': self.total_amount
        }

    @staticmethod
    def from_dict(data):
        """Creates a bill object from a dictionary."""
        services = [Service.from_dict(s) for s in data['services_rendered']]
        bill = Bill(data['bill_id'], data['patient_id'], services, data['bill_date'])
        return bill

    def __str__(self):
        bill_details = f"Bill ID: {self.bill_id}\n"
        bill_details += f"Patient ID: {self.patient_id}\n"
        bill_details += f"Date: {self.bill_date}\n"
        bill_details += "Services Rendered:\n"
        for service in self.services_rendered:
            bill_details += f"  - {service.name} (${service.price:.2f})\n"
        bill_details += f"Total Amount: ${self.total_amount:.2f}\n"
        return bill_details

# --- Main System Class ---

class HospitalBillingSystem:
    """Manages all aspects of the hospital billing system."""
    def __init__(self, data_file='hospital_data.json'):
        self.data_file = data_file
        self.patients = {}  # patient_id -> Patient object
        self.services = {}  # service_id -> Service object
        self.bills = {}     # bill_id -> Bill object
        self.next_patient_id = 1
        self.next_service_id = 1
        self.next_bill_id = 1
        self.load_data()

    def load_data(self):
        """Loads data from the JSON file."""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                
                # Load patients
                self.patients = {p['patient_id']: Patient.from_dict(p) for p in data.get('patients', [])}
                
                # Load services
                self.services = {s['service_id']: Service.from_dict(s) for s in data.get('services', [])}
                
                # Load bills
                self.bills = {b['bill_id']: Bill.from_dict(b) for b in data.get('bills', [])}

                # Set next IDs
                self.next_patient_id = max([p_id for p_id in self.patients.keys()] + [1]) + 1
                self.next_service_id = max([s_id for s_id in self.services.keys()] + [1]) + 1
                self.next_bill_id = max([b_id for b_id in self.bills.keys()] + [1]) + 1

        print("Data loaded successfully.")

    def save_data(self):
        """Saves all current data to the JSON file."""
        data = {
            'patients': [p.to_dict() for p in self.patients.values()],
            'services': [s.to_dict() for s in self.services.values()],
            'bills': [b.to_dict() for b in self.bills.values()]
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=4)
        print("Data saved successfully.")

    # --- Patient Management ---
    def add_patient(self, name, contact):
        patient_id = self.next_patient_id
        patient = Patient(patient_id, name, contact)
        self.patients[patient_id] = patient
        self.next_patient_id += 1
        print(f"Patient '{name}' added with ID: {patient_id}")

    def get_patient(self, patient_id):
        return self.patients.get(patient_id)

    def list_patients(self):
        if not self.patients:
            print("No patients registered.")
            return
        for patient in self.patients.values():
            print(patient)

    # --- Service Management ---
    def add_service(self, name, price):
        service_id = self.next_service_id
        service = Service(service_id, name, price)
        self.services[service_id] = service
        self.next_service_id += 1
        print(f"Service '{name}' added with ID: {service_id}")

    def get_service(self, service_id):
        return self.services.get(service_id)

    def list_services(self):
        if not self.services:
            print("No services available.")
            return
        for service in self.services.values():
            print(service)

    # --- Billing ---
    def create_bill(self, patient_id, service_ids):
        if patient_id not in self.patients:
            print(f"Error: Patient with ID {patient_id} not found.")
            return None

        services_to_bill = []
        for s_id in service_ids:
            service = self.get_service(s_id)
            if service:
                services_to_bill.append(service)
            else:
                print(f"Warning: Service with ID {s_id} not found. Skipping.")
        
        if not services_to_bill:
            print("Error: No valid services provided for the bill.")
            return None

        bill_id = self.next_bill_id
        bill_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        bill = Bill(bill_id, patient_id, services_to_bill, bill_date)
        self.bills[bill_id] = bill
        self.next_bill_id += 1
        print(f"Bill created for patient {patient_id} with Bill ID: {bill_id}")
        return bill

    def get_bill(self, bill_id):
        return self.bills.get(bill_id)

    def list_bills(self):
        if not self.bills:
            print("No bills created yet.")
            return
        for bill in self.bills.values():
            print("---------------------------------")
            print(bill)
        print("---------------------------------")

# --- User Interface (Main Loop) ---

def main():
    h_system = HospitalBillingSystem()

    while True:
        print("\n--- Hospital Billing System Menu ---")
        print("1. Add a new patient")
        print("2. List all patients")
        print("3. Add a new service")
        print("4. List all services")
        print("5. Create a new bill")
        print("6. List all bills")
        print("7. Find a patient by ID")
        print("8. Find a bill by ID")
        print("9. Save and Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter patient name: ")
            contact = input("Enter patient contact info: ")
            h_system.add_patient(name, contact)
        
        elif choice == '2':
            h_system.list_patients()
        
        elif choice == '3':
            name = input("Enter service name: ")
            try:
                price = float(input("Enter service price: "))
                h_system.add_service(name, price)
            except ValueError:
                print("Invalid price. Please enter a number.")
        
        elif choice == '4':
            h_system.list_services()
        
        elif choice == '5':
            patient_id = int(input("Enter patient ID for the bill: "))
            
            # Show available services to the user
            print("\nAvailable Services:")
            h_system.list_services()

            service_ids_str = input("Enter a comma-separated list of service IDs to add to the bill: ")
            try:
                service_ids = [int(s.strip()) for s in service_ids_str.split(',')]
                bill = h_system.create_bill(patient_id, service_ids)
                if bill:
                    print("\n--- New Bill Details ---")
                    print(bill)
            except ValueError:
                print("Invalid service ID list. Please enter numbers separated by commas.")

        elif choice == '6':
            h_system.list_bills()

        elif choice == '7':
            try:
                patient_id = int(input("Enter patient ID to find: "))
                patient = h_system.get_patient(patient_id)
                if patient:
                    print("\n--- Patient Found ---")
                    print(patient)
                else:
                    print("Patient not found.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif choice == '8':
            try:
                bill_id = int(input("Enter bill ID to find: "))
                bill = h_system.get_bill(bill_id)
                if bill:
                    print("\n--- Bill Found ---")
                    print(bill)
                else:
                    print("Bill not found.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        elif choice == '9':
            h_system.save_data()
            print("Exiting application. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()