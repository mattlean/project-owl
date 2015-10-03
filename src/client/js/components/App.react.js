var React = require('react');
var Router = require('react-router-component');
var Locations = Router.Locations;
var Location = Router.Location;

var AppActions = require('../actions/AppActions.js');
var TransForm = require('./TransForm.react.js');
var Test = require('./Test.react.js');

var App = React.createClass({
	render: function() {
		return (
			<Locations>
				<Location path="/" handler={TransForm} />
				<Location path="/test" handler={Test} />
			</Locations>
		)
	}
});

module.exports = App;