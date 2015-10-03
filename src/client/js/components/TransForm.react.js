var React = require('react');
var Link = require('react-router-component').Link;

var AppActions = require('../actions/AppActions.js');

var TransForm = React.createClass({
	handleClick: function() {
		AppActions.addTrans('this is the trans');
	},
	render: function() {
		return (
			<form action="/transaction" method="post">
				<Link href="/history" className="btn btn-success">Go to "history"</Link>
				<h2>New Transaction</h2>
				<div className="form-group">
					<label>
						Cost
						<input type="number" name="cost" className="form-control" required />
					</label>
				</div>
				<div className="form-group">
					<label>
						Date
						<input type="date" name="date" placeholder="2015-10-02" className="form-control" required />
					</label>
				</div>
				<div className="form-group">
					<label>
						Category
						<input type="text" name="category" className="form-control" />
					</label>
				</div>
				<div className="form-group">
					<label>
						Business
						<input type="text" name="business" className="form-control" />
					</label>
				</div>
				<div className="form-group">
					<label>
						Payment
						<input type="text" name="payment" className="form-control" />
					</label>
				</div>
				<div className="form-group">
					<label>
						Comment
						<textarea name="comment" className="form-control"></textarea>
					</label>
				</div>
				<button type="submit" onClick={this.handleClick} className="btn btn-default">Submit</button>
			</form>
		)
	}
});

module.exports = TransForm;
