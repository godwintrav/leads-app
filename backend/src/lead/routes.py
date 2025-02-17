from datetime import date
from fastapi import APIRouter, Depends, Response
from sqlmodel import Session

from auth.model import User
from auth.util import get_current_user
from lead.schema import LeadCreate, LeadDelete, LeadListResponse, LeadUpdate, LeadResponse
from lead.service import create_lead, delete_leads, get_leads, get_leads_as_csv, update_lead, get_lead
from database.database import get_session

router = APIRouter(prefix="/leads", tags=["Leads"])

# controller function for handling creating a new lead. This a protected route
@router.post("/", response_model=LeadResponse, status_code=201)
async def create(lead_data: LeadCreate, user: User = Depends(get_current_user), session: Session = Depends(get_session)) -> LeadResponse:
    return create_lead(lead_data, session=session)

# controller function for handling exporting all lead data as csv. This a protected route
@router.get("/export", response_class=Response)
def export_leads_as_csv(csv_data: str = Depends(get_leads_as_csv)):
    if not csv_data:
        return Response(content="No data available", media_type="text/plain")

    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=leads.csv"}
    )

# controller function for handling  fetching a single lead data. This a protected route
@router.get("/{lead_id}", response_model=LeadResponse, status_code=200)
async def retrieve(lead_id: int, user: User = Depends(get_current_user), session: Session = Depends(get_session)) -> LeadResponse:
    return get_lead(lead_id, session=session)

# controller function for handling updating lead data. This a protected route
@router.put("/{lead_id}", response_model=LeadResponse, status_code=200)
async def update(lead_id: int, lead_data: LeadUpdate, user: User = Depends(get_current_user), session: Session = Depends(get_session)) -> LeadResponse:
    return update_lead(lead_id, lead_data, session=session)

# controller function for handling deleting multiple lead data. This a protected route
@router.delete("/", status_code=200)
async def delete_leads_route(
    lead_data: LeadDelete,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> dict:
    return delete_leads(lead_data.lead_ids, session=session)

# controller function for handling  fetching multiple leads based on filtering or search parameters set. This a protected route
@router.get("/", response_model=LeadListResponse)
async def fetch_leads(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    limit: int = 10,
    page: int = 1,
    from_date: date | None = None,
    to_date: date | None = None,
    sort: str = "desc",
    engaged: bool | None = None,
    stage: int | None = None,
    search: str | None = None
):
    return get_leads(
        session=session,
        limit=limit,
        page=page,
        from_date=from_date,
        to_date=to_date,
        sort=sort,
        engaged=engaged,
        stage=stage,
        search=search
    )
