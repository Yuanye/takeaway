var AppDispatcher = require('../dispatcher/TakeawayDispatcher');
var EventEmitter = require('events').EventEmitter;
var assign = require('object-assign');

var TakeawayConstants = require('../constants/TakeawayConstants');
var CART_URI = TakeawayConstants.API_URI + "carts";

var $ = require('jquery');
$.ajaxSetup({
	async: false
});

var CHANGE_EVENT = 'change';

function create(data) {
	console.log(data);
	return $.post(CART_URI, data, function(result) {
		return result;
	});
}

function getAll() {
	// 这里 data 先返回了, $是异步
	var data = [];
	$.get(CART_URI, function(result) {
		data = result;
	});
	return data;
}

var CartStore = assign({}, EventEmitter.prototype, {

	getAll: function() {
		return getAll();
	},
	getAllByCategoryId: function(categoryId) {
		return getAll();
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


CartStore.dispatchToken = AppDispatcher.register(function(action) {
	var data;
	switch (action.actionType) {
		case TakeawayConstants.CART_CREATE:
			console.log("in action loop");

			data = action.data;
			create(data);
			CartStore.emitChange();
			break;

		case TakeawayConstants.CART_UPDATE:
			data = action.data;
			update(data);
			CartStore.emitChange();
			break;

		case TakeawayConstants.CART_DELETE:
			delete(action.id);
			CartStore.emitChange();
			break;

		default:
			// no op
	}
});

module.exports = CartStore;