var AppDispatcher = require('../dispatcher/TakeawayDispatcher');
var TakeawayConstants = require('../constants/TakeawayConstants');

var FoodActions = {

	create: function(data) {
		AppDispatcher.dispatch({
			actionType: TakeawayConstants.FOOD_CREATE,
			data: data
		});
	},
	update: function(data) {
		AppDispatcher.dispatch({
			actionType: TakeawayConstants.FOOD_CREATE,
			data: data
		});

	},

};

module.exports = FoodActions;