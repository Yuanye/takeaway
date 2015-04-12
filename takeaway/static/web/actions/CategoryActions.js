var AppDispatcher = require('../dispatcher/TakeawayDispatcher');
var TakeawayConstants = require('../constants/TakeawayConstants');

var CategoryActions = {

	create: function(data) {
		AppDispatcher.dispatch({
			actionType: TakeawayConstants.CATEGORY_CREATE,
			text: data
		});
	},
	update: function(data) {
		AppDispatcher.dispatch({
			actionType: TakeawayConstants.CATEGORY_UPDATE,
			text: data
		});

	},

};

module.exports = CategoryActions;