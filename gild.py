from __future__ import division
import praw,threading,datetime,time,os,json

r = None
data = {}
subcount = {}
jsonread = open(os.path.join(os.path.dirname(__file__), "subcount.json"), 'r')
subcount = json.loads(jsonread.read())
jsonread.close()
def getgildings():
    data = {}
    "subcount = {}"
    print 'Getting 1000 posts...'
    comments = r.get_comments('all',gilded_only=True, params={'t':'day'}, limit=2000)
    # ALERT: Old code. Doesn't need to be fast because it only posts once a day.
    print 'Got 1000 posts, sorting and counting now...'
    count = 0 # generators can't be len()
    for comment in comments:
        count+=1
        try:
            subcount[comment.subreddit.display_name] == 1
        except:
            subcount[comment.subreddit.display_name] = comment.subreddit.subscribers
        try:
            data[comment.subreddit.display_name] = data[comment.subreddit.display_name] + 1
        except:
            data[comment.subreddit.display_name] = 1
    gildscore = {}
    print count
    now = datetime.datetime.now()
    print 'All counted, creating post now...'
    num = 1
    post = "Data from last 1000 gilds in a total of {count} subreddits (**bolded** subreddits are abnormally gilded):\n\nRanking | Subreddit | Gild Count\n---------|---------|---------\n".replace("{count}",str(len(data)))
    for sub in sorted(data, key=data.get, reverse=True):
        "print sub + ':' + str(data[sub]/subcount[sub])"
        if data[sub]/subcount[sub] > 0.0001 and data[sub] > 1:
            post = post + str(num) + ". | **/r/{sub}".replace("{sub}",sub) + "** | **" + str(data[sub]) + "**\n"
        elif data[sub] > 1:
            post = post + str(num) + ". | /r/{sub}".replace("{sub}",sub) + " | " + str(data[sub]) + "\n"
        num = num + 1
    post = post + "Subreddits with less than 2 gilds are not shown." \
                  "\n\nIf you're a mod or just a user, consider linking here to show your subscribers how you rank up against other subreddits!"
    main = r.get_subreddit('gildstats') # put your own subreddit there

    r.submit(main, "Gild Statistics for "+str(now)[:10], text=post) # again, change this value to what you want.
    try:
        jsondata = open(os.path.join(os.path.dirname(__file__), "subcount.json"), 'w')
        jsondata.write(json.dumps(subcount))
        jsondata.close()
        print 'opened and wrote to file...'
    except:
        pass
        # json was just easier for storage, I plan to add sqlite
    print 'Submitted post! Closing...'





if __name__ == "__main__":
    user_agent = ("GildStats-bot v0.1.0.3 by /u/sciguymjm. Sorry in advance :c")
    r = praw.Reddit(user_agent=user_agent)
    r.login('', '') # add your information here

    getgildings()