import React from 'react';
import axios from 'axios';

class Config extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            "channels": {},
            "author":"",
            "config_route": "/",
            "mongo": {
                "log": true,
                "mongo_uri": ""
            },
            "name": "",
            "nlp": {
                "key": "",
                "name": ""
            },
            "redis": {
                "host": "",
                "password": "",
                "port": ""
            },
            "button":"Save",
            "restart":false,
            "restart_needed":false
        }

        this.nameChange = this.nameChange.bind(this);
        this.authorChange = this.authorChange.bind(this);
        this.configChange = this.configChange.bind(this);
        this.saveConfig = this.saveConfig.bind(this);
    }

    componentDidMount(){
        var that = this;
        axios.get('/api/config')
        .then(function (response) {
            var resp = response.data;

            that.setState({"name":resp.name,"author":resp.author,"config_route":resp.config_route,"channels":resp.channels,"mongo":resp.mongo,"nlp":resp.nlp,"redis":resp.redis});
            console.log(that.state);
        })
        .catch(function (error) {
            console.log(error);
        });

        $(document).ready(function() {
            M.updateTextFields();
        });
    }

    nameChange(){
        var name = document.getElementById('bot_name').value;
        this.setState({"name":name})
    }

    authorChange(){
        var author = document.getElementById('author_name').value;
        this.setState({"author":author})
    }

    configChange(){
        var config_route = document.getElementById('config_route').value;
        this.setState({"config_route":config_route,"restart_needed":true})
    }

    saveConfig(){
        this.setState({"button":"Saving"})
        var payload = {
            "name": this.state.name,
            "author":this.state.author,
            "config_route":this.state.config_route,
            "channels":this.state.channels,
            "nlp":this.state.nlp,
            "redis":this.state.redis,
            "mongo":this.state.mongo
        }

        var that = this;
        axios.post('/api/config', payload)
          .then(function (response) {
            if (response.status == 200){
                that.setState({"button":"Save"})
                if (that.state.restart_needed){
                    that.setState({"restart":true});
                }
            }else{
                that.setState({"button":"Error"})
            }
          })
          .catch(function (error) {
            that.setState({"button":"Error"})
          });
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
                        <div className="row" style={{"minHeight":"20%","marginBottom":"0"}}>
                            <br/>
                            {this.state.restart?<h6 style={{"marginLeft":"20px","textAlign":"centre","color":"red"}}>Restart the flask server to see the changes</h6>:null}
                            <div className="input-field col s4">
                                <input type="text" value={this.state.name} id="bot_name" onChange={this.nameChange}/>
                                <label htmlFor="bot_name" className="active">Bot Name</label>
                            </div>
                            <div className="input-field col s4">
                                <input type="text" value={this.state.author} id="author_name" onChange={this.authorChange}/>
                                <label htmlFor="author_name" className="active">Author Name</label>
                            </div>
                            <div className="input-field col s4">
                                <input type="text" value={this.state.config_route} id="config_route" onChange={this.configChange}/>
                                <label htmlFor="config_route" className="active">Config Route</label>
                            </div>
                            <div className="col s4">
                                <a className="waves-effect waves-light btn" style={{"backgroundColor":"black"}} onClick={this.saveConfig}>{this.state.button}</a>
                            </div>
                        </div>
                        <div className="row" style={{"backgroundColor":"green","minHeight":"80%"}}></div>
                    </div>
                    <div className="col s3" style={{"backgroundColor":"blue","height":"100%"}}>
                    </div>
                </div>
            </div>
        )
    }
}

export default Config;