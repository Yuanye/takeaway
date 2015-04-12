var React = require('react');

var CategoryForm = React.createClass({
	propTypes: {
		value: React.PropTypes.string,
		placeholder: React.PropTypes.string
	},

	getInitialState: function() {
		return {
			placeholder: "请输入分类",
		};
	},

	render: function() {
		return (
			<div>
			<input ref="name"/>
			<button
                    onClick={this._save}>
                    Add 
            </button>
            </div>
		);
	},

	_save: function() {
		var name = this.refs.name.getDOMNode().value;
		this.props.onSave({"name": name});
    	this.setState({
      		value: ''
    	});
  	},
});

module.exports = CategoryForm;