import praw
import pyttsx3
import ides
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By



def screenshot(driver,type,id):
    target = ""
    if type == "title" and type == "comment" and type == "body":
        print("invalid type for screenshot !!!")
        return
    
    if type == "title":
        target = f"t3_{id}"
    if type == "comment":
        target = f"t1_{id}-comment-rtjson-content"
    if type == "body":
        target = f"t3_{id}-post-rtjson-content"
    
    element = driver.find_elements(By.ID, target)
    if not element:
        print(f"{type} {id} elemnt not found !!!")
        return 
    element[0].screenshot(f"temp/{id}_{type}.png")


def take_screenshots(url,id):
    driver = webdriver.Firefox()
    driver.get(url)
    for com_id in output["comment_ides"]:
        screenshot(driver,"comment",com_id)

    screenshot(driver,"title",id)
    screenshot(driver,"body",id)
    
    driver.quit()
    
    




def voice_over_mp3():
    # Initialize the Pyttsx3 engine
    engine = pyttsx3.init()
    # Set the voice
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    # We can use file extension as mp3 and wav, both will work
    engine.save_to_file(output["title"], 'temp/title.mp3')
    engine.save_to_file(output["body"], 'temp/body.mp3')
    for com_id, comment in zip(output["comment_ides"], output["comments"]):
        engine.save_to_file(comment, f'temp/{com_id}_comment.mp3')    
    
    #engine.save_to_file(output["comments"], 'temp/comments.mp3')
    # Wait until above command is not finished.
    engine.runAndWait()


def scrape_comments(num,comments,target,min_len,max_len):
    print("scraping comments ...")
    for comment in comments[:num]:
        #makes sure we take no bot comments
        if isinstance(comment, praw.models.Comment):
            if comment.author.name.endswith("[bot]"):
                continue
        if ((len(comment.body.split()) < max_len) and (len(comment.body.split()) > min_len)):
            target.append(comment.body)
            output["comment_ides"].append(comment.id) 
            num -= 1
        if(num) == 0:
            return 
            
def select_submission(subreddit,type,timer,field):
    if type == "top":
        submissions = reddit.subreddit(subreddit).top(time_filter=timer,limit=field)
    if type == "new":
        submissions = reddit.subreddit(subreddit).new(limit=field)
    if type == "hot":
        submissions = reddit.subreddit(subreddit).hot(limit=field)
    if type == "controvertial":
        submissions = reddit.subreddit(subreddit).controversial(limit=field)
    return submissions

def get_submission(subreddit,filter,field):
    print("getting submission ...")
    submissions = select_submission(subreddit,"hot",filter,field)
    print("going thought submissions ...")
    used_submissions = ides.get_ides()
    for submission in submissions:
        print("id : ",submission.id)
        if (submission.id not in used_submissions) and (not submission.over_18):
            return submission


def print_output():
    print("title : ",output["title"])
    print("<<",output["body"])
    print(">>")
    for comment in output["comments"]:
        print("==> ",comment)

def fetch_post_by_id(post_id,num_of_comments):
    post = reddit.submission(id=post_id)
    output["title"] = post.title
    output["body"] = post.selftext
    scrape_comments(num_of_comments,post.comments,output["comments"],5,150)


def fetch_posts(subreddit,field,num_of_comments,by_type):
    #field of search is how many seachrs to go through    
    #we use day filter and change as we like 
    submission = get_submission(subreddit,by_type,field)
    print("getting data from API ...")


    ides.write_id(submission.id)
    print("finale chosen : ",submission.id)
    scrape_comments(num_of_comments,submission.comments,output["comments"],5,150)
    output["title"] = submission.title
    output["id"] = submission.id
    output["body"] = submission.selftext
    output["url"] = submission.url
    print_output()



# no need to store title and body id they are the same as submission id 
output = {
        'id' : '',
        'title': "",
        "body": "",
        "comments" : [],
        "comment_ides" : [],
        "url" : ""
}




reddit = praw.Reddit(
    client_id=CID,
    client_secret=CS,
    user_agent="my_app  u/artechno",
    read_only = True
    #username="USERNAME",  
    #password="PASSWORD",
)




