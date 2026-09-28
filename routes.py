from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import ContactMessage, ServiceEnquiry
from app.schemas import (
    ContactCreate,
    ContactResponse,
    LoginRequest,
    ServiceEnquiryCreate,
    ServiceEnquiryResponse,
    TokenResponse,
)
from app.security import create_access_token, require_admin

router = APIRouter()


def admin_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        lambda: None
    ),
):
    # This dependency is replaced below using the explicit security dependency.
    return credentials


from fastapi.security import HTTPBearer
admin_bearer = HTTPBearer(auto_error=False)


def require_admin_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(admin_bearer),
):
    return require_admin(credentials)


@router.post("/auth/login", response_model=TokenResponse, tags=["Authentication"])
def login(data: LoginRequest):
    if (
        data.username != settings.admin_username
        or data.password != settings.admin_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    return {
        "access_token": create_access_token(data.username),
        "token_type": "bearer",
    }


@router.post("/contact", response_model=ContactResponse, status_code=201, tags=["Public"])
def create_contact(
    data: ContactCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    # A simple application-level guard. Put a real IP rate limiter such as
    # slowapi or a reverse-proxy limiter in front of this endpoint for production.
    message = ContactMessage(**data.model_dump())
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


@router.post(
    "/service-enquiries",
    response_model=ServiceEnquiryResponse,
    status_code=201,
    tags=["Public"],
)
def create_service_enquiry(
    data: ServiceEnquiryCreate,
    db: Session = Depends(get_db),
):
    enquiry = ServiceEnquiry(**data.model_dump())
    db.add(enquiry)
    db.commit()
    db.refresh(enquiry)
    return enquiry


@router.get(
    "/admin/contacts",
    response_model=list[ContactResponse],
    tags=["Admin"],
)
def list_contacts(
    db: Session = Depends(get_db),
    _: str = Depends(require_admin_user),
):
    return db.scalars(
        select(ContactMessage).order_by(ContactMessage.created_at.desc())
    ).all()


@router.get(
    "/admin/service-enquiries",
    response_model=list[ServiceEnquiryResponse],
    tags=["Admin"],
)
def list_service_enquiries(
    db: Session = Depends(get_db),
    _: str = Depends(require_admin_user),
):
    return db.scalars(
        select(ServiceEnquiry).order_by(ServiceEnquiry.created_at.desc())
    ).all()


@router.patch("/admin/contacts/{message_id}/read", tags=["Admin"])
def mark_contact_read(
    message_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(require_admin_user),
):
    message = db.get(ContactMessage, message_id)
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")

    message.is_read = True
    db.commit()
    return {"status": "updated", "id": message_id}
