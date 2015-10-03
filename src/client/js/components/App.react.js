var React = require('react');
var AppActions = require('../actions/AppActions.js');

var TransForm = require('./TransForm.react.js');

var App = React.createClass({
	handleClick: function() {
		AppActions.addTrans('this is the trans');
	},
	render: function() {
		return <TransForm />
	}
});

module.exports = App;