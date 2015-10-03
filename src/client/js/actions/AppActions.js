var AppConstants = require('../constants/AppConstants.js');
var AppDispatcher = require('../dispatchers/AppDispatcher.js');

var AppActions = {
	addTrans: function(item) {
		AppDispatcher.handleViewAction({
			actionType: AppConstants.ADD_TRANS,
			item: item
		})
	}
};

module.exports = AppActions;
