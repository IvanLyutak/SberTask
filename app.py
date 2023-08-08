from fastapi import FastAPI, status, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from schemas.deposits import DepositSchema
from services.calculator import depositCalculation

app = FastAPI()

@app.exception_handler(HTTPException)
def custom_exception_handler(_: Request, exc: HTTPException):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, 
        content={"error": str(exc.detail) })

@app.exception_handler(RequestValidationError)
def validation_exception_handler(_: Request, exc: RequestValidationError):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, 
        content={"error": str(exc) })

@app.post("/deposit")
def deposit(item: DepositSchema):
    try:
        return depositCalculation(item.date, item.periods, item.amount, item.rate)    
    except Exception as err:
        raise HTTPException(400, str(err))