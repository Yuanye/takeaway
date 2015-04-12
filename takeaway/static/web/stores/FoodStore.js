var AppDispatcher = require('../dispatcher/TakeawayDispatcher');
var EventEmitter = require('events').EventEmitter;
var assign = require('object-assign');

var TakeawayConstants = require('../constants/TakeawayConstants');
var FOOD_URI = TakeawayConstants.API_URI + "foods";

var $ = require('jquery');
$.ajaxSetup({
	async: false
});

var CHANGE_EVENT = 'change';


function getAll() {
	// 这里 data 先返回了, $是异步
	var data = [];
	$.get(FOOD_URI, function(result) {
		data = result;
	});
	return data;
}

var FoodStore = assign({}, EventEmitter.prototype, {

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


FoodStore.dispatchToken = AppDispatcher.register(function(action) {
	var data;
	switch (action.actionType) {
		case TakeawayConstants.FOOD_CREATE:

			data = action.data;
			create(data);
			FoodStore.emitChange();
			break;

		case TakeawayConstants.FOOD_UPDATE:
			data = action.data;
			update(data);
			FoodStore.emitChange();
			break;

		case TakeawayConstants.FOOD_DELETE:
			delete(action.id);
			FoodStore.emitChange();
			break;

		default:
			// no op
	}
});

module.exports = FoodStore;