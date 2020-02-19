import React from "react";
import {
	BrowserRouter as Router,
	Switch,
	Route,
	Link,
	useParams
} from "react-router-dom";
import axios from 'axios'

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
						<Link to="/devlog">Dev Log</Link>
					</li>
					<li>
						<Link to="/blog">Blog</Link>
					</li>
				</ul>

				<Switch>
					<Route exact path="/projects">
						<Projects />
					</Route>
					<Route path="/projects/:id" children={<Child />} />
				</Switch>
			</div>
		</Router>
	);
}

class Projects extends React.Component {
	constructor(props) {
		super(props);
		this.state = {'projects': []};
	}
	
	render() {
		return (
			<div>
				<h2>Projects!</h2>
				<ul>
					<li>
						<Link to="/projects/ssg">Studio Sleepy Giraffe</Link>
					</li>
					<li>
						<Link to="/projects/O365">Office 365</Link>
					</li>
					<li>
						<Link to="/projects/gduel">Gravity Duel</Link>
					</li>
				</ul>
				{this.state.projects.map(project => <p>{project.name}</p>)}
			</div>
		);
	}
	componentDidMount()
	{
		axios.get('/projects.json')
		.then(response => this.setState({'projects': response.data}));
	}
}

function Child() {
	// We can use the `useParams` hook here to access
	// the dynamic pieces of the URL.
	let { id } = useParams();

	return (
		<div>
			<h3>ID: {id}</h3>
		</div>
	);
}

