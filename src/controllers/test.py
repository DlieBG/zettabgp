from fastapi import APIRouter

test_router = APIRouter()

@test_router.get('/')
def get_test():
    return 'Test 123'
