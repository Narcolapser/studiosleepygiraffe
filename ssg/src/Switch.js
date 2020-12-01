import React from "react";
import styled from 'styled-components';
import Cookies from 'universal-cookie';


export class SwitchPanel extends React.Component {
	constructor(props) {
		super(props);
    this.cookies = new Cookies()
		this.state = {'api': this.cookies.get('api_switch')};
    this.api_change = this.api_change.bind(this);
	}

  api_change = (e) => {
    this.cookies.set('api_switch',e.target.value);
    console.log('Changed API to: ' + e.target.value);
    this.setState({'api':e.target.value});
  }

	render() {


    if (this.state.api === undefined)
    {
      console.log('well, best set it.');
      this.cookies.set('api_switch','ruby');
      this.setState({'api':'ruby'});
    }
    else {
      console.log('Currently using: ' + this.state.api);
    }

		return (
			<Panel>
        <input type="radio" id="ruby" name="api" value="ruby" checked={ this.state.api === 'ruby' } onChange={this.api_change}/>
        <label for="ruby">Ruby API</label>
        <br/>
        <input type="radio" id="python" name="api" value="python" checked={ this.state.api === 'python' } onChange={this.api_change}/>
        <label for="ruby">Python API</label>
			</Panel>
		);
	}
}

const Panel = styled.div`
	position: fixed;
	top: 200px;
	right: 0px;
	background-color: #333;
	color: white;
	padding: 10px;
`
