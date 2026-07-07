from model import *
from schema import *
from sqlalchemy.orm import Session

def add_plan(new_plan:CreatePlan,db:Session):
    check = db.query(Homes).filter(Homes.plan_code==new_plan.plan_code).first()
    if check:
        return None
    home_plan = Homes(
        plan_code = new_plan.plan_code,
        plan_name = new_plan.plan_name,
        device_quantity = new_plan.device_quantity,
        price = new_plan.price
    )
    db.add(home_plan)
    db.commit()
    db.refresh(home_plan)
    return home_plan

def show_all(db:Session):
    return db.query(Homes).all()

def show_through_id(plan_id:int,db:Session):
    check = db.query(Homes).filter(Homes.id == plan_id).first()
    if check:
        return check
    return None