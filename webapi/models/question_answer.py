from pydantic import BaseModel

class QuestionAnswer(BaseModel):
    questionId: int
    langId: int
    questionTranslation: str
    answerTranslation: str
    statusId: int
