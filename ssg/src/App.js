import React from "react";
import {
	BrowserRouter as Router,
	Switch,
	Route,
	Link
} from "react-router-dom";
import { Projects, GetProject} from './Projects.js'
import { DevLogs, GetDevLog } from './DevLogs.js'
import { Blog, GetBlogTag, GetBlogPost} from './Blog.js'

// Params are placeholders in the URL that begin
// with a colon, like the `:id` param defined in
// the route in this example. A similar convention
// is used for matching dynamic segments in other
// popular web frameworks like Rails and Express.

export default function ParamsExample() {
	return (
		<div>
			<div>
				<img
				src="inverted_SSG.jpg"
				title="Studio Sleepy Giraffe logo"
				style={{'display':'block','marginLeft':'auto','marginRight': 'auto','width': '466px'}}/>
			</div>
			<Router>
				<div>
					<ul>
						<li>
							<Link to="/">Home</Link>
						</li>
						<li>
							<Link to="/projects">Projects</Link>
						</li>
						<li>
							<Link to="/devlogs">Dev Log</Link>
						</li>
						<li>
							<Link to="/blog">Blog</Link>
						</li>
					</ul>

					<Switch>
						<Route exact path="/">
							<div style={{maxWidth:"50%",margin:"0 auto",fontSize:"28px",color:"black"}}>
								<h1 style={{textAlign:"center"}}>The mind behind<br/>Studio Sleepy Giraffe</h1>
								<img className="about_picture" src="/face.jpeg" style={{float:"left",width:"50%",margin:"20px"}}/>
								<p>I am Toben <a href="https://github.com/narcolapser">"Narcolapser"</a> Archer. I work as a software developer by day and the same by night as a hobby. At home, I work primarily in Python and React, making apps for Android and PC. This website, built with React, is set up mostly as a professional website. It is my website for sharing my work with friends, family, and potential employers. To see what projects I have been working on, click on the "Projects" tab. To read my mind (see what I was thinking as I worked on the various projects), go to the "Developers Log" page and select a project to read all of the development logs for that project. To read longer stories covering various topics, try the "Blog" tab.</p>
								<p>Resume: <a href="/Toben_Archer.pdf">PDF Download</a></p>
							</div>
						</Route>
						<Route exact path="/projects">
							<Projects />
						</Route>
						<Route path="/projects/:id" children={<GetProject />} />

						<Route exact path="/devlogs">
							<DevLogs />
						</Route>
						<Route path="/devlogs/:id" children={<GetDevLog />} />

						<Route exact path="/blog">
							<Blog />
						</Route>
						<Route path="/blog/tags/:id" children={<GetBlogTag />} />
						<Route path="/blog/posts/:id" children={<GetBlogPost />} />

					</Switch>
				</div>
			</Router>
		</div>
	);
}
