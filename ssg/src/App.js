import React from "react";
import {
	BrowserRouter as Router,
	Switch,
	Route,
	Link
} from "react-router-dom";
import { Projects, GetProject} from './Projects.js'
import { DevLogs, GetDevLog } from './DevLogs.js'

// Params are placeholders in the URL that begin
// with a colon, like the `:id` param defined in
// the route in this example. A similar convention
// is used for matching dynamic segments in other
// popular web frameworks like Rails and Express.

export default function ParamsExample() {
	return (
		<Router>
			<div>
				<h2>Accounts</h2>

				<ul>
					<li>
						<Link to="/home">Home</Link>
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
					<Route exact path="/projects">
						<Projects />
					</Route>
					<Route path="/projects/:id" children={<GetProject />} />

					<Route path="/devlogs">
						<DevLogs />
					</Route>
					<Route path="/devlogs/:id" children={<GetDevLog />} />

				</Switch>
			</div>
		</Router>
	);
}
