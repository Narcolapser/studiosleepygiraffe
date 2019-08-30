function NavBarItem(props){
    return (
        <a className={props.status} href={props.link} onClick={props.onClick}>{props.title}</a>
    )
}

class NavBar extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            home: "active",
            projects: "inactive",
            devlog: "inactive",
            blog: "inactive",
            about: "inactive"
            }
    }
    render()
    {
        return (
        <div className="topnav">
            <NavBarItem status={this.state.home} href="/" title="Home" onClick={() => this.handleClick("home")}/>
            <NavBarItem status={this.state.projects} href="/projects" title="Projects" onClick={() => this.handleClick("projects")}/>
            <NavBarItem status={this.state.devlog} href="/devlog" title="Developers Log" onClick={() => this.handleClick("devlog")}/>
            <NavBarItem status={this.state.blog} href="/blog" title="Blog" onClick={() => this.handleClick("blog")}/>
            <NavBarItem status={this.state.about} href="/about" title="About Me" onClick={() => this.handleClick("about")}/>
        </div>
            );
    }
    handleClick(item)
    {
        this.setState({
            home:item == "home" ? "active" : "inactive",
            projects:item == "projects" ? "active" : "inactive",
            devlog:item == "devlog" ? "active" : "inactive",
            blog:item == "blog" ? "active" : "inactive",
            about:item == "about" ? "active" : "inactive"});
        
        {/*Not elegant but it works for now*/}
        if (item == "home")
            this.props.onHome();
        if (item == "projects")
            this.props.onProjects();
        if (item == "devlog")
            this.props.onDevlog();
        if (item == "blog")
            this.props.onBlog();
        if (item == "about")
            this.props.onAbout();
    }
}

function Home(props)
{
    return (
    <div style={{maxWidth:"50%",margin:"0 auto",fontSize:"28px",color:"white"}} className={props.className}>
        <h1 style={{textAlign:"center"}}>Studio Sleepy Giraffe</h1>
        <p>Where the wizard falls asleep standing up.</p><br/>
        <p>This is my personal website for sharing my work with friends, family, and potential employeers. To see what projects I have been working on click on the "Projects" tab in the nav bar. To read my mind (see what I was thinking as I worked on the various projects) go to the "Dev Log" page and select a project to read all of the development log for that project.
        </p>
</div>);
}

function About(props)
{
    return (
    <div style={{maxWidth:"50%",margin:"0 auto",fontSize:"28px",color:"white"}} className={props.className}>
        <h1 style={{textAlign:"center"}}>The mind behind<br/>Studio Sleepy Giraffe</h1>
        <img className="about_picture" src="/static/face.jpeg" style={{float:"left",width:"50%",margin:"20px"}}/>
        <p>I am Toben "Narcolapser" Archer. I work as a software developer by day and the same by night as a hobby. At home I work primarily in Python and Kivy making apps for Android and PC. This website, made with Flask and React, is setup primarily as a professional website. It is here so that I can point potential employeers or partners to something to get a little information about me.</p>
        
        <p>Resume: <a href="/resume/html">HTML</a> or <a href="/resume/Toben_Archer.pdf">PDF Download</a></p>
    </div>
    );
}

function Project(props)
{
    return (
    <div style={{position:"relative",color:"white",padding:"10px",margin:"20px 0px",background:"#333"}} onClick={props.onClick}>
        <div style={{position:"absolute",top:"8px",left:"16px",textShadow:"3px 3px black"}}>
            <h2>{props.name}: {props.url}</h2>
            <p>{props.description}</p>
        </div>
        <img src={"/static/" + props.url + "1.png"} style={{width:"50%",overflow:"hidden",height:"200px"}}/>
        <img src={"/static/" + props.url + "2.png"} style={{width:"50%",overflow:"hidden",height:"200px"}}/>
    </div>
    );
}

class Projects extends React.Component {
    constructor(props) {
        super(props)
    }
    render()
    {
        return (
            <div>Projects</div>
            );
    }
}

function LogPost(props)
{
    return (
        <div>
            <h2>{props.title}</h2>
            <p style={{whiteSpace:"pre-wrap"}}>{props.message}</p>
            <p>written: {props.date} by: {props.author} on branch: {props.branch}</p>
        </div>
    );
}

class DevLog extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            projects:[],
            posts:[],
            displayAll: true,
            project: ''
        };
    }

    componentDidMount(){
        this.loadAll()
    }
    
    loadAll(){
        var req = new XMLHttpRequest();
        req.open("GET", "/projects.json",false);
        req.send()
        var content = JSON.parse(req.responseText);
        this.setState({projects:content,posts:[],displayAll:true,project:''});
    }
    
    handleClick(project){
        var req = new XMLHttpRequest();
        req.open("GET", "/devlog/" + this.state.projects[project].url + ".json",false);
        req.send()
        var content = JSON.parse(req.responseText);
        this.setState({projects:[],posts:content,displayAll:false,project:this.state.projects[project].name});
    }
    
    renderProjects(){
        var links = [];
        
        for(let i = 0; i < this.state.projects.length; i++)
        {
            links.push(<Project
                url={this.state.projects[i].url}
                name={this.state.projects[i].name}
                description={this.state.projects[i].description}
                onClick={() => this.handleClick(i)}/>);
        }
        return links;
    }
    
    renderPosts(){
        var posts = [];
        
        for(let i=0; i < this.state.posts.length; i++)
        {
            posts.push(LogPost(this.state.posts[i]));
        }
        return posts;
    }

    render()
    {
        return (
        <div style={{maxWidth:"50%",margin:"0 auto",fontSize:"28px",color:"white"}} className={this.props.className}>
            <h1 style={{textAlign:"center"}}>The mind behind<br/>Studio Sleepy Giraffe</h1>
                <p>These development logs are the comments I have made as I work on my projects. They are actually made up of the commit messages from the repo for each project. This has encouraged me to have meaningful commit messages as they are effectively my way of blogging about my project as I work on it. The best part is that because they are commit messages, new posts are just part of my natural workflow. For more information see the apps page for "Studio Sleepy Giraffe."</p><hr/>
            <div style={{display:this.state.displayAll ? '' : 'hidden'}}>
                {this.renderProjects()}
            </div>
            <div style={{display:this.state.displayAll ? 'hidden' : ''}}>
                <h1 style={{textAlign:"center"}}>{this.state.project}</h1>
                <button onClick={() => this.loadAll()}>Back</button>
                {this.renderPosts()}
            </div>
        </div>
            );
    }
}

class Blog extends React.Component {
    constructor(props) {
        super(props)
    }
    render()
    {
        return (
            <div>Blog</div>
            );
    }
}

class SSG extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            home: "showing",
            projects: "hidden",
            devlog: "hidden",
            blog: "hidden",
            about: "hidden"
            }
    }
    render()
    {
        return (
            <div className="root">
                <div className="banner">
                    <img
                        className="header"
                        src="/static/inverted_SSG.jpg.bak"
                        title="Studio Sleepy Giraffe logo"
                        style={{'display':'block','marginLeft':'auto','marginRight': 'auto','width': '466px'}}
                        />
                </div>
                {/*Not elegant but it works for now*/}
                <NavBar 
                    onHome={() => this.handleContentChange("home")}
                    onProjects={() => this.handleContentChange("projects")}
                    onDevlog={() => this.handleContentChange("devlog")}
                    onBlog={() => this.handleContentChange("blog")}
                    onAbout={() => this.handleContentChange("about")}/>
                <div>
                    <Home className={this.state.home}>home</Home>
                    <Projects className={this.state.projects}>projects</Projects>
                    <DevLog className={this.state.devlog}>devlog</DevLog>
                    <Blog className={this.state.blog}>blog</Blog>
                    <About className={this.state.about}>about</About>
                </div>
            </div>
        );
    }
    
    handleContentChange(item)
    {
        console.log("Changing content: " + item);
        this.setState({
            home:item == "home" ? "showing" : "hidden",
            projects:item == "projects" ? "showing" : "hidden",
            devlog:item == "devlog" ? "showing" : "hidden",
            blog:item == "blog" ? "showing" : "hidden",
            about:item == "about" ? "showing" : "hidden",});
    }
}

ReactDOM.render(
  <SSG />,
  document.getElementById('root')
);

