import React from "react";
import {
	Link,
	useParams
} from "react-router-dom";
import styled from 'styled-components';
import axios from 'axios'
import {Title, Verbage} from './Styles'

const FloatText = styled.div`
  position: absolute;
  top: 8px;
  left: 30px;
  text-shadow: black 3px 3px;
`

const BlockDiv = styled.div`
  position: relative;
  color: white;
  margin: 20px auto;
  background: rgb(51, 51, 51);
  padding: 2%;
  max-width: 50%;
`

const ProjectImg = styled.img`
  width: 50%;
  overflow: hidden;
  height: 200px;
`

export default class ProjectLink extends React.Component {
	constructor(props) {
		super(props);
	}

	render() {
		return (
			<BlockDiv>
        <Link to={this.props.link}>
          <FloatText>
            <h2>{this.props.name}</h2>
            <p>{this.props.description}</p>
          </FloatText>
          <ProjectImg src={'/static/' + this.props.url + '1.png'} />
          <ProjectImg src={'/static/' + this.props.url + '2.png'}/>
        </Link>
			</BlockDiv>
		);
	}
}
