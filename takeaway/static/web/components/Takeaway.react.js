var React = require('react');
var CategoryList = require('./CategoryList.react');
var FoodList = require('./FoodList.react');
var TakeawayConstants = require('../constants/TakeawayConstants');

var CategoryForm = require('./CategoryForm.react');

var Takeaway = React.createClass({

	render: function() {
		return (
			<div>
				<CategoryList source={TakeawayConstants.API_URI + "categories"}/>
				<FoodList source={TakeawayConstants.API_URI + "foods"}/>
				<CategoryForm onSave={this._onSave} />
			</div>
		);
	},
	_onSave: function  () {
		// body...
	}

});

module.exports = Takeaway;