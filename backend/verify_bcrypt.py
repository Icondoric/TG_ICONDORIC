import bcrypt
import passlib.handlers.bcrypt
print(f"bcrypt version: {bcrypt.__version__}")
try:
    print(f"passlib seeing bcrypt version: {passlib.handlers.bcrypt._bcrypt.__about__.__version__}")
except AttributeError:
    print("passlib cannot see bcrypt version (AttributeError)")
except Exception as e:
    print(f"Error: {e}")
