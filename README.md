# youtube_views_thumbnail

### Real-time thumbnail upload program using YouTubeAPI 
<br>

# build & install

first you need python3
```
sudo apt update
sudo apt upgrade
sudo apt install python3 python3-pip
```
then clone to my repository
```
cd ~/
git clone https://github.com/thsvkd/youtube_views_thumbnail.git
cd youtube_views_thumbnail

pip install -r requirements.txt
```

before you run the program, you need to make several Youtube API projects (8 projects recommend)

Create and set up a Google project with the following links:

https://cloud.google.com/resource-manager/docs/creating-managing-projects?hl=ko

<br>

Go to the 'Library' tab and click on "YouTube Data API v3" to enable it.

![2020-08-28_12-04-49](https://user-images.githubusercontent.com/53033449/91516688-1398d180-e927-11ea-8661-735e7d784937.png)
https://console.developers.google.com/apis

<br>

![2020-08-28_12-10-29](https://user-images.githubusercontent.com/53033449/91516865-81dd9400-e927-11ea-889c-38bdd86be5f8.png)
![2020-08-28_12-11-42](https://user-images.githubusercontent.com/53033449/91516929-ab96bb00-e927-11ea-88be-2cb75a3bbefe.png)


<br>


Go to the User Authentication tab, click Create User Credentials, and then click Create AOAuth Client.
![2020-08-28_12-26-48](https://user-images.githubusercontent.com/53033449/91517920-f6b1cd80-e929-11ea-8e1b-f33bf41c01ec.png)

<br>

If the 'OAuth consent screen' appears, select 'External' for the user type, define the name of your application, and click the Add button from the scope of Google API to add all of the YouTube-related APIs.

![2020-08-28_12-31-45](https://user-images.githubusercontent.com/53033449/91518137-76d83300-e92a-11ea-9933-596e58c98eaa.png)
![2020-08-28_12-31-10](https://user-images.githubusercontent.com/53033449/91518138-793a8d00-e92a-11ea-8d7f-19e2bd71b091.png)

<br>

They make eight identical projects.
![a멀티프로젝트 만든모습](https://user-images.githubusercontent.com/53033449/91518465-493fb980-e92b-11ea-81f9-5ecf314e93fa.jpg)

after make eight projects, download each OAuth 2.0 client token json file from an individual project

![2020-08-28_12-38-46](https://user-images.githubusercontent.com/53033449/91518579-8906a100-e92b-11ea-9bf2-46625c312cd2.png)

Open the OAuth 2.0 client token json file, paste the contents of the json file to 'client_secrets.json' file(you will be have 8 json file of 8 OAuth 2.0 clients)

Upload the video to YouTube and remember the ID of the video. <br>
https://youtu.be/ "S04vCSDLG88s" <- this is video ID.

run program with next command
```
python thumbnail_generator.py --video-id *YOUR_VIDEO_ID* --file BG_sample.png --noauth_local_webserver
```

If you run the program for the first time, the user authentication window will appear.

![2020-08-28_13-27-35](https://user-images.githubusercontent.com/53033449/91521278-45636580-e932-11ea-9233-647e3eb4a9e9.png)

It is a successed if the thumbnail_generator.py(NUM)-outh2.json file has been created after all authentication.

You can see that the thumbnail is uploaded well after all the certifications are completed.
![2020-08-28_13-37-45](https://user-images.githubusercontent.com/53033449/91521864-ac354e80-e933-11ea-9e46-2ae72fc3b629.png)
![2020-08-28_13-38-39](https://user-images.githubusercontent.com/53033449/91521903-cbcc7700-e933-11ea-99fa-eccea7615519.png)


if you want to edit text, that display at the thumbnail, modify this code
```
text = "이 영상의 조회수는\n%s 입니다 \n 지금 시간은 %02d시 %02d분" % (viewCount, today.hour, today.minute)
font_size = 250
font_color = "ff847c"
font_style = "BlackHanSans"
img_name = ""
img_size = 1
```

if you want edit term of upload, modify this
```
update_term = 120
```

### _As a result of the test, it has been confirmed that Google blocks several projects with the same purpose. So you can have only one YouTube API project per account. If you want to run this project, you'll have to use multiple accounts for multiple projects._