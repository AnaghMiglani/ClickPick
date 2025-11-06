# ClickPick API Documentation

**Version:** 1.0  
**Base URL:** `http://127.0.0.1:8000`  
**Framework:** Django REST Framework 3.14.0  
**Authentication:** JWT (SimpleJWT)  
**Django Version:** 5.0  

---

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Authentication Endpoints](#authentication-endpoints)
4. [Stationery Endpoints](#stationery-endpoints)
5. [Admin Panel](#admin-panel)
6. [Error Handling](#error-handling)
7. [Models & Data Schema](#models--data-schema)
8. [File Upload Specifications](#file-upload-specifications)

---

## Overview

ClickPick is a stationery ordering and printing service platform with a Django REST API backend and Flutter mobile frontend. The API handles user authentication, stationery item orders, and document printing services.

### Tech Stack

**Backend:**
- Django 5.0
- Django REST Framework 3.14.0
- djangorestframework-simplejwt 5.3.1
- SQLite (development)
- Python 3.10+

**Key Features:**
- JWT-based authentication with token rotation
- File upload and processing (PDF, DOCX, images)
- PDF manipulation (watermarking, conversion, cost calculation)
- Order and printout management
- Admin reporting system

---

## Authentication

### Authentication Method
The API uses **JWT (JSON Web Tokens)** for authentication via `djangorestframework-simplejwt`.

### Token Configuration
- **Access Token Lifetime:** 30 days
- **Refresh Token Lifetime:** 30 days
- **Token Rotation:** Enabled (new refresh token on each refresh)
- **Blacklisting:** Enabled (logout invalidates refresh tokens)

### Using Tokens

Include the access token in the `Authorization` header for protected endpoints:

```http
Authorization: Bearer <access_token>
```

### Token Claims
- **User ID Field:** `email`
- **User ID Claim:** `email`
- **Algorithm:** HS256

---

## Authentication Endpoints

All authentication endpoints are under `/auth/` prefix.

### 1. User Registration

**Endpoint:** `POST /auth/register/`  
**Authentication:** Not required  
**Content-Type:** `application/json`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "name": "John Doe",
  "number": "9876543210",
  "role": "STUDENT"
}
```

**Field Specifications:**
- `email` (string, required, unique, max 32 chars): User's email address (used for login)
- `password` (string, required): Plain text password (will be hashed)
- `name` (string, required, max 50 chars): User's full name
- `number` (string, required, max 10 chars): Phone number
- `role` (string, required): User role - one of `"ADMIN"`, `"STAFF"`, `"STUDENT"`

**Success Response (201 Created):**
```json
{
  "message": "User Created Successfully"
}
```

**Error Response (400 Bad Request):**
```json
{
  "email": ["user with this email already exists."],
  "password": ["This field may not be blank."]
}
```

**Notes:**
- Password is automatically hashed using Django's `set_password()` method
- Email is case-sensitive and must be unique
- After registration, user must login to obtain tokens

---

### 2. User Login

**Endpoint:** `POST /auth/login/`  
**Authentication:** Not required  
**Content-Type:** `application/json`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Success Response (200 OK):**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Response (401 Unauthorized):**
```json
{
  "error": "Invalid credentials"
}
```

**Notes:**
- Returns both access and refresh tokens
- User is also logged into Django session (for potential admin panel access)
- Tokens expire after 30 days

---

### 3. Token Refresh

**Endpoint:** `POST /auth/token/refresh/`  
**Authentication:** Not required (but needs refresh token)  
**Content-Type:** `application/json`

**Request Body:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Success Response (200 OK):**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Notes:**
- Refresh token rotation is enabled, so a new refresh token is also returned
- Old refresh token is blacklisted after use

---

### 4. User Logout

**Endpoint:** `POST /auth/logout/`  
**Authentication:** Not required (but needs refresh token)  
**Content-Type:** `application/json`

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Success Response (200 OK):**
```json
{
  "message": "Logout successful"
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Refresh token is required"
}
```

or

```json
{
  "error": "Invalid refresh token"
}
```

**Notes:**
- Blacklists the provided refresh token, preventing further use
- Access token remains valid until expiration (cannot be blacklisted)

---

### 5. Get User Details

**Endpoint:** `GET /auth/user-details/`  
**Authentication:** Required (JWT)  
**Content-Type:** `application/json`

**Request Headers:**
```http
Authorization: Bearer <access_token>
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "John Doe",
  "number": "9876543210",
  "role": "STUDENT"
}
```

**Notes:**
- Returns details of the currently authenticated user
- Sensitive fields are removed: `password`, `groups`, `user_permissions`, `is_superuser`, `is_staff`, `is_active`, `last_login`, `date_joined`

---

## Stationery Endpoints

All stationery endpoints are under `/stationery/` prefix and require authentication.

### 1. Get Item List

**Endpoint:** `GET /stationery/item-list/`  
**Authentication:** Required (JWT)

**Request Headers:**
```http
Authorization: Bearer <access_token>
```

**Success Response (200 OK):**
```json
[
  {
    "id": 1,
    "item": "RING_FILE",
    "price": "50.00",
    "in_stock": true,
    "display_image": "http://127.0.0.1:8000/media/stationery/display-images/ring_file.jpg"
  },
  {
    "id": 2,
    "item": "PEN",
    "price": "10.00",
    "in_stock": true,
    "display_image": "http://127.0.0.1:8000/media/stationery/display-images/pen.jpg"
  }
]
```

**Notes:**
- Returns all available stationery items
- `display_image` is a full URL to the image file

---

### 2. Get Active Orders

**Endpoint:** `GET /stationery/active-orders/`  
**Authentication:** Required (JWT)

**Request Headers:**
```http
Authorization: Bearer <access_token>
```

**Success Response (200 OK):**
```json
[
  {
    "order_id": 1,
    "user": 5,
    "item": 1,
    "item_name": "RING_FILE",
    "item_display_image": "http://127.0.0.1:8000/media/stationery/display-images/ring_file.jpg",
    "quantity": 2,
    "cost": "100.00",
    "custom_message": "Please deliver to room 305",
    "order_time": "2025-11-07T10:30:00+05:30"
  }
]
```

**Notes:**
- Returns only the authenticated user's active orders
- Response includes enriched data: `item_name` and `item_display_image`
- Orders are still pending/being processed

---

### 3. Get Past Orders

**Endpoint:** `GET /stationery/past-orders/`  
**Authentication:** Required (JWT)

**Request Headers:**
```http
Authorization: Bearer <access_token>
```

**Success Response (200 OK):**
```json
[
  {
    "order_id": "ORD0001",
    "user": 5,
    "item": 2,
    "item_name": "PEN",
    "item_display_image": "http://127.0.0.1:8000/media/stationery/display-images/pen.jpg",
    "quantity": 5,
    "cost": "50.00",
    "custom_message": "",
    "order_time": "2025-11-05T14:20:00+05:30"
  }
]
```

**Notes:**
- Returns completed/delivered orders for the authenticated user
- `order_id` is a string (7 characters) for past orders

---

### 4. Get Active Printouts

**Endpoint:** `GET /stationery/active-printouts/`  
**Authentication:** Required (JWT)

**Request Headers:**
```http
Authorization: Bearer <access_token>
```

**Success Response (200 OK):**
```json
[
  {
    "order_id": 1,
    "user": 5,
    "coloured_pages": "2,5",
    "black_and_white_pages": "1-4,6-10",
    "print_on_one_side": true,
    "cost": "78.00",
    "custom_message": "Urgent - needed by 3 PM",
    "order_time": "2025-11-07T11:00:00+05:30",
    "file": "http://127.0.0.1:8000/media/stationery/print-outs/document_20251107.pdf"
  }
]
```

**Notes:**
- Returns authenticated user's active print orders
- `coloured_pages` and `black_and_white_pages` are comma-separated page numbers/ranges
- `file` is a full URL to the uploaded document

---

### 5. Get Past Printouts

**Endpoint:** `GET /stationery/past-printouts/`  
**Authentication:** Required (JWT)

**Request Headers:**
```http
Authorization: Bearer <access_token>
```

**Success Response (200 OK):**
```json
[
  {
    "order_id": "PRT0001",
    "user": 5,
    "coloured_pages": "",
    "black_and_white_pages": "1-15",
    "cost": "30.00",
    "custom_message": "",
    "order_time": "2025-11-06T09:15:00+05:30",
    "file": "http://127.0.0.1:8000/media/stationery/print-outs/report_20251106.pdf"
  }
]
```

**Notes:**
- Returns completed print orders for the authenticated user
- `order_id` is a string (7 characters) for past printouts

---

### 6. Create Order(s)

**Endpoint:** `POST /stationery/create-order/`  
**Authentication:** Required (JWT)  
**Content-Type:** `application/json`

**Request Headers:**
```http
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "orders": [
    {
      "item": "RING_FILE",
      "quantity": 2,
      "cost": 100.00,
      "custom_message": "Please deliver to room 305"
    },
    {
      "item": "PEN",
      "quantity": 3,
      "cost": 30.00,
      "custom_message": ""
    }
  ]
}
```

**Field Specifications:**
- `orders` (array, required): List of order objects
  - `item` (string, required): Item name (must match existing `Items.item` field)
  - `quantity` (integer, required): Number of items to order
  - `cost` (number, required): Total cost for this order line
  - `custom_message` (string, optional): Special instructions or delivery notes

**Success Response (200 OK):**
```json
{
  "message": "Orders Created Successfully"
}
```

**Error Response (400 Bad Request):**
```json
{
  "message": "Order Creation Failed"
}
```

**Notes:**
- Can create multiple orders in a single request
- Item name must exactly match an existing item in the database
- `cost` should be calculated on the client side (quantity × item price)
- User is automatically associated with the order

---

### 7. Create Printout(s)

**Endpoint:** `POST /stationery/create-printout/`  
**Authentication:** Required (JWT)  
**Content-Type:** `multipart/form-data`

**Request Headers:**
```http
Authorization: Bearer <access_token>
```

**Form Data (for multiple files):**
```
files: [file1.pdf, file2.docx]  (array of files)
pages: ["1-3,5", "1-10"]  (array - black & white pages for each file)
colouredpages: ["2", ""]  (array - coloured pages for each file)
costs: ["40.00", "25.00"]  (array - cost for each file)
print_on_one_side_list: ["True", "False"]  (array - boolean strings)
custom_messages: ["Urgent", ""]  (array - messages for each file)
```

**Field Specifications:**
- `files[]` (file array, required): PDF or DOCX files to print
- `pages[]` (string array, required): Black & white page ranges (e.g., "1-3,5,7-10")
- `colouredpages[]` (string array, required): Coloured page numbers/ranges (can be empty string)
- `costs[]` (number array, required): Total cost for each printout
- `print_on_one_side_list[]` (string array, required): "True" or "False" for each file
- `custom_messages[]` (string array, optional): Special instructions for each file

**Important:** All arrays must have the same length (one entry per file).

**Success Response (201 Created):**
```json
{
  "message": "Printout Orders Created Successfully"
}
```

**Error Response (400 Bad Request):**
```json
{
  "message": "Printout Order Creation Failed",
  "errors": {
    "file": ["The submitted file is empty."]
  }
}
```

or

```json
{
  "error": "Index out of range - array mismatch"
}
```

**Notes:**
- Files are saved to `media/stationery/print-outs/`
- Filename is auto-generated using utility function
- Use the `/stationery/calculate-cost/` endpoint first to get accurate costs

---

### 8. Calculate Printout Cost

**Endpoint:** `POST /stationery/calculate-cost/`  
**Authentication:** Not explicitly required (but recommended)  
**Content-Type:** `multipart/form-data`

**Form Data:**
```
files: [file1.pdf, file2.pdf]  (array of files)
pages: ["1-10", "1-5"]  (array - pages to print in B&W)
colouredpages: ["2,5", ""]  (array - pages to print in colour)
```

**Pricing Logic:**
- **Black pages (with significant black content):** ₹5.00 per page
- **Non-black pages (minimal black content):** ₹2.00 per page
- **Coloured pages:** ₹10.00 per page

**Success Response (200 OK):**
```json
{
  "cost": 78.0
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Invalid file type. Only pdf and docx accepted"
}
```

or

```json
{
  "error": "Failed to convert DOCX to PDF"
}
```

**Process:**
1. Files are temporarily saved to `media/temp_files/`
2. DOCX files are converted to PDF using `python-docx` and custom converter
3. PDF pages are analyzed using PyMuPDF for black content detection
4. Cost is calculated based on page analysis
5. Temporary files are deleted
6. Total cost is returned

**Notes:**
- Supported formats: PDF, DOCX
- Page ranges use format: "1-3,5,7-10" (ranges and individual pages)
- Black content detection uses pixel analysis threshold
- Files are NOT saved permanently (this is just cost estimation)

---

### 9. Generate First Page

**Endpoint:** `POST /stationery/generate-firstpage/`  
**Authentication:** Not required (commented out in code)  
**Content-Type:** `application/json`

**Request Body:**
```json
{
  "subject_name": "Data Structures and Algorithms",
  "subject_code": "CSE-301",
  "faculty_name": "Dr. Rajesh Kumar",
  "student_name": "Arpan Sharma",
  "faculty_designation": "Associate Professor",
  "roll_number": "21/CSE/045",
  "semester": "5th Semester",
  "group": "A"
}
```

**Success Response (200 OK):**
- **Content-Type:** `application/pdf`
- **Content-Disposition:** `attachment; filename="converted.pdf"`
- Returns a PDF file as binary data

**Error Response (400 Bad Request):**
```json
{
  "error": "Error message describing what went wrong"
}
```

**Process:**
1. Creates a DOCX file using `python-docx` with provided data
2. Inserts college logo (`maitlogomain.png`)
3. Formats the first page with all fields
4. Converts DOCX to PDF
5. Returns PDF as downloadable file
6. Deletes temporary DOCX file

**Notes:**
- This generates a standard college assignment/project first page
- The logo image must exist in the assets folder
- Temporary file is created in system temp directory
- PDF is returned directly (not saved on server)

---

### 10. Convert Images to PDF

**Endpoint:** `POST /stationery/img-to-pdf/`  
**Authentication:** Not required  
**Content-Type:** `multipart/form-data`

**Form Data:**
```
images: [image1.jpg, image2.png, image3.jpg]  (array of image files)
pics_per_page: 2  (optional, default: 2)
```

**Field Specifications:**
- `images[]` (file array, required): Image files (JPG, PNG, etc.)
- `pics_per_page` (integer, optional, default: 2): Number of images per PDF page (1-4 recommended)

**Success Response (200 OK):**
- **Content-Type:** `application/pdf`
- **Content-Disposition:** `attachment; filename="output.pdf"`
- Returns a PDF file as binary data

**Error Response (400 Bad Request):**
```json
{
  "error": "No images provided"
}
```

**Process:**
1. Images are temporarily saved to a temp directory
2. `ImageToPdfConverter` class processes images
3. Images are arranged according to `pics_per_page`
4. Single PDF is generated
5. Temporary files are automatically deleted
6. PDF is returned as downloadable file

**Notes:**
- Useful for converting multiple images into a single PDF document
- Images are arranged in grid format on each page
- Temporary directory is created and cleaned up automatically

---

## Admin Panel

### Access
- **URL:** `http://127.0.0.1:8000/admin/`
- **Requirements:** User must have `is_staff=True` or `is_superuser=True`
- **Create Superuser:** `python manage.py createsuperuser`

### Admin-Only Endpoints

These endpoints are accessible only through the Django admin panel or by admin users.

#### 1. Mark Active Order as Past

**Endpoint:** `GET/POST /stationery/delete_active_order/<int:order_id>/`  
**Authentication:** Admin only  
**Access:** Via admin panel "Mark as Past" button

**Process:**
1. Retrieves ActiveOrder by `order_id`
2. Creates new PastOrder with same data
3. Deletes ActiveOrder
4. Redirects to `/admin/stationery/activeorders/`

---

#### 2. Mark Active Printout as Past

**Endpoint:** `GET/POST /stationery/delete_active_printout/<int:order_id>/`  
**Authentication:** Admin only  
**Access:** Via admin panel "Mark as Past" button

**Process:**
1. Retrieves ActivePrintOut by `order_id`
2. Creates new PastPrintOut with same data (including file)
3. Deletes ActivePrintOut
4. Redirects to `/admin/stationery/activeprintouts/`

---

#### 3. Generate Order Reports

**Daily Report:**  
`GET /stationery/order-reports/daily/`

**Weekly Report:**  
`GET /stationery/order-reports/weekly/`

**Monthly Report:**  
`GET /stationery/order-reports/monthly/`

**Response:** HTML page with filtered order records

**Date Ranges:**
- **Daily:** Today's date only
- **Weekly:** Monday to Sunday of current week
- **Monthly:** 1st to last day of current month

---

#### 4. Generate Custom Order Report

**Endpoint:** `GET/POST /stationery/generate_custom_order_report/`  
**Authentication:** Admin only

**GET Request:** Returns HTML form to select date range

**POST Request Body:**
```
start_date_time: 2025-01-01T00:00
end_date_time: 2025-01-31T23:59
```

**Response:** HTML page with filtered records between specified dates

---

#### 5. Generate Printout Reports

**Daily Report:**  
`GET /stationery/printout-reports/daily/`

**Weekly Report:**  
`GET /stationery/printout-reports/weekly/`

**Monthly Report:**  
`GET /stationery/printout-reports/monthly/`

**Response:** HTML page with filtered printout records

---

#### 6. Generate Custom Printout Report

**Endpoint:** `GET/POST /stationery/generate_custom_printout_report/`  
**Authentication:** Admin only

**GET Request:** Returns HTML form to select date range

**POST Request Body:**
```
start_date_time: 2025-01-01T00:00
end_date_time: 2025-01-31T23:59
```

**Response:** HTML page with filtered records between specified dates

---

## Error Handling

### Standard HTTP Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful GET request or operation |
| 201 | Created | Resource successfully created |
| 400 | Bad Request | Invalid request data or validation error |
| 401 | Unauthorized | Missing or invalid authentication token |
| 403 | Forbidden | Valid token but insufficient permissions |
| 404 | Not Found | Resource does not exist |
| 500 | Internal Server Error | Server-side error |

### Error Response Format

```json
{
  "error": "Error message describing the issue"
}
```

or with validation errors:

```json
{
  "field_name": ["Error message for this field"],
  "another_field": ["Error message", "Another error message"]
}
```

### Common Errors

**Invalid Token:**
```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```

**Missing Authentication:**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**Permission Denied:**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

## Models & Data Schema

### User Model

**Table:** `users`

```python
{
  "id": Integer (Primary Key),
  "email": String(32) [Unique, Indexed],
  "password": String (Hashed),
  "name": String(50),
  "number": String(10),
  "role": Enum("ADMIN", "STAFF", "STUDENT"),
  "is_staff": Boolean,
  "is_superuser": Boolean,
  "is_active": Boolean,
  "last_login": DateTime,
  "date_joined": DateTime,
  "groups": ManyToMany,
  "user_permissions": ManyToMany
}
```

**Roles:**
- `ADMIN`: Full admin panel access
- `STAFF`: Staff user with potential admin access
- `STUDENT`: Regular user (API access only)

---

### Items Model

**Table:** `stationery_items`

```python
{
  "id": Integer (Primary Key),
  "item": String(25) [Item name],
  "price": Decimal(6, 2),
  "in_stock": Boolean,
  "display_image": ImageField
}
```

---

### ActiveOrders Model

**Table:** `stationery_active_orders`

```python
{
  "order_id": Integer (Primary Key, Auto),
  "user": ForeignKey(User),
  "item": ForeignKey(Items),
  "quantity": PositiveInteger,
  "cost": Decimal(6, 2),
  "custom_message": Text,
  "order_time": DateTime (Auto)
}
```

---

### PastOrders Model

**Table:** `stationery_past_orders`

```python
{
  "order_id": String(7) [Unique, Indexed],
  "user": ForeignKey(User),
  "item": ForeignKey(Items),
  "quantity": PositiveInteger,
  "cost": Decimal(6, 2),
  "custom_message": Text,
  "order_time": DateTime
}
```

---

### ActivePrintOuts Model

**Table:** `stationery_active_printouts`

```python
{
  "order_id": Integer (Primary Key, Auto),
  "user": ForeignKey(User),
  "coloured_pages": String(20),
  "black_and_white_pages": String(20),
  "print_on_one_side": Boolean,
  "cost": Decimal(6, 2),
  "custom_message": Text,
  "order_time": DateTime (Auto),
  "file": FileField
}
```

---

### PastPrintOuts Model

**Table:** `stationery_past_printouts`

```python
{
  "order_id": String(7) [Unique, Indexed],
  "user": ForeignKey(User),
  "coloured_pages": String(20),
  "black_and_white_pages": String(20),
  "cost": Decimal(6, 2),
  "custom_message": Text,
  "order_time": DateTime,
  "file": FileField
}
```

---

## File Upload Specifications

### Supported File Types

| Endpoint | Supported Formats | Max Size | Notes |
|----------|------------------|----------|-------|
| `/stationery/create-printout/` | PDF, DOCX | Not specified | Files stored permanently |
| `/stationery/calculate-cost/` | PDF, DOCX | Not specified | Files deleted after processing |
| `/stationery/img-to-pdf/` | JPG, PNG, BMP, GIF | Not specified | Files deleted after processing |

### File Storage Locations

- **Printout files:** `media/stationery/print-outs/`
- **Item display images:** `media/stationery/display-images/`
- **Temporary files:** `media/temp_files/` (auto-deleted)
- **Temporary first pages:** `media/temp_first_pages/`

### File Naming

Files are automatically renamed using utility functions to avoid conflicts:
- Format: `{original_name}_{timestamp}.{extension}`
- Special characters are handled
- Duplicates are prevented

---

## Database

### Configuration

- **Engine:** SQLite3 (development)
- **Database File:** `backend/aman.sqlite3`
- **Location:** Local filesystem
- **Migrations:** Django ORM migrations

### Running Migrations

```bash
python manage.py migrate
```

### Creating Tables

All models are automatically migrated. To create a fresh database:

```bash
python manage.py migrate
python manage.py createsuperuser
```

---

## CORS Configuration

**Current Setting:** `CORS_ALLOW_ALL_ORIGINS = True`

**Note:** This is configured for development. In production, set specific allowed origins:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://yourdomain.com"
]
```

---

## Rate Limiting

**Current Status:** Not implemented

**Recommendation:** Add rate limiting for production using `django-ratelimit` or similar.

---

## Example Usage

### Complete Authentication Flow

```python
import requests

BASE_URL = "http://127.0.0.1:8000"

# 1. Register
register_data = {
    "email": "student@example.com",
    "password": "securepass123",
    "name": "John Doe",
    "number": "9876543210",
    "role": "STUDENT"
}
response = requests.post(f"{BASE_URL}/auth/register/", json=register_data)
print(response.json())  # {"message": "User Created Successfully"}

# 2. Login
login_data = {
    "email": "student@example.com",
    "password": "securepass123"
}
response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
tokens = response.json()
access_token = tokens["access"]
refresh_token = tokens["refresh"]

# 3. Get user details
headers = {"Authorization": f"Bearer {access_token}"}
response = requests.get(f"{BASE_URL}/auth/user-details/", headers=headers)
print(response.json())

# 4. Create an order
order_data = {
    "orders": [
        {
            "item": "PEN",
            "quantity": 5,
            "cost": 50.00,
            "custom_message": "Blue pens only"
        }
    ]
}
response = requests.post(f"{BASE_URL}/stationery/create-order/", 
                        json=order_data, headers=headers)
print(response.json())

# 5. Logout
logout_data = {"refresh_token": refresh_token}
response = requests.post(f"{BASE_URL}/auth/logout/", json=logout_data)
print(response.json())
```

### Creating a Printout Order

```python
import requests

BASE_URL = "http://127.0.0.1:8000"
access_token = "your_access_token"

# 1. Calculate cost first
files = [
    ('files', open('document.pdf', 'rb')),
    ('files', open('report.pdf', 'rb'))
]
data = {
    'pages': ['1-10', '1-5'],
    'colouredpages': ['2,5', '']
}
response = requests.post(f"{BASE_URL}/stationery/calculate-cost/", 
                        files=files, data=data)
cost = response.json()["cost"]
print(f"Total cost: ₹{cost}")

# 2. Create the printout order
files = [
    ('files', open('document.pdf', 'rb')),
    ('files', open('report.pdf', 'rb'))
]
data = {
    'pages': ['1-10', '1-5'],
    'colouredpages': ['2,5', ''],
    'costs': [cost * 0.7, cost * 0.3],  # Split cost
    'print_on_one_side_list': ['True', 'False'],
    'custom_messages': ['Urgent', 'Regular delivery']
}
headers = {"Authorization": f"Bearer {access_token}"}
response = requests.post(f"{BASE_URL}/stationery/create-printout/", 
                        files=files, data=data, headers=headers)
print(response.json())
```

---

## Testing

### Available Test Endpoints (DEBUG mode only)

**Base:** `/testing/` (only available when `DEBUG=True`)

Check `backend/testing/urls.py` and `backend/testing/views.py` for available test endpoints.

---

## Environment Variables

Required environment variables (defined in `.env` file):

```env
SECRET_KEY=your-secret-key
ALLOWED_HOST_1=127.0.0.1
ALLOWED_HOST_2=localhost
ALLOWED_HOST_3=0.0.0.0

# Email configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Database (optional - for MySQL)
# DATABASE_ENGINE=django.db.backends.mysql
# DATABASE_NAME=clickpick
# DATABASE_USER=root
# DATABASE_PASSWORD=password
# DATABASE_HOST=localhost
# DATABASE_PORT=3306
```

---

## Deployment Checklist

Before deploying to production:

1. ✅ Set `DEBUG = False` in settings.py
2. ✅ Configure specific `ALLOWED_HOSTS`
3. ✅ Set specific `CORS_ALLOWED_ORIGINS` (remove `CORS_ALLOW_ALL_ORIGINS`)
4. ✅ Use PostgreSQL/MySQL instead of SQLite
5. ✅ Set strong `SECRET_KEY` (keep it secret!)
6. ✅ Configure production email backend
7. ✅ Set up proper media/static file serving (use CDN/S3)
8. ✅ Enable HTTPS
9. ✅ Add rate limiting
10. ✅ Set up logging and monitoring
11. ✅ Configure CSRF protection
12. ✅ Review and set appropriate JWT token lifetimes
13. ✅ Set up automated backups
14. ✅ Review file upload size limits

---

## Support & Contact

**Project:** ClickPick  
**Repository:** github.com/Hardikdhull/ClickPick  
**Framework:** Django 5.0 + Django REST Framework  
**License:** Not specified  

---

## Changelog

### Version 1.0 (Current)
- JWT authentication with token rotation
- User registration and management
- Stationery item ordering
- Document printing services
- PDF/DOCX processing
- Image to PDF conversion
- Admin reporting system
- Cost calculation for printouts

---

**Last Updated:** November 7, 2025
