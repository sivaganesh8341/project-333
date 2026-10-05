from sqlalchemy.orm import Session
from app.models.master_data import MasterData
from sqlalchemy import func
from app.exceptions.custom_exceptions import NotFoundException, DuplicateNameException

def generate_sequential_product_code(name: str, db: Session) -> str:
    prefix = ''.join(e for e in name.upper() if e.isalnum())[:5].ljust(5, "X")[:5]
    max_code = db.query(func.max(MasterData.product_code)).filter(MasterData.product_code.like(f"{prefix}%")).scalar()
    if max_code:
        try:
            number_part = int(max_code[len(prefix):]) + 1
        except ValueError:
            number_part = 1
    else:
        number_part = 1
    return f"{prefix}{number_part:05d}"

def validate_unique_name(name: str, db: Session):
    existing = db.query(MasterData).filter(MasterData.name == name).first()
    if existing:
        raise DuplicateNameException(name)

def create_masterdata(request, db: Session):
    validate_unique_name(request.name, db)
    product_code = generate_sequential_product_code(request.name, db)
    new_masterdata = MasterData(
        name=request.name,
        parent_id=request.parentId,
        brand_id=request.brandId,
        type=request.type,
        status=request.status,
        summary=request.summary,
        Description=request.description,
        product_code=product_code
    )
    db.add(new_masterdata)
    db.commit()
    db.refresh(new_masterdata)
    return new_masterdata

def get_active_product(skip: int, limit: int, db: Session):
    return db.query(MasterData).filter(MasterData.status == True, MasterData.type == 2).offset(skip).limit(limit).all()

def fetch_product_by_id(product_id: int, db: Session):
    product = db.query(MasterData).filter(MasterData.id == product_id).first()
    if not product:
        raise NotFoundException(f"Product with ID {product_id}")
    return product

def remove_masterdata(product_id: int, db: Session):
    product_query = db.query(MasterData).filter(MasterData.id == product_id)
    product = product_query.first()
    if not product:
        raise NotFoundException(f"Product with ID {product_id}")
    product_query.delete(synchronize_session=False)
    db.commit()
    return {"message": f"The product with ID {product_id} was successfully deleted."}

def update_masterdata(product_id: int, request, db: Session):
    product_query = db.query(MasterData).filter(MasterData.id == product_id)
    existing_product = product_query.first()
    if not existing_product:
        raise NotFoundException(f"Product with ID {product_id}")

    update_data = request.model_dump(exclude_unset=True)
    # prevent changing product_code manually:
    update_data.pop("product_code", None)
    # If name is changed, ensure new name unique
    if "name" in update_data and update_data["name"] != existing_product.name:
        validate_unique_name(update_data["name"], db)

    product_query.update(update_data, synchronize_session=False)
    db.commit()
    return {"message": f"Product with ID {product_id} updated successfully"}
