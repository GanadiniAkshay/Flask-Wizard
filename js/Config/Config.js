import React from 'react';

class Config extends React.Component{
    constructor(props){
        super(props);
        this.state = {}
    }

    render(){
        return (
            <div className="fluid-container" style={{"height":"100%"}}>
                <nav style={{"backgroundColor":"#7A7A7A"}}>
                    <div className="nav-wrapper">
                    <a href="#" className="brand-logo" style={{"marginLeft":"10px"}}>Flask-Wizard</a>
                    <ul id="nav-mobile" className="right hide-on-med-and-down">
                        <li className="active"><a href="#">Home</a></li>
                        <li><a target="_blank" href="http://flask-wizard.readthedocs.io/en/latest/" className="waves-effect waves-light btn" style={{"color":"black","backgroundColor":"white"}}>Docs</a></li>
                    </ul>
                    </div>
                </nav>
                <div className="row" style={{"height":"100%"}}>
                    <div className="col s9" style={{"height":"100%"}}>
                        <div className="row" style={{"backgroundColor":"red","height":"30%","marginBottom":"0"}}></div>
                        <div className="row" style={{"backgroundColor":"green","height":"70%"}}></div>
                    </div>
                    <div className="col s3" style={{"backgroundColor":"blue","height":"100%"}}>
                    </div>
                </div>
            </div>
        )
    }
}

export default Config;