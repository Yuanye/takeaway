var React = require('react');
var FoodList = require('./FoodList.react');
var FoodForm = require('./FoodForm.react');
var FoodActions = require('../actions/FoodActions');

var TakeawayConstants = require('../constants/TakeawayConstants');

var FoodAdmin = React.createClass({

	render: function() {
		return (
			<div >
				<FoodForm onSave={this.onSave} />
				<FoodList />
			</div>
		);
	},
	onSave: function(data) {
		console.log(data);
		FoodActions.create(data);
	}

});

module.exports = FoodAdmin;
