var React = require('react');
var AppActions = require('../actions/AppActions.js');

var App = React.createClass({
	handleClick: function() {
		AppActions.addTrans('this is the trans');
	},
	render: function() {
		return <p onClick={this.handleClick}>Hello world!</p>
	}
});

module.exports = App;