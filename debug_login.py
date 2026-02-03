
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_system.settings")
django.setup()

from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

# Cleanup
User.objects.filter(username="test@example.com").delete()

# Create User
email = "test@example.com"
password = "correct_password"
print(f"Creating user {email} with password '{password}'")
user = User.objects.create_user(username=email, email=email, password=password)

# Test Correct Login
user_auth = authenticate(username=email, password=password)
if user_auth:
    print("SUCCESS: Correct password login worked.")
else:
    print("FAILURE: Correct password login failed.")

# Test Wrong Login
wrong_pass = "wrong_password"
print(f"Testing login with password '{wrong_pass}'")
user_wrong = authenticate(username=email, password=wrong_pass)

if user_wrong:
    print("CRITICAL LOGIC ERROR: User logged in with WRONG password!")
else:
    print("SUCCESS: User logic correctly rejected wrong password.")
