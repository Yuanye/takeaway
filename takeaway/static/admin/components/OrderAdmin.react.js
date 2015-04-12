var React = require('react');
var OrderList = require('./OrderList.react');

var OrderAdmin = React.createClass({

	render: function() {
		return (
			<OrderList />
		);
	}

});

module.exports = OrderAdmin;