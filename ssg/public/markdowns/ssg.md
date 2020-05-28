# Studio Sleepy Giraffe

I am a software developer, I did not want to deal with updating content on my website, rather I wanted it done automatically. Further, I'm very used to using git, and why not save the content of my website in a git repository? It simplifies moving the code around and allows me to keep a record. So I created a git repo to not only contain the HTML templates, static resources, etc. of Studio Sleepy Giraffe but also containt the scripts that automate the population of the website.

## Git-posting

One of the first utilities I created for the Studio Sleepy Giraffe website is one that converts git commit messages into json strings, formated like so:

``` json
{
    "flight_night": {
        "name": "Flight Night",
        "path": "/home/toben/Eurus/ssg projects/Flight Night",
        "posts": [
            {
                "author": "Toben Archer",
                "branch": "master",
                "date": "2017-03-20 21:01:16-05:00",
                "message": "Fixed number alignment and session scrunch.",
                "project": "Flight Night",
                "title": "Fixed number alignment and session scrunch."
            }
        ]
    }
}
```

These are processed in React (or Flask depending on the version of the site) to create the "Dev Log" section of SSG. The objective here was three fold:

1. Encourage me to make more meaningful commit messages. Since I knew people would potentially see my commit messages, this encouraged me to write messages that were meaningful. The hope being that some day this will serve as a type of blogging engine. Should I be working on a public facing project, those interested could check the devlog for that project. While I went about working on my projects, updates would automatically be thrown up. This leads to effortless blogging.
2. The second part of it is related. I often see with personal websites that the content goes stale. This would allow me to keep content fresh as it would be automatically thrown up as I worked on projects. So long as I had been working, content would be fresh.
3. Finally the purpose of this website is a professional portfolio. Meaning those who are considering hiring me would come to this site to learn a little about me, about the way I code. Having my git commit messages exposed gives a glimps of how I work. For an artist, it would be like letting my future employeer see my source/sketch books.

## Markdown preview

Continuing in the vein of my git-post system, I connected the app's discription page with the README.md of each project. This again allows me to modify the content of the website while inside my normal work flow. Further, it allows me to reuse the README.md that is being used for the publicly visible projects that are hosted on github, which saves work. This that you are reading right now is actually the README.md for my SSG git repository. Simple and elegant.
