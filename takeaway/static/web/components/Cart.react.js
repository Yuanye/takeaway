var React = require('react');

var Cart = React.createClass({
	getInitialState: function(){
		return {
			isChecked: false,
		};
	},
	render: function() {
		return (
			<div className="cart">
					<div className="column t-checkbox">
						<input 
							onChange={this._onChange} 
							type="checkbox" 
							name="carts" 
							value={this.props.data.id} 
							checked={this.state.isChecked}
							refs="carts"
							id=""/>
					</div>
					<div className="column t-goods">
						<img className="p-img" src={this.props.data.food.cover} alt=""/>
						{this.props.data.food.name}
					</div>
					<div className="column t-price">
						{this.props.data.food.price}元
					</div>
					<div className="column t-quantity">
						{this.props.data.amount}
					</div>

			</div>
		);
	},

	_onChange: function() {
		var isChecked = !this.state.isChecked;
		this.setState({isChecked: isChecked});
		if (isChecked) {
			this.props.onSelect();
		} else {
			this.props.onUnSelect();

		}
	}

});

module.exports = Cart;