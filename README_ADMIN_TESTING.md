# Admin Panel Testing Guide

## Setup

1. **Start the backend server:**
   ```bash
   cd backend
   python3 app.py
   ```
   
   This will:
   - Initialize the database
   - Create the admin user automatically (if it doesn't exist)
   - Start the server on port 5001

2. **Admin Credentials:**
   - Email: `Admin@kgplaunchpad.in`
   - Password: `IITKGP2026`

## Testing Admin Login

### Using curl:

```bash
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"Admin@kgplaunchpad.in","password":"IITKGP2026"}'
```

Expected response:
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "name": "Admin",
    "email": "Admin@kgplaunchpad.in",
    "role": "admin",
    "is_approved": true
  }
}
```

### Using the test script:

```bash
cd backend
./test_admin_endpoints.sh
```

## Testing Admin Endpoints

After logging in, save the token and use it for authenticated requests:

### 1. Get Pending Founders
```bash
curl -X GET http://localhost:5001/api/admin/pending-founders \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 2. Approve a Founder
```bash
curl -X POST http://localhost:5001/api/admin/founders/1/approve \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 3. Reject a Founder
```bash
curl -X POST http://localhost:5001/api/admin/founders/1/reject \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 4. Get Support Messages
```bash
curl -X GET http://localhost:5001/api/admin/support-messages \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Testing User Support Endpoint

Users can send support messages:

```bash
# First, login as a regular user to get a token
USER_TOKEN=$(curl -s -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}' | jq -r '.token')

# Send a support message
curl -X POST http://localhost:5001/api/support/message \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content":"I need help with my account"}'
```

## Troubleshooting

### Admin user doesn't exist
The admin user is created automatically when the server starts. If it doesn't exist:
1. Make sure the server has been started at least once
2. Check the database: `sqlite3 launchpad.db "SELECT * FROM users WHERE email='Admin@kgplaunchpad.in';"`

### Login fails with "Invalid credentials"
1. Verify the email is exactly: `Admin@kgplaunchpad.in` (case-sensitive)
2. Verify the password is exactly: `IITKGP2026`
3. Check if the admin user exists in the database

### Database constraint error
If you see an error about role constraint, run:
```bash
python3 fix_admin_role.py
```

This updates the database schema to allow the 'admin' role.
