var AppDispatcher = require('../dispatcher/TakeawayDispatcher');
var EventEmitter = require('events').EventEmitter;
var assign = require('object-assign');

var TakeawayConstants = require('../constants/TakeawayConstants');
var LOGIN_URI = TakeawayConstants.API_URI + "login";
var SIGNUP_URI = TakeawayConstants.API_URI + "signup";
var ACCOUNT_URI = TakeawayConstants.API_URI + "account"

var $ = require('jquery');
$.ajaxSetup({
	async: false
});

var CHANGE_EVENT = 'change';

function account(data) {
	var a = null;
	
	$.get(ACCOUNT_URI, function(result) {
		a = result;
	});
	return a;
}

function login(data) {
	return $.post(LOGIN_URI, data, function(result) {
		return result;
	});
}

function signup(data) {
	return $.post(SIGNUP_URI, data, function(result) {
		return result;
	});
}

var UserStore = assign({}, EventEmitter.prototype, {
	account: function() {
		return account();
	},
	login: function() {
		return login();
	},
	signup: function() {
		return signup();
	},

	emitChange: function() {
		this.emit(CHANGE_EVENT);
	},

	addChangeListener: function(callback) {
		this.on(CHANGE_EVENT, callback);
	},

	removeChangeListener: function(callback) {
		this.removeListener(CHANGE_EVENT, callback);
	}
});


UserStore.dispatchToken = AppDispatcher.register(function(action) {
	var data;
	switch (action.actionType) {
		case TakeawayConstants.USER_LOGIN:
			data = action.data;
			login(data);
			UserStore.emitChange();
			break;

		case TakeawayConstants.USER_SIGNUP:
			data = action.data;
			signup(data);
			UserStore.emitChange();
			break;
		default:
			// no op
	}
});

module.exports = UserStore;