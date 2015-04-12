var React = require('react');

var Cart = React.createClass({

	render: function() {
		return (
			<div>
				<input type="checkbox" name="" id=""/>
				{this.props.data.id}
				创建时间: {this.props.data.created_at}/
				数量: {this.props.data.amount}/
				<img src={this.props.data.food.cover} alt="" />	
				{this.props.data.food.name}
				单价：{this.props.data.food.price}元		
				共计：{this.props.data.amount* this.props.data.food.price}元
			</div>
		);
	}

});

module.exports = Cart;