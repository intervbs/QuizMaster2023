class quiz_index:
    def __init__(self, quiz_id, quizname, description, category, user_id, visible) -> None:
        self.quiz_id        = quiz_id
        self.name           = quizname
        self.description    = description
        self.category       = category
        self.user_id        = user_id
        self.visible        = visible

class quiz_everything:
    def __init__(self):#, question_id, quiz_id, question_text, answer_id, answer_text) -> None:
        self.questions_id   = None#= question_id
        self.quiz_id        = None#= quiz_id
        self.question       = None#= question_text
        self.answer_id      = None#= answer_id
        self.alt = []
    
    def __iter__(self):
        for self.question, answers in self.alt:
            yield (self.question, answers)


