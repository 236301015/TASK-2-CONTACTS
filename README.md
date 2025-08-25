# Contact Management System

A Python-based Contact Management System with a Tkinter GUI, integrated with MySQL for storing and managing contact information. Users can add, view, search, update, and delete contacts through an intuitive interface.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## Features
- **Add Contact**: Save new contacts with name, contact number, email, and address.
- **View Contacts**: Display all contacts in a sorted table view.
- **Search Contacts**: Search by name, contact number, email, or address with partial matching for addresses.
- **Update Contacts**: Modify existing contact details (name, number, email, or address).
- **Delete Contacts**: Remove contacts by name, number, email, or address.
- **MySQL Integration**: Stores contact data persistently in a MySQL database.
- **User-Friendly GUI**: Built with Tkinter, featuring colorful buttons and clear feedback.
- **Error Handling**: Displays connection status and input validation errors.

## Installation
1. **Prerequisites**:
   - Python 3.x installed on your system.
   - MySQL Server installed and running.
   - Tkinter (included with Python by default).
   - MySQL Connector for Python.

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/236301015/contact-management-system.git
   cd contact-management-system
   ```

3. **Install Dependencies**:
   Install the MySQL Connector for Python:
   ```bash
   pip install mysql-connector-python
   ```

## Database Setup
1. Ensure MySQL Server is running on your system.
2. Update the MySQL connection details in the code:
   - Open `contact_management.py`.
   - In the `isconnected()` function, replace `'your_mysql_username'` and `'your_mysql_password'` with your MySQL username and password.
   ```python
   mydb = mysql.connector.connect(
       host="localhost",
       user="your_mysql_username",
       password="your_mysql_password"
   )
   ```
3. The program automatically creates a database named `Contact` and a table named `contact` with the following schema:
   ```sql
   CREATE TABLE contact (
       name VARCHAR(255),
       number BIGINT UNIQUE,
       email VARCHAR(255),
       address VARCHAR(255)
   );
   ```
   No manual database setup is required unless you need a different configuration.

## Usage
1. Run the program:
   ```bash
   python contact_management.py
   ```
2. The main window will display the connection status and a welcome message.
3. Use the buttons to perform actions:
   - **Add Contact**: Opens a form to enter name, contact number, email, and address.
   - **View Contact**: Displays all contacts in a table, sorted by name.
   - **Search Contact**: Choose to search by name, number, email, or address, and view results in a table.
   - **Update Contact**: Select a field to update and provide current and new values.
   - **Delete Contact**: Select a field to delete a contact by its value.
   - **Exit**: Closes the database connection and exits the application.
4. If the MySQL connection fails, the program will display an error and exit after 3 seconds.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

Please ensure your code follows the project’s style, includes comments, and handles errors appropriately.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
