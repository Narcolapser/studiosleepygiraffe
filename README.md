# Studio Sleepy Giraffe

This website is purpose built to demonstrate my abilities as a programmer. For its size and purpose it is radically over engineered. Static content that gets saved with the site would have been far simplier, but would have said nothing of my abilities. This little website has multiple front ends and back ends that all interoperate with each other. The front ends show my experience with technologies like React and Flask, the back ends show my experience with Ruby and Python. The content provided by the backends is constructed from my code repositories. The result is a website that updates whenever I work on projects or write posts. Further details of how it all works below.

## Backends

Practically speaking, the Ruby and Python implementations of the API are the same. They differ linguistically but their output and how they generate it is done in the same way. This was easy to do since the languages are really quite similar in mentality and syntax. So I won't be highlighting them individually, but rather as a group.

The back, or api.studiosleepygiraffe.com, has 4 regions: projects, logs, posts, and feed. 

### Projects

This area gives a introduction to each of the projects that I am proud of. There are projects that I am currently working on towards the top and old projects that I thought were cool drift towards the bottom. Each of my code repositories has 4 components that make this possible. Two pngs: banner1.png and banner2.png, an info.json, and a README.md. This is visible [here](https://github.com/narcolapser/panerus). The banner pictures provide the background for the link, the info provides the meta data, and then the README.md (which you are currently reading) provides the text for the project page. In doing it this way I can make changes to my projects and have them automatically reflected in my website.

### Logs

This was one of my ealier ideas and I still really like it. With visual artists you can get an idea of how they think by looking at their source books. With programmers there isn't as easy a glimpse. Sure you can read the code I have written, but that doesn't tell you why I made the choices I did. By publishing my commit messages like so I have created a mechanism to give some insight into why I made the choices I made for the changes in the commit. It also has encouraged me to write meaningful commit messages. 

### Posts

I realized fairly early into my personal website project that I would need a place to put musings that weren't directy related to any specific project. So I created a blog repository where I write and commit posts. Like projects the content of the blog is generated from files and folder structure of my blog posts. Each post consists of a folder '2020-06-11' in which there are at least: cover.jpg, info.json, and post.md. Each of my posts is written in mark down just like a README.md to make it easy to have formatted content that I can write in CLI. Cover.jpg is the cover image for each post, and info.json holds the metadata, just like with projects. It is worth noting that I specifically do not have post date in info.json. This was done so that the folder name would control the publishing date and I have only one place to edit said date. The front end does not know this though. The publish date gets injected into info.json when the API reads it in and sends it to the front end.

### Feed

This is a newer feature. Agrigating across both posts and logs it gives a snapshot of the most recent activity on my website. There are two version of the feed: api.studiosleeypgiraffe.com/feed.rss and api.studiosleeypgiraffe.com/feed.json. The former to support older rss feed readers, the latter to support newer REST API applications. 

### Validation

One other item worth mentioning is I have a API validator as well. This is a little script that I can point at a webserver and validate it is compliant with my API specification. This is important to keep the two APIs identical. Any difference between the two would cause problems in my website.

## Frontends

Unlike the backends these are fairly different in implementation. I currently have two front ends: React.js and Flask (with plans for a few others as further demonstrations.) The objective is to none the less to have these two front ends as close to identical as possible. As the backend has a validator I have done something similar for the front end, I have a suit of selenium tests that are run to validate that the front ends are in compliance with each other. This is a looser concept, but it at least helps me ensure they are generally the same.

### React.js

A modern javascript frame work. Rendering done on the client side. This is a single page web app whcih, throught he magic of the React Router, has all the good of a multi-page web app but the responsiveness and lower over head o fa single page web app. After the inital static load from the web server, additional content is provided by api.studiosleepygiraffe.com, the backends listed above. 

### Flask (In progress)

A more traditional method of creating a web app. Rendering done on the server side with the client receiving flat HTML. This makes it a traditional multi-page web app. Every page gets loaded from the web server which also servers as its own backend generating the content the same way the python API does. 

# Enjoy

So now then, go explroe. Read my blog posts and my dev logs to get an idea of how I think, fork the projects that I have posted publicly, subscribe to my feed. 

Soli De Gloria
