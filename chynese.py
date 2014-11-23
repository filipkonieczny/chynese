#!/usr/bin/env python
# encoding: utf-8


# TODO: documentation
# description


# imports
import json
import random
import datetime


# globals
MAX_ANSWERS = 3
LETTERS = 'abcdefghijklmnopqrstuvwxyz'
DATA_FILE = 'data.json'
LOGS_DIR = 'logs/'
OVERALL_FILE = '{}overall.json'.format(LOGS_DIR)


# functions
def hello_message():
# TODO: documentation
    '''
    '''

    print "\n"
    print "Aloha."
    print "\n"


def load_data(file_name):
    # TODO: documentation
    '''
    '''

    data_file = open(file_name).read()
    data = json.loads(data_file)

    return data


def randomize_answers(data, correct_answer_id):
    # TODO: documentation
    '''
    '''

    max_characters = len(data)
    answers = []

    for i in xrange(MAX_ANSWERS):
        random_character = random.randint(0, max_characters - 1)
        meanings = data[random_character]['pinyin'] + ' - '
        meanings += ', '.join(data[random_character]['meanings'])
        while random_character + 1 == correct_answer_id or meanings in answers:
            random_character = random.randint(0, max_characters - 1)
            meanings = data[random_character]['pinyin'] + ' - '
            meanings += ', '.join(data[random_character]['meanings'])
        answers.append(meanings)

    return answers


def print_question(index, character_data):
    # TODO: documentation
    '''
    '''

    print '\n'
    print "#%d What's the meaning of this character: %s" % (index + 1,
                                                            character_data['character'])


def shuffle_answers(answers):
    # TODO: documentation
    '''
    '''

    correct_answer = answers[-1]
    shuffled_answers = {}

    for i in xrange(len(answers)):
        random_choice = random.randint(0, len(answers) - 1)

        currently_shuffled_answer = answers.pop(random_choice)
        if currently_shuffled_answer == correct_answer:
            correct_answer_id = LETTERS[i]

        shuffled_answers[LETTERS[i]] = currently_shuffled_answer

    return (shuffled_answers, correct_answer_id)


def print_answers(answers):
    # TODO: documentation
    '''
    '''

    answers_keys = sorted(answers.keys())

    for key in answers_keys:
        print "%s) %s" % (key, answers[key])

    print "\n"


def get_user_choice():
    # TODO: documentation
    '''
    '''

    valid_input = "(%s-%s)" % (LETTERS[0], LETTERS[MAX_ANSWERS])
    user_choice_input_text = "What's your answer%s?: " % valid_input
    user_choice = raw_input(user_choice_input_text)

    while user_choice.lower() not in LETTERS[:MAX_ANSWERS + 1] or len(user_choice) == 0:
        print "Invalid input."

        user_choice = raw_input(user_choice_input_text)

    return user_choice


def evaluate_user_choice(correct_choice, user_choice):
    # TODO: documentation
    '''
    '''

    if user_choice == correct_choice:
        print 'Correct!'
        return True
    else:
        print 'Incorrect! The answer is: %s' % correct_choice
        return False


def print_statistics(total_characters, total_correct, total_incorrect):
    # TODO: documentation
    '''
    '''

    print "\n"
    print "Total characters: %s" % total_characters
    print "Total correct: %s" % total_correct
    print "Total incorrect: %s" % total_incorrect
    print "Success rate: %.2f%%" % ((float(total_correct) / float(total_characters)) * 100)


def save_data(file_name, data):
    # TODO: documentation
    '''
    '''

    with open(file_name, 'w') as outfile:
        json.dump(data, outfile, indent=4)


def goodbye_message():
    # TODO: documentation
    '''
    '''

    print '\n'
    print 'Thanks for using Chynese!'
    print '\n'


def main():
    # TODO: documentation
    '''
    '''

    total_correct = 0
    total_incorrect = 0

    hello_message()

    data = load_data(DATA_FILE)

    # encode the character to be displayed
    for i, character_data in enumerate(data):
        print_question(i, character_data)

        answers = {}
        correct_answer = character_data['pinyin'] + " - "
        correct_answer += ', '.join(character_data['meanings'])
        answers = randomize_answers(data, character_data['id'])
        answers.append(correct_answer)
        shuffled_answers = shuffle_answers(answers)
        correct_choice = shuffled_answers[1]
        print_answers(shuffled_answers[0])

        user_choice = get_user_choice()
        if evaluate_user_choice(correct_choice, user_choice):
            total_correct += 1
            data[i]['times_answered_correctly'] += 1
        else:
            total_incorrect += 1
            data[i]['times_answered_incorrectly'] += 1

        total_character_answers = data[i]['times_answered_correctly'] + data[i]['times_answered_incorrectly']
        data[i]['success_rate'] = "%.2f%%" % ((float(data[i]['times_answered_correctly']) / float(total_character_answers)) * 100)

        total_characters = i + 1

    # print statistics for current session
    print_statistics(total_characters, total_correct, total_incorrect)

    # save character statistics
    save_data(DATA_FILE, data)

    # get current time
    now = str(datetime.datetime.now())[:-7]

    # save session statistics
    session_statistics = {
        'total_characters': total_characters,
        'total_correct': total_correct,
        'total_incorrect': total_incorrect,
        'success_rate': "%.2f%%" % ((float(total_correct) / float(total_characters)) * 100)
    }
    save_data('{}{}.json'.format(LOGS_DIR, now), session_statistics)

    # save overall statistics
    overall_statistics = load_data(OVERALL_FILE)
    overall_statistics['last_taken_date'] = now
    overall_statistics['times_taken'] += 1
    overall_statistics['total_characters'] = total_characters
    overall_statistics['times_answered_correctly'] += total_correct
    overall_statistics['times_answered_incorrectly'] += total_incorrect
    overall_statistics['success_rate'] = "%.2f%%" % ((overall_statistics['times_answered_correctly']) / (float(overall_statistics['times_answered_correctly']) + float(overall_statistics['times_answered_incorrectly'])) * 100)
    save_data(OVERALL_FILE, overall_statistics)

    # goodbye
    goodbye_message()


# run the main function
if __name__ == '__main__':
    main()
