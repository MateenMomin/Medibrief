import asyncio
from db import async_session_maker
from sqlalchemy import select
from db import Reports
from summarizer import summarize


async def process_summary(report_id: int):
    try:
        await asyncio.sleep(1)
        async with async_session_maker() as session:
            result = await session.execute(
                select(Reports).where(Reports.id == report_id)
            )
            report = result.scalar_one_or_none()

            if not report:
                print(f"[tasks] Report {report_id} not found")
                return

            print(f"[tasks] Starting summary for report {report_id}...")
            summary = await summarize(report.extracted_text)

            report.summarized_text = summary
            report.status = "completed"
            await session.commit()
            print(f"[tasks] Report {report_id} completed!")

    except Exception as e:
        print(f"[tasks] ERROR on report {report_id}: {e}")
        import traceback
        traceback.print_exc()