from dataclasses import dataclass

@dataclass
class QuestionAnswerTranslate:
    id: int
    lang_id: int
    question_text: str
    answer_text: str
    status: int

    __select__ = '''
    select
        q."id",
        q."status",
        qt.lang_id,
        qt."translation" as question_text,
        qat."translation" as answer_text
    from question q
    join question_translation qt on qt.question_id = q."id"
    join question_answer_translation qat on qat.question_id = q."id" and qat.lang_id = qt.lang_id
    '''