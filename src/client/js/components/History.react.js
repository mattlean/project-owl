var React = require('react');
var Link = require('react-router-component').Link;

var AppStore = require('../stores/AppStore.js');

var History = React.createClass({
	componentDidMount: function() {
		AppStore.getHistory(this.updateHistory);
	},

	updateHistory: function(data) {
		//console.log(data);
		this.setState(data);
	},

	render: function() {
		if(this.state !== null) {
			var ids = this.state.ids.map(function(id) {
				return <div>{id}</div>
			});
		
			return (
				<div id="id-list">
				<Link href="/" className="btn btn-success">Go to "transaction form"</Link>
				{ids}
				</div>
			)
		}

		return (
			<div>
				<Link href="/" className="btn btn-success">Go to "transaction form"</Link>
				empty
			</div>)
	}
});

module.exports = History;