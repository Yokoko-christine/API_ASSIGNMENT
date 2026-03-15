
# Refund routes for payment API
import logging
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.services.payment_service import PaymentService
from app.repos.fake_payment_repo import FakePaymentRepo

logger = logging.getLogger(__name__)
router = APIRouter()
service = PaymentService(FakePaymentRepo())



@router.post("/refunds", status_code=201)
async def create_refund(body: dict):
    payment_id = body.get("paymentId")
    amount = body.get("amount")

    if not payment_id or amount is None:
        return JSONResponse(status_code=400, content={"error": "Both paymentId and amount are required."})

    try:
        refund = service.refund(payment_id, amount)
        return JSONResponse(status_code=201, content=refund)
    except ValueError as err:
        error_message = str(err)
        if "exceeds" in error_message:
            return JSONResponse(status_code=422, content={"error": error_message})
        if "not found" in error_message.lower():
            return JSONResponse(status_code=404, content={"error": error_message})
        return JSONResponse(status_code=400, content={"error": error_message})
    except Exception as err:
        logger.error(err)
        return JSONResponse(status_code=500, content={"error": "Internal server error."})



@router.get("/refunds/{refund_id}")
async def get_refund(refund_id: str):
    refund = service.get_refund(refund_id)
    if not refund:
        return JSONResponse(status_code=404, content={"error": "Refund not found."})
    return refund
