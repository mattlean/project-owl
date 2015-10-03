var assign = require('react/lib/Object.assign');
var EventEmitter = require('events').EventEmitter;

var AppDispatcher = require('../dispatchers/AppDispatcher');
var AppConstants = require('../constants/AppConstants');

var CHANGE_EVENT = 'change';

var _transHistory = {};

function _dlHistory(callback) {
	$.ajax({
		url: '/transaction',
		dataType: 'json',
		cache: false,
		success: function(data) {
			_transHistory = data;
			callback(_transHistory);
		}.bind(this),
		error: function(xhr, status, err) {
			console.log(this.props.url, status, err.toString());
		}.bind(this)
	});
}

var AppStore = assign(EventEmitter.prototype, {
	emitChange: function() {
		this.emit(CHANGE_EVENT);
	},

	addChangeListener: function(callback) {
		this.on(CHANGE_EVENT, callback);
	},

	removeChangeListener: function(callback) {
		this.removeListener(CHANGE_EVENT, callback);
	},

	getHistory: function(callback) {
		_dlHistory(callback);
	},

	dispatcherIndex: AppDispatcher.register(function(payload) {
		var action = payload.action; // action from handleViewAction

		switch(action.actionType) {
			case AppConstants.ADD_TRANS:
				_addItem(payload.action.item);
				break;
		}

		AppStore.emitChange();
		return true;
	})
});

module.exports = AppStore;
