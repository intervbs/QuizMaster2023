class quiz_index:
    def __init__(self, quiz_id, quizname, description, category, is_public) -> None:
        self.quiz_id        = quiz_id
        self.name           = quizname
        self.description    = description
        self.category       = category
        self.is_public      = is_public

class quiz_questions:
    def __init__(self, question_id, quiz_id, question_text, choice1_text, choice2_text, choice3_text, 
                 choice4_text, choice1_correct, choice2_correct, choice3_correct, choice4_correct) -> None:
        self.question_id    = question_id
        self.quiz_id        = quiz_id
        self.question       = question_text
        self.choice1        = choice1_text
        self.choice2        = choice2_text
        self.choice3        = choice3_text
        self.choice4        = choice4_text
        self.is_correct1    = choice1_correct
        self.is_correct2    = choice2_correct
        self.is_correct3    = choice3_correct
        self.is_correct4    = choice4_correct
    




