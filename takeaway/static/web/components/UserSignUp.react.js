var React = require('react');
var UserActions = require('../actions/UserActions');
var UserStore = require('../stores/UserStore');
var TakeawayConstants = require('../constants/TakeawayConstants');

var UserSignUp = React.createClass({
	getInitialState: function(){
		return {
			error: false,
			name: null
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
		if (user) {
  			window.location.replace(TakeawayConstants.WEB_URI);
  		} else {
  			this.setState({"error": "注册失败！"})
  		};
	},

	render: function() {
		var ErrorStyle = {display: "none"};
		if (this.state.error) {
			ErrorStyle = {color: "red"}

		}
		return (
			<div className="col-sm-12">
				<div className="signup-form">
					<div className="signup-username">
						<label labelFor="name">
							<span>用户名：</span>	
						</label>
						<input ref="name"/>
					</div>
					<div className="signup-phone_num">
						<label labelFor="phone_um">
							<span>手机：</span>	
						</label>
						<input ref="phone_num"/>
					</div>
					<div className="signup-password">
						<label labelFor="password">
							<span>密码：</span>	
						</label>
						<input type="password" ref="password"/>
					</div>
					<div className="signup-error" style={ErrorStyle}>
						<label labelFor="error">
							<span>错误：{this.state.error}</span>	
						</label>
					</div>
					<div className="col-sm-5 save-button">
						<button
	                    	onClick={this._save}>
	                    	注册 
	            		</button>
					</div>
				</div>
			</div>
		);
	},
	_save: function() {
		this.setState({"error": false});
		var name = this.refs.name.getDOMNode().value;
		var phone_num = this.refs.phone_num.getDOMNode().value;
  		var password = this.refs.password.getDOMNode().value;
  		this.setState({"name": name});

  		UserActions.signup({
  			"password":password,
  			"phone_num":phone_num,
  			"name": name 
  		});
	}

});

module.exports = UserSignUp;