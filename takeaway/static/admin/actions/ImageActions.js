var AppDispatcher = require('../dispatcher/TakeawayDispatcher');
var TakeawayConstants = require('../constants/TakeawayConstants');

var ImageActions = {
	create: function(data) {
		AppDispatcher.dispatch({
			actionType: TakeawayConstants.IMAGE_CREATE,
			data: data
		});
	},
	update: function(data) {
		AppDispatcher.dispatch({
			actionType: TakeawayConstants.IMAGE_CREATE,
			data: data
		});

	},

};

module.exports = ImageActions;