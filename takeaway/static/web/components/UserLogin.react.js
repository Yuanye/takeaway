var React = require('react');
var UserActions = require('../actions/UserActions');
var UserStore = require('../stores/UserStore');
var TakeawayConstants = require('../constants/TakeawayConstants');

function isEmptyObject(obj){
    for (var n in obj) {
        return false
    }
    return true; 
} 

var UserLogin = React.createClass({
	getInitialState: function(){
		return {
			error: false
		};
	},
	componentDidMount: function() {
		UserStore.addChangeListener(this._onChange);
  	},
  	componentWillUnmount: function() {
        UserStore.removeChangeListener(this._onChange);
    },
    _onChange: function() {
    	var user = UserStore.account();
		if (!isEmptyObject(user)){
  			window.location.replace(TakeawayConstants.WEB_URI);
  		} else {
  			this.setState({"error": "登录失败！"})
  		};
	},

	render: function() {
		var ErrorStyle = {display: "none"};
		if (this.state.error) {
			ErrorStyle = {color: "red"}

		};
		return (
			<div className="col-sm-12">
				<div className="login-form">
					<div className="login-username">
						<label labelFor="name">
							<span>用户名：</span>	
						</label>
						<input ref="name"/>
					</div>
					<div className="login-password">
						<label labelFor="password">
							<span>密码：</span>	
						</label>
						<input type="password" ref="password"/>
					</div>
					<div className="login-error" style={ErrorStyle}>
						<label labelFor="error">
							<span>错误：{this.state.error}</span>	
						</label>
					</div>
					<div className="col-sm-5 save-button">
						<button
	                    	onClick={this._save}>
	                    	登录 
	            		</button>
					</div>
				</div>
			</div>
		);
	},

	_save: function() {
		var name = this.refs.name.getDOMNode().value;
  		var password = this.refs.password.getDOMNode().value;
  		console.log(name, password);
  		UserActions.login({
  			"password":password,
  			"name": name 
  		});
	}

});

module.exports = UserLogin;