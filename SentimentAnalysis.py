import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import praw

reddit = praw.Reddit(client_id= 'vRFmnr-5nov9pA',
                     client_secret='sQbptqP1nvj7w57TSh6fYpdyjMo',
                     user_agent='my user agent'
                     )


nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()


def get_text_negative_proba(text):
   return sid.polarity_scores(text)['neg']


def get_text_neutral_proba(text):
   return sid.polarity_scores(text)['neu']


def get_text_positive_proba(text):
   return sid.polarity_scores(text)['pos']


def get_submission_comments(url):
    submission = reddit.submission(url=url)
    submission.comments.replace_more()

    return submission.comments


def process_comments(comment, a, b, c):
    if comment is None:
        return ''

    text = comment.body
    neg = get_text_negative_proba(text)
    neu = get_text_neutral_proba(text)
    pos = get_text_positive_proba(text)
    prob = [neg, neu, pos]
    if neg == max(prob):
        a.append(text)
    if neu == max(prob):
        b.append(text)
    if pos == max(prob):
        c.append(text)

    if comment.replies:
        for i in range(len(comment.replies)):
            process_comments(comment.replies[i], a, b, c)

    return [a, b, c]

def main():

    comments = get_submission_comments('https://www.reddit.com/r/learnprogramming/comments/5w50g5/eli5_what_is_recursion/')
    neg = []
    neu = []
    pos = []
    processed_comments = []

    for i in range(len(comments)):
        processed_comments = (process_comments(comments[i], neg, neu, pos))


    for i in range(len(processed_comments)):
        if i == 0:
            print('------------NEGATIVE COMMENTS------------')
        if i == 1:
            print('------------NEUTRAL COMMENTS------------')
        if i == 2:
            print('------------POSITIVE COMMENTS------------')
        if len(processed_comments[i]) > 9:
            for j in range(9):
                print(processed_comments[i][j])
        else:
            for j in range(len(processed_comments[i])):
                print(processed_comments[i][j])

        print()



main()

