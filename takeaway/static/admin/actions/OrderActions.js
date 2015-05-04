var AppDispatcher = require('../dispatcher/TakeawayDispatcher');
var TakeawayConstants = require('../constants/TakeawayConstants');

var OrderActions = {

	create: function(data) {
		AppDispatcher.dispatch({
			actionType: TakeawayConstants.ORDER_CREATE,
			data: data
		});
	},
	update: function(data) {
		AppDispatcher.dispatch({
			actionType: TakeawayConstants.ORDER_UPDATE,
			data: data
		});

	},

};

module.exports = OrderActions;