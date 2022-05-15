![_Simple-Scribe](https://user-images.githubusercontent.com/84144584/168478365-88fae434-a6a6-4846-a49d-ac8a8004872c.png)

## Overview :sparkles:
## Inspiration

_Accessibility_ was the inspiration behind Simple Scribe. Many users suffer from physical ailments that hinder their ability to accomplish simple tasks such as writing and typing. As a result, we wanted to create a website that is simple and intuitive enough to be used by anyone.

## What it does

Simple Scribe is a website that generates a text transcript of an audio recording and provides a translation of the said transcript. Simply upload the file to the website, and the user will be sent back the transcript and translation in the form of text.

## How we built it
### Frontend
The frontend refers to the part of the application that is seen by the end user. For this aspect of the project, the design was extremely important. To accomplish this we used **Javascript, jquery, ajax, dropzone.js, HTML, CSS, Distributed Compute Protocol (DCP), and Bootstrap.**

To make our website dynamic we used dropzone.js for a simple drag and drop feature, ajax to send HTTP requests for users, and DCP to integrate monetization.

### Backend
The backend is the part of the application that handles processing and is not seen by the end. For this **Flask** a python based framework, **AssemblyAI API** was used to handle the scripts that are responsible for converting the audio to text. The site simply requests the API to convert the uploaded audio file.

### Miscellaneous Components
There were also aspects of this project that go beyond frontend, and backend. For this, we used **Cookies, Multithreading, AssemblyAI API.** 

## Challenges we ran into

Since we are new to web development, one challenge that took a while to fix was the problem of sending server updates to the client. After doing some research, we used a technique called Server-Sent Events to send the transcription result back to the user. Another issue that we ran into was to being able to host multiple users at the same time. This was important to be working, so we had to make sure multithreading was in use, or else only a single user can use it a time which is not ideal or scalable in the real world.

The biggest issue we ran into is hosting the website using firebase. If further time was permitted, this would be the main issue that we would've tackled.

## Accomplishments that we're proud of

We are proud of the website we made since it was most of our first time doing web development. However, what we enjoyed most was the process of collaborating together to build a beautiful website, a backend that can service multiple users, and a website that provides a useful service that is practical yet meaningful.

## What we learned

We learned a lot about backend web development, particularly with flask, frontend web design using CSS, ajax, and bootstrap; source control using git; AssemblyAI and DCP's API systems; and Server-Sent Events. These were all new skills that we picked up, and are now comfortable using which may aid us in our future pursuits and projects we decide. Furthermore, we also enjoyed communicating and sharing ideas. 

## What's next for SimpleScribe Website

Going further with this project, We want to use AssemblyAi's real-time transcription service to improve the transcription speed and be able to host the website as well. 


## Example 
![gifforsite](https://user-images.githubusercontent.com/84144584/168483395-15c88c39-2624-4ffc-8947-01169f84ab8c.gif)


_Simple-Scribe in action_



## Development :computer:
### Requirements
- Python 3.10

### Setup
Install virtual environment
```sh
$ pip install pipenv
```

Run virtual environment
```sh
$ pipenv shell
```

Install dependencies
```sh
$ pipenv install -r requirements.txt
```

Provide environment variables ~ Create .env file

### Usage
```sh
$ python main.py
```

