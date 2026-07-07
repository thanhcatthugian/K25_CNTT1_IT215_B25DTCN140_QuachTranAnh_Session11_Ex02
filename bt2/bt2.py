from fastapi import FastAPI,HTTPException,status,Depends,Request,Path
from fastapi.encoders import jsonable_encoder
from database import *
from model import *
from schema import *
from user_service import *
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from datetime import datetime

app = FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()
    

def create_response(
        status_code:int,
        message:str,
        error = None,
        data = None,
        path = ""
):
    return JSONResponse(
        status_code=status_code,
        content={
            "status_code":status_code,
            "message":message,
            "error":error,
            "data":data,
            "timestamp": datetime.utcnow().isoformat(),
            "path": path
        }
    )

@app.exception_handler(RequestValidationError)

def request_validation_handler(request:Request,exc:RequestValidationError):
    return create_response(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        message="Loi dinh dang du lieu",
        error=exc.errors,
        path=request.url.path
    )

@app.exception_handler(HTTPException)
def http_exception_handler(request:Request,exc:HTTPException):
    return create_response(
        status_code=exc.status_code,
        message=exc.detail,
        path=request.url.path
    )

@app.exception_handler(Exception)
def exception_handler(request:Request,exc:Exception):
    print(f"[INTERNAL SERVER ERROR] Path: {request.url.path} | {str(exc)}")
    return create_response(
        status_code=500,
        message="Loi server vui long thu lai sau",
        path=request.url.path
    )

@app.get("/smart-home-plans",response_model=Response)
def show_all_plan(request:Request,db:Session = Depends(get_db)):
    return create_response(
        status_code=status.HTTP_200_OK,
        message="Lay toan bo du lieu thanh cong",
        data=jsonable_encoder(show_all(db)),
        path = request.url.path
    )

@app.post("/smart-home-plans",response_model=Response)
def add_new_plan(request:Request,new_plan:CreatePlan,db:Session = Depends(get_db)):
    check = add_plan(new_plan,db)
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ma goi thiet bi da ton tai"
        )
    return create_response(
        status_code=status.HTTP_201_CREATED,
        message="Tao thanh cong goi thiet bi moi",
        data = jsonable_encoder(check),
        path = request.url.path
    )

@app.get("/smart-home-plans/{plan_id}")
def show_plans_through_id(request:Request,plan_id:int = Path(...),db:Session = Depends(get_db)):
    check = show_through_id(plan_id,db)
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Khong tim thay id goi thiet bi"
        )
    return create_response(
        status_code=status.HTTP_200_OK,
        message="Lay thong tin thanh cong",
        data = jsonable_encoder(check),
        path = request.url.path
    )




