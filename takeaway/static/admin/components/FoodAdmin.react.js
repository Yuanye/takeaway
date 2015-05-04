var React = require('react');
var FoodList = require('./FoodList.react');
var FoodForm = require('./FoodForm.react');
var FoodActions = require('../actions/FoodActions');

var TakeawayConstants = require('../constants/TakeawayConstants');

var FoodAdmin = React.createClass({

	render: function() {
		return (
			<div className="col-sm-10">
				<FoodForm onSave={this.onSave} />
				<FoodList />
			</div>
		);
	},
	onSave: function(data) {
		FoodActions.create(data);
	}

});

module.exports = FoodAdmin;
