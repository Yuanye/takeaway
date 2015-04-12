var React = require('react');
var CategoryList = require('./CategoryList.react');
var CategoryForm = require('./CategoryForm.React');

var CategoryActions = require('../actions/CategoryActions');

var TakeawayConstants = require('../constants/TakeawayConstants');

var CategoryAdmin = React.createClass({

	render: function() {
		return (
			<div>
				<CategoryForm onSave={this.onSave}/>
				<CategoryList />
			</div>
		);
	},
    onSave: function(data) {
    	CategoryActions.create(data);
    }

});

module.exports = CategoryAdmin;