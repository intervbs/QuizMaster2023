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

class all_users():
    def __init__(self, uid, fname, lname, email, pwh, uname, admin) -> None:
        self.user_id = uid
        self.firstname = fname
        self.lastname = lname
        self.email = email
        self.passwordHash = pwh
        self.username = uname
        self.admin = admin

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





