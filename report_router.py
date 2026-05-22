from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
import asyncio
from tasks import process_summary
from db import Reports, get_session_maker
from authentication import current_active_user
from report_schema import ReportCreate, ReportResponse
from summarizer import (
    summarize,
    answer_question,
    translate_report
)

router = APIRouter(prefix="/reports", tags=["Reports"])



@router.post("/", response_model=ReportResponse)
async def create_report(
    data: ReportCreate,
    session: AsyncSession = Depends(get_session_maker),
    user=Depends(current_active_user)
):
    try:

        new_report = Reports(
            extracted_text=data.extracted_text,
            summarized_text=None,
            language=data.language,
            status="Processing",
            user_id=user.id
        )

        session.add(new_report)
        await session.commit()
        await session.refresh(new_report)
        asyncio.create_task(process_summary(new_report.id))


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

@router.post("/ask")
async def ask_question(
    report_id: int,
    question: str,
    session: AsyncSession = Depends(get_session_maker),
    user=Depends(current_active_user)
):

    result = await session.execute(
        select(Reports).where(
            Reports.id == report_id,
            Reports.user_id == user.id
        )
    )

    report = result.scalar_one_or_none()

    if not report:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    answer = await answer_question(
        report.extracted_text,
        question
    )

    return {
        "answer": answer
    }
    
@router.post("/translate")
async def translate(
    report_id: int,
    language: str,
    session: AsyncSession = Depends(get_session_maker),
    user=Depends(current_active_user)
):

    result = await session.execute(
        select(Reports).where(
            Reports.id == report_id,
            Reports.user_id == user.id
        )
    )

    report = result.scalar_one_or_none()

    if not report:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    translated = await translate_report(
        report.summarized_text,
        language
    )

    return {
        "translation": translated
    }