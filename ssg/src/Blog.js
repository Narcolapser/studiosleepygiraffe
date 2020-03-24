import React from "react";
import {
	Link,
	useParams
} from "react-router-dom";
import axios from 'axios'
import styled from 'styled-components';
import {Title, Verbage, BoldFlatLink} from './Styles'
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
	width: 100%;
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
					.map(post => <BlogDiv>
							<BoldFlatLink to={"/blog/posts/"+post.date}>
								<CenterFloat>
									<center>{post.title}</center>
								</CenterFloat>
								<CropHeight>
									<BlogLinkImg src={'/blog/covers/' + post.cover} />
								</CropHeight>
							</BoldFlatLink>
						</BlogDiv>)}
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
		this.state = {'markdown': '',
						'title': '',
						'info': {'tags':[]}}
	}

	render() {
		return (
		<Verbage>
			<Title>{this.state.info.title}</Title>
			<img src={'/blog/covers/' + this.state.info.cover} />
			<ReactMarkdown source={this.state.markdown}/>
			<p>On {this.state.info.date}</p>
			<ul>
				{this.state.info.tags
				.map(tag => <li key={tag}><Link to={"/blog/tags/"+tag}>{tag}</Link></li>)}
			</ul>
		</Verbage>);
	}

	componentDidMount() {
		axios.get('/blog/' + this.props.post + '.md')
			.then(response => this.setState({'markdown': response.data}));
		axios.get('/blog/' + this.props.post + '.json')
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
		return (
			<div>
				<h1>{this.props.tag}</h1>
				<ul>
					{this.state.posts.map(post =>
						<li key={post.id}><Link to={"/blog/posts/"+post.id}>{post.title}</Link></li>
					)}
				</ul>
			</div>);
	}

	componentDidMount() {
		axios.get('/blog/tags/' + this.props.tag + '.json')
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
