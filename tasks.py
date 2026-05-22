from db import get_session_maker
from sqlalchemy import select
from db import Reports
from summarizer import summarize


async def process_summary(report_id: int):

    async for session in get_session_maker():

        result = await session.execute(
            select(Reports).where(Reports.id == report_id)
        )

        report = result.scalar_one_or_none()

        if not report:
            return

        summary = await summarize(report.extracted_text)

        report.summarized_text = summary
        report.status = "completed"

        await session.commit()

        print(summary)