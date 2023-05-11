class quiz_index:
    def __init__(self, quiz_id, quizname, description, category, is_public) -> None:
        self.quiz_id        = quiz_id
        self.name           = quizname
        self.description    = description
        self.category       = category
        self.is_public      = is_public

class quiz_questions:
    def __init__(self, question_id, quiz_id, question_text, choice1_text, choice2_text, choice3_text, 
                 choice4_text, essay, choice1_correct, choice2_correct, choice3_correct, choice4_correct, 
                 approved, q_type) -> None:
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
        self.essay          = essay
        self.appoved        = approved
        self.q_type       = q_type

class answered_question:
    def __init__(self, question_text, q_type, aid, choice1_selected, choice2_selected, choice3_selected, choice4_selected,
                 essay_answer, comment, graded, choice1_correct, choice2_correct, choice3_correct, choice4_correct,
                 choice1_text, choice2_text, choice3_text, choice4_text) -> None:
        self.q_txt = question_text
        self.q_type = q_type
        self.aid = aid
        self.a1_sel = choice1_selected
        self.a2_sel = choice2_selected
        self.a3_sel = choice3_selected
        self.a4_sel = choice4_selected
        self.a_essay = essay_answer
        self.comment = comment
        self.c1_cor = choice1_correct
        self.c2_cor = choice2_correct
        self.c3_cor = choice3_correct
        self.c4_cor = choice4_correct
        self.c1_txt = choice1_text
        self.c2_txt = choice2_text
        self.c3_txt = choice3_text
        self.c4_txt = choice4_text
        self.graded = graded

class all_users():
    def __init__(self, uid, fname, lname, email, pwh, uname, admin) -> None:
        self.user_id        = uid
        self.firstname      = fname
        self.lastname       = lname
        self.email          = email
        self.passwordHash   = pwh
        self.username       = uname
        self.admin          = admin

class all_user_answers:
    def __init__(self, question_text, choice1, choice2, choice3, choice4, 
                 choice1_correct, choice2_correct, choice3_correct, choice4_correct,
                 choice1_text, choice2_text, choice3_text, choice4_text) -> None:
        self.question       = question_text
        self.choice1        = choice1
        self.choice2        = choice2
        self.choice3        = choice3
        self.choice4        = choice4
        self.is_correct1    = choice1_correct
        self.is_correct2    = choice2_correct
        self.is_correct3    = choice3_correct
        self.is_correct4    = choice4_correct
        self.choice1_text   = choice1_text
        self.choice2_text   = choice2_text
        self.choice3_text   = choice3_text
        self.choice4_text   = choice4_text





