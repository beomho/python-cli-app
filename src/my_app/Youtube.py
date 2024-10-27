from googleapiclient.discovery import build
from jproperties import Properties

configs = Properties()

with open('../src/my_app/app-config.properties', 'rb') as config_file:
    configs.load(config_file)

DEVELOPER_KEY = configs.get("DEVELOPER_KEY").data

class Youtube():
    def __init__(self,query,maxResults):
        self.query=query
        self.maxResults=maxResults

    def search_videos(self):
        youtube = build('youtube', 'v3', developerKey=DEVELOPER_KEY)
        request = youtube.search().list(part='id', type='video', q=self.query, maxResults=self.maxResults)
        response = request.execute()
        return response

    def get_video_details(self,count,video_id):
        youtube = build('youtube', 'v3', developerKey=DEVELOPER_KEY)
        request = youtube.videos().list(part='snippet,statistics', id=video_id)
        details = request.execute()
        title = details['items'][0]['snippet']['title']
        #print(f'Title of video {count}: {title}')
        
    def get_title(self,count,video_id):
        youtube = build('youtube', 'v3', developerKey=DEVELOPER_KEY)
        request = youtube.videos().list(part='snippet,statistics', id=video_id)
        details = request.execute()
        title = details['items'][0]['snippet']['title']
        
        return title 

    def main(self):
        results = self.search_videos()
        video_list=results['items']
        resultArr = {}
        for i in range(len(video_list)):
            video_id=video_list[i]['id']['videoId']
            title = self.get_title(i+1,video_id)
            resultArr[title] = 'https://www.youtube.com/watch?v={0}'.format(video_id)

        return resultArr
            
#query = 'Gfg'
#maxResults= 10
#obj=Youtube(query,maxResults)
#obj.main()

