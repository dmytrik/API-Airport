# API-Airport service

Welcome to **Airport Management System** — This is a Django-Rest-Framework project that manages airport operations,
including flights, routes, tickets, and crew management.
It utilizes PostgreSQL for the database and Redis for caching.
The system is containerized using Docker for ease of setup and deployment.
**User for testing:** email - airport@admin.com, password - airportadmin1234

---

## Features

- **Airports Management**: Manage airport information like names and locations.
- **Flight Scheduling**: Create and manage flights with details like departure/arrival times, routes, and airplanes.
- **Ticket Booking**: Assign tickets to passengers with validation for seat availability.
- **Crew Management**: Manage crew members working on flights.
- **Data Validation**: Includes validations like checking seat availability and ensuring that the source and destination airports are different.

---

## 🗂️ Database Structure

Here's an overview of the project's database design:

<img width="1184" alt="Screenshot 2024-12-01 at 20 19 36" src="https://github.com/user-attachments/assets/2119eea7-46cd-4fb5-bc13-76234cef44db">
---

## Models

### 1. **Order**
Represents a customer's purchase of tickets. Automatically tracks creation time.

**Fields:**
- `created_at` Timestamp of order creation
- `user` Foreign key to the user who made the order.

---

### 2. **Ticket**
Defines a seat and row on a specific flight.

**Fields:**
- `row` Row number.
- `seat` Seat number.
- `flight` Foreign key to the associated flight.
- `order` Foreign key to the associated order.

**Constraints:**
- Ensures unique tickets per seat, row, and flight.
- Validates seat and row ranges within airplane capacity.


---

### 3. **Flight**
Represents a flight with assigned routes, airplanes, and crew.

**Fields:**
- `route` Foreign key to the flight's route.
- `airplane` Foreign key to the assigned airplane.
- `departure_time` Date and time of departure.
- `arrival_time` Date and time of arrival.
- `crew` Many-to-many relationship with crew members.

---

### 4. **Route**
Defines a journey between two airports.

**Fields:**
- `source` Foreign key to the source airport.
- `destination` Foreign key to the destination airport.
- `distance` Distance in kilometers.

---

### 5. **Airport**
Stores details of an airport.

**Fields:**
- `name` Name of the airport.
- `closest_big_city` Closest major city.

---

### 6. **Crew**
Represents individuals assigned to flights.

**Fields:**
- `first_name` Crew member's first name.
- `last_name` Crew member's last name.
- `full_name` Property for full name.

---

### 7. **Airplane**
Manages airplane details.

**Fields:**
- `name` Name of the airplane.
- `rows` Number of seat rows.
- `seats_in_row` Number of seats per row.
- `airplane_type` Foreign key to the airplane type.

---

### 8. **AirplaneType**
Categorizes airplanes into types.

**Fields:**
- `name` Name of the airplane type.

---

## 🚀 Installation

Follow these steps to set up the project locally:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/dmytrik/all_for_rest.git

2. **Create a Virtual Environment:**
   ```bash
   python -m venv env
   source env/bin/activate       # Linux/Mac
   env\Scripts\activate          # Windows 

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt

4. **Run Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate

5. **Create a Superuser:**
   ```bash
   python manage.py createsuperuser

6. **Create env file:**
   - `ENVIRONMENT` local
   - `SECRET_KEY`

7. **Install the redis and run:**
   [Install Redis](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/)

8. **Initial Data Load:**
   ```bash
   python manage.py loaddata airport_initial_data.json

9. **Start the Development Server:**
   ```bash
   python manage.py runserver


Follow these steps to set up the project in the Docker:

1. **Install Docker:**
   [Install Docker](https://www.docker.com/get-started)

2. **Create env file:**
   - `ENVIRONMENT` local
   - `POSTGRES_PASSWORD`
   - `POSTGRES_USER`
   - `POSTGRES_DB`
   - `POSTGRES_HOST`
   - `POSTGRES_PORT`
   - `SECRET_KEY`

3. **Run container:**
   ```bash
   docker-compose up --build
