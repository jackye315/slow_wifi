import praw

############ Parse a specific post by url and get its comments

def reddit_setup(client_id, client_secret, user,):
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://localhost",
        user_agent=f"{user}_scrape_post by u/{user}",
    )
    return reddit

def get_post_data(submission) -> dict:
    post_data = {}
    post_data['author'] = submission.author
    post_data['title'] = submission.title
    post_data['score'] = submission.score
    post_data['link'] = submission.url
    post_data['body_text'] = submission.selftext
    return post_data

def _create_comment_dict(submission) -> dict:
    comments_dict = {}
    for comment in submission.comments.list():
        comments_dict[comment.id] = comment
    return comments_dict

def create_comment_conversations(submission) -> list:
    comments_dict = _create_comment_dict(submission)
    
    seen_comments = {}
    comment_conversations = []
    for comment in reversed(submission.comments.list()):
        if comment.id not in seen_comments:
            seen_comments[comment.id] = comment
            curr_comment = comment
            conversation = [curr_comment]
            while curr_comment.parent_id.split('_')[-1] != submission.id:
                curr_comment = comments_dict[curr_comment.parent_id.split('_')[-1]]
                seen_comments[curr_comment.id] = curr_comment
                conversation.append(curr_comment)
            comment_conversations.append(list(reversed(conversation)))
    return comment_conversations

def sort_comment_conversations(comment_order_dict, comment_conversations):
    sorted_conversations = sorted(comment_conversations, key=lambda x: [comment_order_dict[item] for item in x])
    return sorted_conversations

def get_post_and_comments(reddit, url:str):
    submission = reddit.submission(url=url)
    submission.comments.replace_more(limit=None)
    post_data = get_post_data(submission)
    comment_conversations = create_comment_conversations(submission)

    ordered_comments = {key:index for index, key in enumerate(submission.comments.list())}
    sorted_conversations = sort_comment_conversations(ordered_comments, comment_conversations=comment_conversations)
    
    return post_data, sorted_conversations


############ Parse a entire subreddit and get all posts

# subreddit = reddit.subreddit("japanesestreetwear")
# # assume you have a Subreddit instance bound to variable `subreddit`
# for submission in subreddit.hot(limit=3):
#     print(submission.title)
#     # Output: the submission's title
#     print(submission.url)
#     # Output: the URL the submission points to or the submission's URL if it's a self post

if __name__=="__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()
    reddit_client_id = os.environ['reddit_client_id']
    reddit_client_secret = os.environ['reddit_client_secret']
    reddit_user = os.environ['user']

    reddit = reddit_setup(client_id=reddit_client_id,client_secret=reddit_client_secret,user=reddit_user)

    test_urls = [
        "https://www.reddit.com/r/japanesestreetwear/comments/q3wshh/where_to_buy_from_japanese_streetwear/",
        "https://www.reddit.com/r/streetwear/comments/1g22vzm/clarks_x_tokyo_collection_wallabees/",
        "https://www.reddit.com/r/deloitte/comments/1g2psfe/deloitte_global_us_layoffs/",
    ]
    url = test_urls[2]
    submission = reddit.submission(url=url)
    submission.comments.replace_more(limit=None)
    comments_list = submission.comments.list()
    comments_dict = {key:index for index, key in enumerate(comments_list)}

    comment_conversations = create_comment_conversations(submission)
    sorted_conversations = sort_comment_conversations(comments_dict, comment_conversations)
    for conversation in comment_conversations:
        for comment in conversation:
            print(comment.body)