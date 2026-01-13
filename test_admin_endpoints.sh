#!/bin/bash
# Test script for admin endpoints
# Make sure the backend server is running on port 5001

BASE_URL="http://localhost:5001"
ADMIN_EMAIL="Admin@kgplaunchpad.in"
ADMIN_PASSWORD="IITKGP2026"

echo "=========================================="
echo "Testing Admin Login and Endpoints"
echo "=========================================="
echo ""

# Test 1: Admin Login
echo "1. Testing Admin Login..."
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$ADMIN_EMAIL\",\"password\":\"$ADMIN_PASSWORD\"}")

echo "Response: $LOGIN_RESPONSE"
echo ""

# Extract token
TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
  echo "❌ Login failed! Could not extract token."
  echo "Please check:"
  echo "  - Is the server running on port 5001?"
  echo "  - Does the admin user exist in the database?"
  echo "  - Run: python3 app.py to start the server (this will create the admin user)"
  exit 1
fi

echo "✓ Login successful! Token: ${TOKEN:0:20}..."
echo ""

# Test 2: Get Pending Founders
echo "2. Testing Get Pending Founders..."
PENDING_RESPONSE=$(curl -s -X GET "$BASE_URL/api/admin/pending-founders" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json")

echo "Response: $PENDING_RESPONSE"
echo ""

# Test 3: Get Support Messages
echo "3. Testing Get Support Messages..."
SUPPORT_RESPONSE=$(curl -s -X GET "$BASE_URL/api/admin/support-messages" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json")

echo "Response: $SUPPORT_RESPONSE"
echo ""

echo "=========================================="
echo "All tests completed!"
echo "=========================================="
