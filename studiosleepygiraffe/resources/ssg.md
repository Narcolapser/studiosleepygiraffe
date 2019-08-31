#Studio Sleepy Giraffe

I am a software developer; I did not want to deal with updating content on my website; instead, I wanted it done automatically. Further, I'm very used to using git, and why not save the content of my website in a git repository? It simplifies moving the code around and allows me to keep a record. So the repo I have created contains more than just Studio Sleepy Giraffe's HTML templates, static resources, etc.  The repo also includes the scripts that automate the population of the website.

## Git-posting

One of the first utilities I created for the Studio Sleepy Giraffe website is one that converts git commit messages into JSON strings, formated like so:

``` json
{
    "automatic-fiesta": {
        "description": "A system for automatically distributing code to satellite micropython nodes based on MAC address.",
        "name": "Automatic Fiesta",
        "path": "/home/toben/Code/ssg/automatic-fiesta",
        "posts": [
            {
                "author": "Toben Archer",
                "branch": "master",
                "date": "2016-06-01 02:39:05+00:00",
                "message": "There is a lot to do to hash it out and make it more robust and\nhave better performance. But it is feature complete with a telnet\nand web server that are both simple to use and extendable.\n\nTO THE KING!\n",
                "project": "Automatic Fiesta",
                "title": "Automatic fiesta is at it's first beta."
            },
}
```

These are processed in Flask to create the "Dev Log" section of SSG. The objective here was three-fold:

1. Encourage me to make more meaningful, commit messages. Since I knew people would potentially see my commit messages, this encouraged me to write meaningful messages. The hope is that someday, this will serve as a type of blogging engine. Should I be working on a public-facing project, those interested could check the devlog for that project. While I went about working on my projects, updates would automatically be thrown up. This automation leads to effortless blogging.
2. The second part of it is related. I often see with personal websites that the content goes stale. Automating, as mentioned in point one would allow me to keep content fresh as it would be automatically thrown up as I worked on projects. So long as I had been working, content would be fresh.
3. Finally, the purpose of this website is a professional portfolio. Meaning those who are considering hiring me would come to this site to learn a little about me, about the way I code. Having my git commit messages exposed gives a glimpse of how I work. For an artist, it would be like letting my future employer see my source/sketchbooks.

## Markdown preview

Continuing in the vein of my git-post system, I connected the app's description page with the README.md of each project. By using the README.md I am again modifying the content of the website while inside my typical workflow. The added benefit is that the README.md pulls double duty. Projects that I have GitHub hosting publicly also use the README.md for the home page of the project. This reuse saves me a little work in having to write the information twice. This page that you are reading right now is the README.md for my SSG git repository. Simple and elegant.
