var AppDispatcher = require('../dispatcher/TakeawayDispatcher');
var EventEmitter = require('events').EventEmitter;
var assign = require('object-assign');

var TakeawayConstants = require('../constants/TakeawayConstants');
var CATEGORY_URI = TakeawayConstants.API_URI + "categories";

var $ = require('jquery');
$.ajaxSetup({ 
    async : false
});

var CHANGE_EVENT = 'change';

function create(data) {
	console.log(data);
	$.ajax({
		url: CATEGORY_URI, 
	    type: 'POST',
	    data: JSON.stringify(data),
	    contentType: 'application/json',
	    processData: false,
	    success: function(result){
	    	console.log(result);
	    }
	});
}

function getAll() {
	// 这里 data 先返回了, $是异步
	var data = [];
	$.get(CATEGORY_URI, function(result) {
		data = result;
	});
	return data;
}

function update(data) {
	return $.patch(CATEGORY_URI + "/" + data.id, data, function(result) {
		return result;
	});
}

function remove(data) {
	return $.delete(CATEGORY_URI + "/" + data.id, data, function(result) {
		return result;
	});
}

var CategoryStore = assign({}, EventEmitter.prototype, {

	getAll: function() {
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


CategoryStore.dispatchToken = AppDispatcher.register(function(action) {
	var data;
	switch (action.actionType) {
		case TakeawayConstants.CATEGORY_CREATE:

			data = action.data;
			create(data);
			CategoryStore.emitChange();
			break;

		case TakeawayConstants.CATEGORY_UPDATE:
			data = action.data;
			update(data);
			CategoryStore.emitChange();
			break;

		case TakeawayConstants.CATEGORY_DELETE:
			delete(action.id);
			CategoryStore.emitChange();
			break;

		default:
			// no op
	}
});

module.exports = CategoryStore;