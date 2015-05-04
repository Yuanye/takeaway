var React = require('react');
var CartActions = require('../actions/CartActions');
var TakeawayConstants = require('../constants/TakeawayConstants');

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
		var CART_URL = TakeawayConstants.WEB_URI+"#/carts"
		var food = this.props.data;
		var amount = this.state.amount;
		var AddAmountStyle = {width: "25px", float: "right"};
		if (amount > 0 ) {
			var reduceAmountStyle = {width: "25px",float: "left"};
			var CartStyle = {width: "70px",float: "right"};
			var AmountStyle = {width: "20px", float: "left", margin: "2px 0 0 1px"};

		} else {
			var reduceAmountStyle = {display: "none"};
			var CartStyle = {display: "none"};
			var AmountStyle = {display: "none"};
		}

		return (
			<div className="food">
				<div className="cover">
					<img  src={food.cover} alt="" />
				</div>
				<div className="intro">
					{food.name}	
				</div>
				<div className="sale-info"> 
					月销售{food.records} 份 
					<div style={CartStyle}>
						<a href={CART_URL}>去购物车</a>
					</div>
				</div>	
				<div className="buy">
					<div className="price">¥{food.price}/份</div>
					<div className="choose-amount">
						<div style={reduceAmountStyle}>
							<button onClick={this.reduceAmount} >-</button>
						</div>
						<div style={AmountStyle}>
							{this.state.amount}
						</div>
						<div style={AddAmountStyle}>
							<button onClick={this.addAmount} >+</button>
						</div>
						
					</div>
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