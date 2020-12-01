import React from "react";
import {
	useParams
} from "react-router-dom";
// import axios from 'axios'
import { ssget } from './ssg_request.js'
import {Title, SubTitle, Verbage} from './Styles'
import ProjectLink from './ProjectLink'

export class DevLogs extends React.Component {
	constructor(props) {
		super(props);
		this.state = {'projects': []};
	}

	render() {
		console.log(JSON.stringify(this.state.projects))
		return (
			<div>
				<Title>Development Log</Title>
				<Verbage>
These development logs are the comments I have made as I work on my projects. They are actually made up of the commit messages from the repo for each project. This has encouraged me to have meaningful commit messages as they are effectively my way of blogging about my project as I work on it. The best part is that because they are commit messages, new posts are just part of my natural workflow. For more information see the apps page for "Studio Sleepy Giraffe."
				</Verbage>
				{this.state.projects
				.map(project => <ProjectLink name={project.name} url={project.url}
					link={project.url} description={project.description}/>)}
			</div>
		);
	}
	componentDidMount()
	{
		ssget('http://api.studiosleepygiraffe.com/logs/')
		.then(response => this.setState({'projects': response.data}));
	}
}


export class DevLog extends React.Component {
	constructor(props) {
		super(props);
		this.state = {'project': props.project,
						logs: {description:'',
								name:'',
								url:'',
								posts:[]}}
	}

	render() {
		return (<Verbage> {this.state.logs.posts.map((post) => {
			return (<div>
						<SubTitle>{post.title}</SubTitle>
						<p>{post.message}</p>
						<p>Commited on {post.date}</p>
					</div>)})}
			</Verbage>);
	}

	componentDidMount() {
		console.log(JSON.stringify(this.state));
		console.log('http://api.studiosleepygiraffe.com/logs/' + this.state.project);
		ssget('http://api.studiosleepygiraffe.com/logs/' + this.state.project)
			.then(response => this.setState({'logs': response.data}));
	}
}

export function GetDevLog() {
	// We can use the `useParams` hook here to access
	// the dynamic pieces of the URL.
	let { id } = useParams();

	return (
		<div>
			<DevLog project={id} />
		</div>
	);
}
