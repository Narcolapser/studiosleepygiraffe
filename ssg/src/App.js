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
import {Title, Verbage} from './Styles'
import styled from 'styled-components';

// Params are placeholders in the URL that begin
// with a colon, like the `:id` param defined in
// the route in this example. A similar convention
// is used for matching dynamic segments in other
// popular web frameworks like Rails and Express.
const NavBar = styled.div`
	overflow: hidden;
	background-color:#222;
`

const NavLink = styled(Link)`
	float: left;
	color: #f2f2f2;
	text-align: center;
	padding: 14px 0px;
	text-decoration: none;
	font-size: 17px;
	background-color: #333;
	margin-left: 1%;
	margin-right: 1%;
	width: 23%;

	&:hover {
		background-color: #ddd;
		color: black;
	}

	&.active {
		background-color: #ddd
		coor: black;
	}
	`
const FacePanel = styled.img`
	float: left;
	width: 50%;
	margin: 20px;
`

export default function ParamsExample() {
	return (
		<div>
			<div>
				<img
				src="/inverted_SSG.jpg"
				title="Studio Sleepy Giraffe logo"
				alt="Studio Sleepy Giraffe logo"
				style={{'display':'block','marginLeft':'auto','marginRight': 'auto','width': '466px'}}/>
			</div>
			<Router>
				<div>
					<NavBar >
						<NavLink to="/">Home</NavLink>
						<NavLink to="/projects">Projects</NavLink>
						<NavLink to="/logs">Dev Log</NavLink>
						<NavLink to="/blog">Blog</NavLink>
					</NavBar>

					<Switch>
						<Route exact path="/">
							<Verbage>
								<Title>The man behind <br/>the giraffe</Title>
								<FacePanel className="about_picture" src="/face.jpeg"/>
								<p>I am Toben <a href="https://github.com/narcolapser">"Narcolapser"</a> Archer. I work as a software developer by day and the same by night as a hobby. At home, I work primarily in Python and React, making apps for Android and PC. This website, built with React, is set up mostly as a professional website. It is my website for sharing my work with friends, family, and potential employers. To see what projects I have been working on, click on the "Projects" tab. To read my mind (see what I was thinking as I worked on the various projects), go to the "Developers Log" page and select a project to read all of the development logs for that project. To read longer stories covering various topics, try the "Blog" tab.</p>
								<p>Resume: <a href="/Toben_Archer.pdf">PDF Download</a></p>
							</Verbage>
						</Route>
						<Route exact path="/projects">
							<Projects />
						</Route>
						<Route path="/projects/:id" children={<GetProject />} />

						<Route exact path="/logs">
							<DevLogs />
						</Route>
						<Route path="/logs/:id" children={<GetDevLog />} />

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
