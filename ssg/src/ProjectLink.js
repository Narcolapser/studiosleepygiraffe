import React from "react";
import styled from 'styled-components';
import {BoldFlatLink} from './Styles'
import { api_url } from './api_url.js'

const FloatText = styled.div`
  position: absolute;
  top: 8px;
  left: 30px;
	text-shadow: 4px 4px grey;
	font-size: 2vw;
`

const BlockDiv = styled.div`
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

const ProjectImg = styled.img`
  width: 50%;
  overflow: hidden;
  height: 200px;
`

export default class ProjectLink extends React.Component {
	render() {
		return (
			<BlockDiv>
        <BoldFlatLink to={this.props.link}>
          <FloatText>
            <h2>{this.props.name}</h2>
            <p>{this.props.description}</p>
          </FloatText>
          <ProjectImg src={api_url() + this.props.url.replace('log','project') + '/banner1.png'} />
          <ProjectImg src={api_url() + this.props.url.replace('log','project') + '/banner2.png'} />
        </BoldFlatLink>
			</BlockDiv>
		);
	}
}
