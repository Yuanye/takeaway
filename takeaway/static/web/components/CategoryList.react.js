
var Category = require('./Category.react');
var React = require('react');

var CategoryStore = require('../stores/CategoryStore');

var CategoryList = React.createClass({
	getInitialState: function(){
		return {
			categories: CategoryStore.getAll(),
		};
	},

	render: function() {
		return (
			<ul>
				{this.state.categories.map(function(result) {
					return <Category key={'cid_' + result.id} data={result} /> 
				})} 
			</ul>
		);
	},
	_onChange: function() {
		this.setState({
			categories: CategoryStore.getAll()
		});	
	}

});

module.exports = CategoryList;