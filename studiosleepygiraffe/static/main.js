let {Router, Route, Link, browserHistory, useParams, Switch} = window.ReactRouter;

class Index extends React.Component {
	render() {
		return (
			<div>
				<div className="banner">
					<img
						className="header"
						src="/static/img/inverted_SSG.jpg"
						title="Studio Sleepy Giraffe logo"
						style={{'display':'block','marginLeft':'auto','marginRight': 'auto','width': '466px'}}
						/>
				</div>
				<ul>
					<li><Link to='/home'>Home</Link></li>
					<li><Link to='/projects'>Projects</Link></li>
					<li><Link to='/devlog'>DevLog</Link></li>
					<li><Link to='/blog'>Blog</Link></li>
				</ul>
				{this.props.children}
			</div>
		);
	}
}

class Home extends React.Component {
	render() {
		return (
			<div style={{maxWidth:"50%",margin:"0 auto",fontSize:"28px",color:"white"}}>
				<h1 style={{textAlign:"center"}}>The mind behind<br/>Studio Sleepy Giraffe</h1>
				<img className="about_picture" src="/static/img/face.jpeg" style={{float:"left",width:"50%",margin:"20px"}}/>
				<p>I am Toben <a href="https://github.com/narcolapser">"Narcolapser"</a> Archer. I work as a software developer by day and the same by night as a hobby. At home I work primarily in Python and Kivy making apps for Android and PC. This website, made with Flask and React, is setup primarily as a professional website. It is my personal website for sharing my work with friends, family, and potential employeers. To see what projects I have been working on click on the "Projects" tab in the nav bar. To read my mind (see what I was thinking as I worked on the various projects) go to the "Developers Log" page and select a project to read all of the development log for that project. To read longer stories covering various topics try the "Blog" tab.
				</p>
				<p>Resume: <a href="/resume/html">HTML</a> or <a href="/resume/Toben_Archer.pdf">PDF Download</a></p>
			</div>
		);
	}
}

const Project  = ({ match }) => (
	// here's a nested div
	<div>
		Looking up project: {match.url}
	</div>
)

function ProjectLink(props)
{
	return (
		<a href={"/projects/" + props.url}>
			<div style={{position:"relative",color:"white",padding:"10px",margin:"20px 0px",background:"#333"}} onClick={props.onClick}>
				<div style={{position:"absolute",top:"8px",left:"16px",textShadow:"3px 3px black"}}>
					<h2>{props.name}</h2>
					<p>{props.description}</p>
				</div>
				<img src={"/static/img/" + props.url + "1.png"} style={{width:"50%",overflow:"hidden",height:"200px"}}/>
				<img src={"/static/img/" + props.url + "2.png"} style={{width:"50%",overflow:"hidden",height:"200px"}}/>
			</div>
		</a>
	);
}

class Projects extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			displayAll: true,
			project: '',
			projectTitle: '',
			projects: []
			};
	}
	
	componentDidMount(){
		this.loadAll()
	}
	
	loadAll(){
		var req = new XMLHttpRequest();
		req.open("GET", "/projects.json",false);
		req.send()
		let content = JSON.parse(req.responseText);
		this.setState({projects:content,displayAll:true,project:'',projectTitle:''});
	}
	
	renderProjects(){
		var links = [];
		
		for(let i = 0; i < this.state.projects.length; i++)
		{
			links.push(<ProjectLink
				url={this.state.projects[i].url}
				name={this.state.projects[i].name}
				description={this.state.projects[i].description}
				onClick={() => this.handleClick(i)}/>);
		}
		return links;
	}
	
	renderProject(){
		return this.state.project;
	}
	render() {
		return (
			<div  style={{maxWidth:"50%",margin:"0 auto",fontSize:"28px",color:"white"}}>
				<h1 style={{textAlign:"center"}}>Projects</h1><hr/>
				START PROJECTS
				{this.renderProjects()}
				END PROJECTS
			</div>
		);
	}
}

class ProjectDisp extends React.Component {
	render() {
		let { id } = useParams();
		return (
			<div>ID: {id}</div>
		);
	}
}

class DevLog extends React.Component {
	render() {
		return (
			<div>DevLog</div>
		);
	}
}

class Blog extends React.Component {
	render() {
		return (
			<div>Blog</div>
		);
	}
}

function Child() {
  // We can use the `useParams` hook here to access
  // the dynamic pieces of the URL.
  let { id } = useParams();

  return (
    <div>
      <h3>ID: {id}</h3>
    </div>
  );
}

ReactDOM.render((
	<Router history={browserHistory}>
		<Route path='/' component={Index}>
			<Route path='home' component={Home}/>
			<Route path='projects' component={Projects}/>
			<Route path='devlog' component={DevLog}/>
			<Route path='blog' component={Blog}/>
		</Route>
		<Switch>
			<Route path="/projects/:id" children={ProjectDisp}/>
		</Switch>
	</Router>
	), document.getElementById('content')
);
