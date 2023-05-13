from myDB import myDB
from flask import redirect, url_for

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

def make_txt_file_for_download(user_id, quiz_id):
    '''Function returns a completed text with all the answers and comments for the user to download'''
    with myDB() as db:
        is_graded = db.get_quiz_comment_graded(user_id, quiz_id)
        if is_graded[0][4] == 1:
            quizname = db.get_quiz_num(quiz_id)
            answers = db.get_all_user_answers(int(user_id), int(quiz_id))
        else:
            return redirect(url_for('index'))
    linebreak = '======================================================================================='
    output = ''
    output += f'Quiz Name: {quizname[0][1]}\n\n{linebreak}\n\n'
    output += f'Quiz Comment:\n{is_graded[0][3]}\n\n{linebreak}\n\n'
    for answer in answers:
        question_text = answer[0]
        q_type = answer[1]
        essay = answer[7]
        comment = answer[8]
        choice1_selected = answer[3]
        choice2_selected = answer[4]
        choice3_selected = answer[5]
        choice4_selected = answer[6]
        choice1_text    = answer[14]
        choice2_text    = answer[15]
        choice3_text    = answer[16]
        choice4_text    = answer[17]

        if q_type == 0 or q_type == 2:
            output += f'Question:\n{question_text}\n\nAlternatives:\n'
            output += "Your Answer -->\t" + choice1_text + "\n\n" if choice1_selected == 1 else "\t\t" + choice1_text + "\n\n"
            output += "Your Answer -->\t" + choice2_text + "\n\n" if choice2_selected == 1 else "\t\t" + choice2_text + "\n\n"
            output += "Your Answer -->\t" + choice3_text + "\n\n" if choice3_selected == 1 else "\t\t" + choice3_text + "\n\n"
            output += "Your Answer -->\t" + choice4_text + "\n\n" if choice4_selected == 1 else "\t\t" + choice4_text + "\n\n"
            if comment != '':
                output += f'Comment:\n{comment}\n\n'
            output += f'{linebreak}\n\n'
        else:
            output += f'Question:\n{question_text}\n\nAnswer:\n'
            output += f'{essay}\n\n'
            if comment != '':
                output += f'Comment:\n{comment}\n\n'
            output += f'{linebreak}\n\n'
    
    return output