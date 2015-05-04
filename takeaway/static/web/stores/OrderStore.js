var AppDispatcher = require('../dispatcher/TakeawayDispatcher');
var EventEmitter = require('events').EventEmitter;
var assign = require('object-assign');

var TakeawayConstants = require('../constants/TakeawayConstants');
var ORDER_URI = TakeawayConstants.API_URI + "orders";

var $ = require('jquery');
$.ajaxSetup({
	traditional: true,
	async: false
});

var CHANGE_EVENT = 'change';


function getAll() {
	var data = [];
	$.get(ORDER_URI, function(result) {
		data = result;
	});
	return data;
}

function create(data) {
	return $.post(ORDER_URI, data, function(result) {
		return result;
	});
}

function update(data) {
	return $.post(ORDER_URI+"/"+data.id, data, function(result) {
		console.log(data);
		return result;
	});
}

var OrderStore = assign({}, EventEmitter.prototype, {

	getAll: function() {
		return getAll();
	},
	create: function(data){
		return create(data);
	},
	update: function(data){
		return update(data);
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


OrderStore.dispatchToken = AppDispatcher.register(function(action) {
	var data;
	switch (action.actionType) {
		case TakeawayConstants.ORDER_CREATE:
			data = action.data;
			create(data);
			OrderStore.emitChange();
			break;

		case TakeawayConstants.ORDER_UPDATE:
			data = action.data;
			update(data);
			OrderStore.emitChange();
			break;

		default:
			// no op
	}
});

module.exports = OrderStore;