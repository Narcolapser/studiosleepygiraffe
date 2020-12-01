import React from "react";
import {
	Link,
	useParams
} from "react-router-dom";
// import axios from 'axios'
import styled from 'styled-components';
import {Title, Verbage, BoldFlatLink} from './Styles'
import { ssget } from './ssg_request.js'
const ReactMarkdown = require('react-markdown')

const BlogDiv = styled.div`
	position: relative;
	color: white;
	margin: 20px auto;
	background: rgb(51, 51, 51);
	padding: 2%;
	max-width: 50%;

	&:hover {
		background-color: #ddd;
		color: black;
	}
`

const CropHeight = styled.div`
	max-height: 150px;
	overflow: hidden;
`

const BlogLinkImg = styled.img`
	display: block;
	width: 100%;
	height: auto !important;
`

const CenterFloat = styled.div`
	position: absolute;
	width: auto;
	min-width: 92%;
	top: 40px;
	text-shadow: 4px 4px grey;
	font-size: 4vw;
`

export class Blog extends React.Component {
	constructor(props) {
		super(props);
		this.state = {'posts': []};
	}

	render() {
		return (
			<div>
				<Title>Weblog</Title>
					{this.state.posts
					.map(post => <BlogDiv key={post.date}>
							<BoldFlatLink to={"/blog/posts/"+post.date}>
								<CenterFloat>
									<center>{post.title}</center>
								</CenterFloat>
								<CropHeight>
									<BlogLinkImg src={'http://api.studiosleepygiraffe.com' + post.url + '/cover.jpg'} alt={post.cover_text} />
								</CropHeight>
							</BoldFlatLink>
						</BlogDiv>)}
			</div>
		);
	}
	componentDidMount()
	{
		ssget('http://api.studiosleepygiraffe.com/posts')
			.then(response => this.setState({'posts': response.data}));
	}
}


export class BlogPost extends React.Component {
	constructor(props) {
		super(props);
		this.state = {'markdown': '',
						'title': '',
						'info': {'tags':[],'files':[]}}
	}

	render() {
		let cover = <img alt="loading..."/>
		if (this.state.info.date !== undefined){
			cover = <img style={{'max-width': '100%'}} src={'http://api.studiosleepygiraffe.com/posts/' + this.state.info.date + '/cover.jpg'} alt={this.state.info.cover_text} />
		}
		return (
		<Verbage>
			<Title>{this.state.info.title}</Title>
			{ cover }
			<ReactMarkdown source={this.state.markdown}/>
			{this.state.info.files
			.map(file => <div key={file}><a href={'http://api.studiosleepygiraffe.com/posts/' + this.state.info.date + '/' + file}>{file}</a><br/></div>)}
			<p>Posted on: {this.state.info.date}</p>
			<ul>
				{this.state.info.tags
				.map(tag => <li key={tag}><Link to={"/blog/tags/"+tag}>{tag}</Link></li>)}
			</ul>
		</Verbage>);
	}

	componentDidMount() {
		ssget('http://api.studiosleepygiraffe.com/posts/' + this.props.post + '/post.md')
			.then(response => this.setState({'markdown': response.data}));
		ssget('http://api.studiosleepygiraffe.com/posts/' + this.props.post)
			.then(response => this.setState({'info': response.data}));

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
		this.state = {'posts': []}
	}

	render() {
		console.log(this.state);
		return (
			<div>
				<Title>Weblog: {this.props.tag}</Title>
					{this.state.posts
					.map(post => <BlogDiv key={post.date}>
							<BoldFlatLink to={"/blog/posts/"+post.date}>
								<CenterFloat>
									<center>{post.title}</center>
								</CenterFloat>
								<CropHeight>
									<BlogLinkImg src={'http://api.studiosleepygiraffe.com/posts/' + post.date + '/cover.jpg'} alt={post.cover_text} />
								</CropHeight>
							</BoldFlatLink>
						</BlogDiv>)}
			</div>
		);
	}

	componentDidMount() {
		ssget('http://api.studiosleepygiraffe.com/posts/tags/' + this.props.tag)
			.then(response => this.setState({'posts': response.data}));
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
