var React = require('react');
var OrderStateConstants = require('../constants/OrderStateConstants');
var OrderActions = require('../actions/OrderActions');

var Order = React.createClass({
	getInitialState: function(){
		return {
			id: this.props.data.id,
			state: this.props.data.state,
		};
	},
	cancle: function(){
		var state = -1
		this.setState({state: state})
		OrderActions.update({"id":this.state.id, "state": state})
	},

	render: function() {
		var CancleStyle = {display: "none"};
		console.log(this.state.state);
		if (this.state.state == 10) {
			CancleStyle = {}
		};
		return (
			<div className="order">
				<div className="detail">
					<div>
						<div className="order_id">订单编号: 
							<span className="order_detail_msg">{this.props.data.id}</span>
						</div>
						<div className="price">金&emsp;&emsp;额: 
							<span className="order_detail_msg">{this.props.data.total} 元</span>
						</div>
						<div className="consignee">收&nbsp;货&nbsp;人: 
							<span className="order_detail_msg">{this.props.data.consignee}</span>
						</div>
						<div className="address">地&emsp;&emsp;址:
							<span className="order_detail_msg">{this.props.data.address} </span>
						</div>
						<div className="created_at">时&emsp;&emsp;间: 
							<span className="order_detail_msg">{this.props.data.created_at}</span>
						</div>
						<div className="order_state">
							状&emsp;&emsp;态: <span className="order_detail_msg">{OrderStateConstants[this.state.state]}</span>

							<button style={CancleStyle} onClick={this.cancle}>取消</button>
						</div>
					</div>
				</div>

				<div className="goods">
					{this.props.data.foods.map(function(food){
							return  <div> 
										<div className="column food-name">
											名称:{food.name}
											
										</div>
										<div className="column food-price">
											小计（元）:{food.price}
										</div>
										<div className="column food-amount">
											数量:{food.amount}
										</div>
									</div>
						})
					} 
				</div>

			</div>
		);
	}

});

module.exports = Order;