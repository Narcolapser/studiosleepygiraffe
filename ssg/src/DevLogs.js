import React from "react";
import {
	Link,
	useParams
} from "react-router-dom";
import axios from 'axios'

export class DevLogs extends React.Component {
	constructor(props) {
		super(props);
		this.state = {'projects': []};
	}
	
	render() {
		return (
			<div>
				<h2>Dev Log!</h2>
				<ul>
					{this.state.projects
					.map(project => <li key={project.url}><Link to={"/devlogs/"+project.url}>{project.name}</Link></li>)}
				</ul>
			</div>
		);
	}
	componentDidMount()
	{
		axios.get('/projects.json')
		.then(response => this.setState({'projects': response.data}));
	}
}


export class DevLog extends React.Component {
	constructor(props) {
		super(props);
		this.state = {'project': props.project,
						'logs': ''}
	}
	
	render() {
		return (<div> {this.state.logs} </div>);
	}
	
	componentDidMount() {
		axios.get('/logs/' + this.state.project + '.json')
			.then(response => this.setState({'logs': response.data}));
	}
}

export function GetDevLog() {
	// We can use the `useParams` hook here to access
	// the dynamic pieces of the URL.
	console.log("Hello there");
	let { id } = useParams();

	return (
		<div>
			<p>id: {id}</p>
		</div>
	);
}
