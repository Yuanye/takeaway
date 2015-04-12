var React = require('react');
var CategoryActions = require('../actions/CategoryActions');

var Category = React.createClass({
	propTypes: {
    	data: React.PropTypes.object.isRequired
	},
	getInitialState: function(){
		return {id: this.props.data.id }
	},

	render: function() {
		return (
			<li >
				<a href={"/category/"+ this.props.data.id} > {this.props.data.name}</a> 
			</li>
			); 
	},

	_onSave: function(){
		CategoryActions.update(data);
    	this.setState({isEditing: false});
	},
});

module.exports = Category;