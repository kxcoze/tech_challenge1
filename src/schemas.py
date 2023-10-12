from pydantic import BaseModel, conint


class QuestionRequest(BaseModel):
    # questions_num must be in 1 <= questions_num <= 100
    questions_num: conint(ge=1, le=100)
