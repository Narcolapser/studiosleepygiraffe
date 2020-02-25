import React from "react";
import {
	Link,
	useParams
} from "react-router-dom";
import axios from 'axios'
const ReactMarkdown = require('react-markdown')

export class Blog extends React.Component {
	constructor(props) {
		super(props);
		this.state = {'posts': []};
	}
	
	render() {
		return (
			<div>
				<h2>Dev Log!</h2>
				<ul>
					{this.state.posts
					.map(post => <li key={post.date}><Link to={"/blog/posts/"+post.date}>{post.title}</Link></li>)}
				</ul>
			</div>
		);
	}
	componentDidMount()
	{
		axios.get('/posts.json')
		.then(response => this.setState({'posts': response.data}));
	}
}


export class BlogPost extends React.Component {
	constructor(props) {
		super(props);
		this.state = {'post': props.post,
						'markdown': ''}
	}
	
	render() {
		return (<ReactMarkdown source={this.state.markdown}/>);
	}

	componentDidMount() {
		axios.get('/blog/' + this.state.post + '.md')
			.then(response => this.setState({'markdown': response.data}));
	}
}

export function GetBlogPost() {
	// We can use the `useParams` hook here to access
	// the dynamic pieces of the URL.
	let { id } = useParams();

	return (
		<div>
			<BlogPost post={id} />
		</div>
	);
}

export class BlogTag extends React.Component {
	constructor(props) {
		super(props);
		this.state = {'project': props.project,
						logs: {description:'',
								name:'',
								url:'',
								posts:[]}}
	}

	render() {
		return (<div> {this.state.logs.posts.map((post) => {
			return (<div>
						<h3>{post.title}</h3>
						<p>{post.message}</p>
					</div>)})} 
			</div>);
	}
	
	componentDidMount() {
		axios.get('/logs/' + this.state.project + '.json')
			.then(response => this.setState({'logs': response.data}));
	}
}

export function GetBlogTag() {
	// We can use the `useParams` hook here to access
	// the dynamic pieces of the URL.
	let { id } = useParams();

	return (
		<div>
			<BlogTag tag={id} />
		</div>
	);
}
