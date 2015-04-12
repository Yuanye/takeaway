var React = require('react');

var Cart = React.createClass({
	propTypes: {
		data: React.PropTypes.object,
		id: React.PropTypes.string,
		food: React.PropTypes.object,
		amount: React.PropTypes.number,
		user_id: React.PropTypes.number,
		has_ordered: React.PropTypes.bool,
		created_at: React.PropTypes.string
	},
	getInitialState: function() {
		return {
			id: this.props.data.id,
			amount: this.props.data.amount,
			has_ordered: this.props.data.has_ordered
		};
	},

	render: function() {
		var food = this.props.data.food;
		return (
			<div>
				{this.props.id}|
				{food.name}|
				{food.price}|
				{food.amount}|
				<img src={food.cover} alt="" />
				{this.props.updated_at}
			</div>
		);
	}

});

module.exports = Cart;