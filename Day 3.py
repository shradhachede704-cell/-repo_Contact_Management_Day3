import os
import json
import logging

logging.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    level=logging.INFO
)


class ContactError(Exception):
    """Base exception for Contact Manager errors."""
    pass

class ContactNotFoundError(ContactError):
    """Raised when a specified contact does not exist."""
    pass

class InvalidContactDataError(ContactError):
    """Raised when contact fields violate format parameters."""
    pass

class DatabaseCorruptedError(ContactError):
    """Raised when JSON parsing completely fails due to syntax corruption."""
    pass

class ContactManager:
    def init(self, db_filename="contacts.json"):
        self.db_filename = db_filename
        self._initialize_db()

    def _initialize_db(self):
        """Gracefully handles missing or corrupted database configurations."""
        if not os.path.exists(self.db_filename):
            try:
                with open(self.db_filename, "w") as file:
                    json.dump([], file, indent=4)
                logging.info(f"Database file '{self.db_filename}' initialized successfully.")
            except IOError as e:
                logging.critical(f"Failed to create file system asset: {e}")
                print(f"Critical Error: Could not setup storage file ({e}).")

    def _load_contacts(self):
        """Loads contacts via 'try-except-else-finally' construct."""
        file_handle = None
        try:
            file_handle = open(self.db_filename, "r")
            data = json.load(file_handle)
            return data
        except FileNotFoundError:
            logging.warning(f"'{self.db_filename}' missing during load lifecycle. Re-initializing.")
            self._initialize_db()
            return []
        except json.JSONDecodeError as e:
            logging.error(f"Database file corruption event triggered: {e}")
            raise DatabaseCorruptedError("The storage file is corrupted and cannot be parsed.")
        else:
            logging.debug("Database loaded successfully with zero execution anomalies.")
        finally:
            if file_handle:
                file_handle.close()

    def _save_contacts(self, contacts):
        """Saves internal collection state to the external json file structure."""
        try:
            with open(self.db_filename, "w") as file:
                json.dump(contacts, file, indent=4)
        except IOError as e:
            logging.error(f"I/O execution blocked database modification: {e}")
            raise ContactError(f"Failed to commit adjustments to storage: {e}")

    def add_contact(self, name, phone, email):
        """Validates incoming properties and tracks data ingestion errors."""
        name = name.strip()
        phone = phone.strip()
        email = email.strip()

        if not name or not phone:
            raise InvalidContactDataError("Contact operation dropped: Name and Phone cannot be blank.")

        try:
            contacts = self._load_contacts()
        except DatabaseCorruptedError:
            print("️ Automated recovery: Overwriting the corrupted data store with a blank array.")
            logging.warning("Overwriting corrupted data store following manual structural override choice.")
            contacts = []

        for contact in contacts:
            if contact['name'].lower() == name.lower():
                raise ContactError(f"A contact named '{name}' already exists.")
        new_contact = {"name": name, "phone": phone, "email": email}
        contacts.append(new_contact)
        
        self._save_contacts(contacts)
        logging.info(f"Successfully added record element: '{name}'.")
        print(f"Contact '{name}' recorded successfully.")

    def list_contacts(self):
        """Retrieves and displays saved records."""
        try:
            contacts = self._load_contacts()
        except DatabaseCorruptedError as e:
            print(f"Operation Failed: {e} Repair or delete '{self.db_filename}'.")
            return

        if not contacts:
            print("ℹ️ No saved contacts available.")
            return

        print("\n=== Registered Directory Listing ===")
        for idx, contact in enumerate(contacts, 1):
            print(f"{idx}. Name: {contact['name']} | Phone: {contact['phone']} | Email: {contact['email']}")
        print("====================================")

    def delete_contact(self, name):
        """Locates specific items and fires customized NotFound flags when missing."""
        name = name.strip()
        try:
            contacts = self._load_contacts()
        except DatabaseCorruptedError as e:
            print(f"Operation Failed: {e}")
            return

        initial_count = len(contacts)
        contacts = [c for c in contacts if c['name'].lower() != name.lower()]

        if len(contacts) == initial_count:
            raise ContactNotFoundError(f"Delete targeted object mismatch: '{name}' not found.")

        self._save_contacts(contacts)
        logging.info(f"Successfully evicted contact record: '{name}'.")
        print(f"Contact '{name}' deleted successfully.")



def main():
    manager = ContactManager()
    print(" Welcome to Intermediate Contact Management Tool (Day 3 Edition)")
    
    while True:
        print("\n--- CLI Menu Options ---")
        print("1. Add Contact")
        print("2. List All Contacts")
        print("3. Delete Contact")
        print("4. Exit Application")
        
        choice = input("Select an option (1-4): ").strip()
        
        try:
            if choice == "1":
                name = input("Enter contact name: ")
                phone = input("Enter phone number: ")
                email = input("Enter email address: ")
                manager.add_contact(name, phone, email)
                
            elif choice == "2":
                manager.list_contacts()
                
            elif choice == "3":
                name = input("Enter name of the contact to delete: ")
                manager.delete_contact(name)
                
            elif choice == "4":
                print(" Terminating application instance loop cleanly. Goodbye!")
                logging.info("Application session terminated normally via structural user choice request.")
                break
                
            else:
                print("️ Invalid Menu Selection. Please key in a numerical selection matching 1-4.")
                logging.warning(f"User entered anomalous root-menu selection: '{choice}'")
                
        except ContactNotFoundError as e:
            print(f" Item Warning: {e}")
            logging.warning(f"Target object not resolved: {e}")
        except InvalidContactDataError as e:
            print(f" Validation Warning: {e}")
            logging.warning(f"Inbound parameters configuration invalid: {e}")
        except ContactError as e:
            print(f"Application Error: {e}")
            logging.error(f"Application operations error instance captured: {e}")
        except Exception as e:
            print(" Unexpected Global Framework Exception occurred! Logged to target app.log tracker.")
            logging.exception(f"Unhandled Runtime Thread Trap Triggered: {e}")

if __name__ == "__main__":
    main()
