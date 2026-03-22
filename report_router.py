from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List

from db import Reports, get_session_maker
from authentication import current_active_user
from report_schema import ReportCreate, ReportResponse
from summarizer import summarize

router = APIRouter(prefix="/reports", tags=["Reports"])



@router.post("/", response_model=ReportResponse)
async def create_report(
    data: ReportCreate,
    session: AsyncSession = Depends(get_session_maker),
    user=Depends(current_active_user)
):
    try:
        summary = await summarize(data.extracted_text)

        new_report = Reports(
            extracted_text=data.extracted_text,
            summarized_text=summary,
            language=data.language,
            status="completed",
            user_id=user.id
        )

        session.add(new_report)
        await session.commit()
        await session.refresh(new_report)

        return new_report

    except Exception:
        raise HTTPException(status_code=500, detail="Error creating report")



@router.get("/", response_model=List[ReportResponse] | ReportResponse)
async def get_reports(
    report_id: Optional[int] = Query(default=None),
    session: AsyncSession = Depends(get_session_maker),
    user=Depends(current_active_user)
):
    if report_id is not None:
        result = await session.execute(
            select(Reports).where(
                Reports.id == report_id,
                Reports.user_id == user.id
            )
        )
        report = result.scalar_one_or_none()

        if not report:
            raise HTTPException(status_code=404, detail="Report not found")

        return report

    result = await session.execute(
        select(Reports).where(Reports.user_id == user.id)
    )
    reports = result.scalars().all()

    return reports


@router.delete("/")
async def delete_report(
    report_id: int,
    session: AsyncSession = Depends(get_session_maker),
    user=Depends(current_active_user)
):
    result = await session.execute(
        select(Reports).where(Reports.id == report_id)
    )
    report = result.scalar_one_or_none()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    if report.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not your report")

    await session.delete(report)
    await session.commit()

    return {"message": "Report deleted successfully"}