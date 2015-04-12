var AppDispatcher = require('../dispatcher/TakeawayDispatcher');
var TakeawayConstants = require('../constants/TakeawayConstants');

var CategoryActions = {

	create: function(data) {
		AppDispatcher.dispatch({
			actionType: TakeawayConstants.CATEGORY_CREATE,
			data: data
		});
	},
	update: function(data) {
		AppDispatcher.dispatch({
			actionType: TakeawayConstants.CATEGORY_CREATE,
			data: data
		});

	},

};

module.exports = CategoryActions;