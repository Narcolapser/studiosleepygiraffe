import React from "react";
import {
	Link,
	useParams
} from "react-router-dom";
import axios from 'axios'
import {Title, Verbage} from './Styles'
import ProjectLink from './ProjectLink'
const ReactMarkdown = require('react-markdown')

export class Projects extends React.Component {
	constructor(props) {
		super(props);
		this.state = {'projects': []};
	}

	render() {
		return (
			<div>
				<Title>Projects</Title>
				{this.state.projects
				.map(project => <ProjectLink name={project.name} url={project.url}
					link={"/projects"+project.url} description={project.description}/>)}
			</div>
		);
	}
	componentDidMount()
	{
		axios.get('http://api.studiosleepygiraffe.com/projects')
		.then(response => this.setState({'projects': response.data}));
	}
}

export class Project extends React.Component {
	constructor(props) {
		super(props);
		this.state = {'project': props.project,
						'markdown': ''}
	}

	render() {
		return (<Verbage><ReactMarkdown source={this.state.markdown}/></Verbage>);
	}

	componentDidMount() {
		axios.get('http://api.studiosleepygiraffe.com/projects/' + this.state.project + '/README.md')
			.then(response => this.setState({'markdown': response.data}));
	}
}

export function GetProject() {
	// We can use the `useParams` hook here to access
	// the dynamic pieces of the URL.
	let { id } = useParams();

	return (
		<div>
			<Project project={id}></Project>
		</div>
	);
}
