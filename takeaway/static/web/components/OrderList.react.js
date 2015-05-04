var React = require('react');
var Order = require('./Order.react');
var OrderStore = require('../stores/OrderStore');
var OrderStateConstants = require('../constants/OrderStateConstants');

var OrderList = React.createClass({
	getInitialState: function(){
		return {
			orders: OrderStore.getAll()
		};
	},

	render: function() {
		return (
			<div className="col-sm-12">
				{this.state.orders.map(function(result) {
					return <Order
					 	key={'cid_' + result.id } 
					 	data={result} /> 
				}, this)}


			</div>
		);
	}

});

module.exports = OrderList;