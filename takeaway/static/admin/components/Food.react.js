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
		var amount = this.state.amount;
		return (
			<div className="food">
				<div className="cover">
					<img  src={food.cover} alt="" />
				</div>
				<div className="intro">
					{food.name}	
				</div>
				<div className="sale-info"> 月销售{food.records} 份</div>	
				<div className="price">¥{food.price}/份</div>

			</div>
		);
	}

});

module.exports = Food;