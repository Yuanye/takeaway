var AppDispatcher = require('../dispatcher/TakeawayDispatcher');
var TakeawayConstants = require('../constants/TakeawayConstants');

var CartActions = {

	create: function(data) {
		AppDispatcher.dispatch({
			actionType: TakeawayConstants.CART_CREATE,
			data: data
		});
	},
	update: function(data) {
		AppDispatcher.dispatch({
			actionType: TakeawayConstants.CART_UPDATE,
			tata: data
		});

	},

};

module.exports = CartActions;