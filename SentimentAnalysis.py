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
    #Returns an empty string if the object comment is null
    if comment is None:
        return ''

    #Stores body of comment in variable text
    text = comment.body

    #Assigns probabilities for the comment being negative, neutral and positive
    neg = get_text_negative_proba(text)
    neu = get_text_neutral_proba(text)
    pos = get_text_positive_proba(text)

    #Stores all probabilities in a list
    prob = [neg, neu, pos]

    #Appends coment to the list corresponding to the category with the highest probability (negative, neutral, or positive)
    if neg == max(prob):
        a.append(text)
    if neu == max(prob):
        b.append(text)
    if pos == max(prob):
        c.append(text)

    #If the comment has any replies, calls the process_comments method for each of those replies
    if comment.replies:
        for i in range(len(comment.replies)):
            process_comments(comment.replies[i], a, b, c)

    #Returns all three lists of processed comments
    return [a, b, c]

def main():
    #Creates string of all unprocessed comments extracted from Reddit
    comments = get_submission_comments('https://www.reddit.com/r/learnprogramming/comments/5w50g5/eli5_what_is_recursion/')

    #Initializes lists that will contain processed comments
    neg = []
    neu = []
    pos = []

    #Initializes list that will contain all sets of processed comments
    processed_comments = []

    #Calls processing method for all root comments
    for i in range(len(comments)):
        #Updates list to include the most recent lists of processed comments in each iteration
        processed_comments = (process_comments(comments[i], neg, neu, pos))

    #Prints as many as 10 sample comments from each category (i.e., 10 negative ones, 10 neutral ones, etc)
    for i in range(len(processed_comments)):
        if i == 0:
            print('------------NEGATIVE COMMENTS------------')
        if i == 1:
            print('------------NEUTRAL COMMENTS------------')
        if i == 2:
            print('------------POSITIVE COMMENTS------------')

        #If there are more than 10 comments in a category, prints the first 10
        if len(processed_comments[i]) > 9:
            for j in range(9):
                print(processed_comments[i][j])

        #If there are less than 10 comments in a category, prints all of them
        else:
            for j in range(len(processed_comments[i])):
                print(processed_comments[i][j])

        print()



main()

