from myDB import myDB

def set_is_quiz_graded(user_id, quiz_id):
    '''Sets the checkbox to True/False if all the answers have been graded'''
    with myDB() as db:
        answers_graded = db.check_answer_is_graded(user_id, quiz_id)
        quiz_graded = db.get_quiz_comment_graded(user_id, quiz_id)
        if any(answer[0] == 0 for answer in answers_graded) == True:
            db.update_quiz_graded(quiz_graded[0][0], 0)
        if any(answer[0] == 0 for answer in answers_graded) == False:
            db.update_quiz_graded(quiz_graded[0][0], 1)
        quiz_graded = db.get_quiz_comment_graded(user_id, quiz_id)
    return quiz_graded[0][4]