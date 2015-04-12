var React = require('react');
var CartActions = require('../actions/CartActions');

var Food = React.createClass({
	propTypes: {
    	data: React.PropTypes.object,
    	id: React.PropTypes.number,
    	name: React.PropTypes.string,
    	category: React.PropTypes.object,
    	price: React.PropTypes.number,
    	cover: React.PropTypes.string,
    	records: React.PropTypes.number,
    	createdAt: React.PropTypes.string
	},

	getInitialState: function(){
		return {
			amount: 0,
		};
	},

	render: function() {
		var food = this.props.data;
		console.log(this.state.amount);
		var amount = this.state.amount;

		if (amount > 0 ) {
			var reduceAmountStyle = {};
			var AmountStyle = {}
		} else {
			var reduceAmountStyle = {display: "none"};
			var AmountStyle = {display: "none"};
		}

		return (
			<div className="food">
				{food.id}
				{food.name}		
				{food.price}		
				{food.createdAt}
				<img src={food.cover} alt="" />		

				<div className="choose-amount">
					<button onClick={this.reduceAmount} style={reduceAmountStyle}>-</button>
					<div style={AmountStyle}>
						{this.state.amount}
					</div>
					<button onClick={this.addAmount}>+</button>
				</div>
			</div>
		);
	},
	reduceAmount: function() {
		var food_id = this.props.data.id;
		var amount = this.state.amount -1;
		this.setState({"amount": amount});
		this.addToCart({"food_id": food_id, "amount": amount});
	},
	addAmount: function() {
		var food_id = this.props.data.id;
		var amount = this.state.amount + 1;
		this.setState({"amount": amount});
		this.addToCart({"food_id": food_id, "amount": amount});
	},
	addToCart:function(data) {
		CartActions.create(data);
	}

});

module.exports = Food;