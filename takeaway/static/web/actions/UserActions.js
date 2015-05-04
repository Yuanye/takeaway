var AppDispatcher = require('../dispatcher/TakeawayDispatcher');
var TakeawayConstants = require('../constants/TakeawayConstants');

var UserActions = {

	signup: function(data) {
		AppDispatcher.dispatch({
			actionType: TakeawayConstants.USER_SIGNUP,
			data: data
		});
	},
	login: function(data) {
		console.log(TakeawayConstants.USER_LOGIN, "in actions");
		AppDispatcher.dispatch({
			actionType: TakeawayConstants.USER_LOGIN,
			data: data
		});

	},

};

module.exports = UserActions;