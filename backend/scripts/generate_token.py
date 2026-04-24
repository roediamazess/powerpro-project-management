import sys
import os
sys.path.append('/app')
from app.core import security
from datetime import timedelta

# Mock a user ID
token = security.create_access_token(
    subject="e893a6c1-9cd8-43c4-995f-229b921d477b", # admin user id
    expires_delta=timedelta(minutes=5)
)
print(token)
