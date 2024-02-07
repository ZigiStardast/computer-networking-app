# Humanitarian Aid Donation System

This project is a client-server application for donating money for humanitarian purposes. The application enables users to make donations, register, log in, view the total amount of funds collected, and view transaction history.

## Basic Requirements

- The client connects to the server.
- The server sends a message confirming successful connection and provides options defined below.
- Users can make a donation by providing their personal details (name, surname, address, credit card number, and CVV code (three-digit number), and amount).
- After a successful donation, the user receives a text file containing basic donation details (user's name, surname, address, donation date and time, amount).

### Constraints:

- Allow the server to handle multiple clients simultaneously.
- Implement error handling for network communication and program operation.
- Ensure persistence of data after server shutdown.
- Minimum donation amount is 200 RSD.
- Credit card number format should be xxxx-xxxx-xxxx-xxxx where x is a digit, and CVV is a three-digit number.
- Ensure a unique database of credit card numbers and CVV codes to validate user input.
- Assume users have unlimited funds on their cards.

## Additional Requirement 1 

- Users can view the total amount of funds collected.

### Constraints:

- Ensure persistence of data after server shutdown.

## Additional Requirement 2

- Implement user registration and login to the server.
- Registration includes basic user information such as username, password, name, surname, ID number, credit card number, and email.
- Users log in to the system by entering their username and password.
- Logged-in users can make donations and view the total amount of funds collected.
- Logged-in users can make donations without entering credit card numbers, only the CVV code.

### Constraints:

- Ensure no two users can have the same username.
- Ensure persistence of data after server shutdown.

## Additional Requirement 3

- After logging in, registered users can view the last 10 donations in the format: donor's name and surname, date, time, and amount.

