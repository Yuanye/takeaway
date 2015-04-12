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
                    Submit
            </button>
            </div>
		);
	},

	_save: function() {
		console.log("_save");

    	this.setState({
      		value: ''
    	});
  	},
});

module.exports = CategoryForm;