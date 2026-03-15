
import logging
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.services.payment_service import PaymentService
from app.repos.fake_payment_repo import FakePaymentRepo

logger = logging.getLogger(__name__)
router = APIRouter()
service = PaymentService(FakePaymentRepo())



@router.post("/customers", status_code=201)
async def create_customer(body: dict):
    name = body.get("name")
    email = body.get("email")

    if not name or not email:
        return JSONResponse(status_code=400, content={"error": "Both name and email are required."})
    if len(name) > 100:
        return JSONResponse(status_code=400, content={"error": "Name exceeds maximum length."})

    try:
        customer = service.create_customer(name, email)
        return JSONResponse(status_code=201, content=customer)
    except ValueError as err:
        error_message = str(err)
        if "already exists" in error_message:
            return JSONResponse(status_code=409, content={"error": error_message})
        return JSONResponse(status_code=400, content={"error": error_message})
    except Exception as err:
        logger.error(err)
        return JSONResponse(status_code=500, content={"error": "Internal server error."})



@router.get("/customers/{customer_id}")
async def get_customer(customer_id: str):
    customer = service.get_customer(customer_id)
    if not customer:
        return JSONResponse(status_code=404, content={"error": "Customer not found."})
    return customer



@router.get("/customers/{customer_id}/payments")
async def get_customer_payments(customer_id: str):
    customer = service.get_customer(customer_id)
    if not customer:
        return JSONResponse(status_code=404, content={"error": "Customer not found."})
    return service.get_payments_for_customer(customer_id)
