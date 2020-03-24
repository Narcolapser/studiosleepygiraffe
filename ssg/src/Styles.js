import styled from 'styled-components';
import {Link} from "react-router-dom";

export const Title = styled.h1`
	text-align: center;
	color: white;
`

export const SubTitle = styled.h2`
	text-align: center;
	color: white;
`

export const Verbage = styled.div`
	max-width: 50%;
	margin: 0 auto;
	font-size: 28px;
	color: white;
`

export const BoldFlatLink = styled(Link)`
	color: black;
	font-weight: bold;
	&:visited {
		color: black;
	}
`
