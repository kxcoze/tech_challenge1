import json
import logging
import asyncio
from datetime import datetime
from typing import Any, List, Dict

import aiohttp
from aiohttp.client_exceptions import ClientResponseError
from fastapi import APIRouter, Depends, Request
from sqlalchemy.exc import IntegrityError

from src.schemas import QuestionRequest
from src.config import config
from src.logger import CustomLogger
from src.api.deps import get_db
from db.models import Question
from db.session import SessionLocal


router = APIRouter()


logger = CustomLogger("endpoint_logger")


async def fetch_questions(questions_num: int) -> List:
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        async with session.get(
            f"https://jservice.io/api/random?count={questions_num}"
        ) as response:
            data = await response.read()
            return json.loads(data)


@router.post("/get_questions/")
async def get_questions(
    question_request: QuestionRequest,
    request: Request,
    db: SessionLocal = Depends(get_db),
) -> Dict:
    current_amount = question_request.questions_num
    for attempt in range(1, config.MAX_ATTEMPTS + 1):
        try:
            questions: List = await fetch_questions(current_amount)
        except ClientResponseError:
            # If client is not accesible appently we send too much requests, let's wait
            wait = attempt * 5  # Waiting in seconds
            logger.log_with_request(
                logging.WARNING,
                f"External server is busy, let's try after {wait}s.",
                request,
            )
            await asyncio.sleep(wait)
            continue

        for question in questions:
            try:
                # We receive "%Y-%m-%dT%H:%M:%S.%fZ" format of time so just
                # remove last letter from string to convert to ISO format
                formatted_created_at = datetime.fromisoformat(
                    question["created_at"][:-1]
                )
                q = Question(
                    id=question["id"],
                    question_text=question["question"],
                    answer_text=question["answer"],
                    created_at=formatted_created_at,
                )
                db.add(q)
                db.commit()
                current_amount -= 1
            except IntegrityError:
                # Question already in db, skip
                db.rollback()
                continue
        if current_amount == 0:
            logger.log_with_request(
                logging.INFO,
                f"{question_request.questions_num} questions were added to database!",
                request,
            )
            # All possible questions have been received
            break
        else:
            logger.log_with_request(
                logging.WARNING,
                f"{current_amount} were already in database, trying to fetch remaining questions...",
                request,
            )

    else:
        logger.log_with_request(
            logging.ERROR,
            f"After {config.MAX_ATTEMPTS} attempts no available questions has been found",
            request,
        )
        # None questions are available from site, try later
        return {}

    if questions:
        return questions[-1]
    return {}

