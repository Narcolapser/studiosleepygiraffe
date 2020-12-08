import React from "react";
import styled from 'styled-components';
import {
	useParams
} from "react-router-dom";
import axios from 'axios'
import { api_url } from './api_url.js'
import {Title, Verbage} from './Styles'
const ReactMarkdown = require('react-markdown')

export class Activity extends React.Component {
	constructor(props) {
		super(props);
		this.state = {'items': []};
	}

	render() {
		return (
			<div>
				<Title>Activity</Title>
				{this.state.items.map(item => <Item>
            <a href={item.link} key={item.title}>
              <h3>{item.title.includes('Merge branch') ? item.title.slice(0, item.title.indexOf('Merge branch') + 12) : item.title}</h3>
              <div>{item.date.slice(0,16)}</div>
            </a>
          </Item>)}
			</div>
		);
	}
	componentDidMount()
	{
		console.log(api_url() + '/feed.json');
		axios.get(api_url() + '/feed.json')
		.then(response => this.setState({'items': response.data.slice(0,4)}));
		//.then(response => console.log(response.data))
	}
}

export const Item = styled.div`
	max-width: 21%;
	margin: 0 2%;
	font-size: 28px;
	color: white;
  float: left;
	overflow: hidden;
`
