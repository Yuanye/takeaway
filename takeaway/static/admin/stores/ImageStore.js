var AppDispatcher = require('../dispatcher/TakeawayDispatcher');
var EventEmitter = require('events').EventEmitter;
var assign = require('object-assign');

var TakeawayConstants = require('../constants/TakeawayConstants');
var UPLOAD_TOKEN_URI = TakeawayConstants.API_URI+ "uploads";
var QINIU_UPLOAD_URI = TakeawayConstants.QINIU_UPLOAD_URI;

var $ = require('jquery');
$.ajaxSetup({
	async: false,
	contentType: 'multipart/form-data'
});

var CHANGE_EVENT = 'change';

function getUploadToken(){
	var uptoken;
	$.get(UPLOAD_TOKEN_URI, function(result){
		uptoken = result;
	});
	return uptoken;
}

function create(data) {
	var url;
	var formData = new FormData();
	formData.append('token', data['token']);
	formData.append('key', data['key']);
	formData.append('file', data['file']);
	$.ajax({
		url: QINIU_UPLOAD_URI,
	    type: 'POST',
	    data: formData,
	    contentType: false,
	    processData:false,
	    success: function(result){
	    	url = TakeawayConstants.QINIU_IMAGE_URI +result.key;
	    }
	});
}

var ImageStore = assign({}, EventEmitter.prototype, {

	getUploadToken: function() {
		return getUploadToken();
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


ImageStore.dispatchToken = AppDispatcher.register(function(action) {
	var data;
	switch (action.actionType) {
		case TakeawayConstants.IMAGE_CREATE:
			data = action.data;
			create(data);
			ImageStore.emitChange();
			break;

		case TakeawayConstants.IMAGE_DELETE:
			delete(action.id);
			ImageStore.emitChange();
			break;

		default:
			// no op
	}
});

console.log(ImageStore.dispatchToken);
module.exports = ImageStore;