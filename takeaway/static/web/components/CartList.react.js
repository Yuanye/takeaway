var React = require('react');

var CartStore = require('../stores/CartStore');
var Cart = require('./Cart.react');
var OrderActions = require('../actions/OrderActions');
var TakeawayConstants = require('../constants/TakeawayConstants');


var CartList = React.createClass({
	getInitialState: function(){
		var categoryId = this.props.params.categoryId;
		return {
			carts: CartStore.getAll(),
			cart_ids: Array()
		};
	},

	componentDidMount: function() {
		CartStore.addChangeListener(this._onChange);
  	},
  	componentWillUnmount: function() {
        CartStore.removeChangeListener(this._onChange);
    },
    componentWillReceiveProps: function(){
    },

    onSelect: function(id) {
    	this.state.cart_ids.push(id);
  	},
    onUnSelect: function(id) {
    	this.state.cart_ids.pop(id);
  	},
  	_onChange: function() {
  		// body...
  	},
  	_save: function () {
  		var consignee = this.refs.consignee.getDOMNode().value;
  		var phone_num = this.refs.phone_num.getDOMNode().value;
  		var address = this.refs.address.getDOMNode().value;
  		OrderActions.create({
  			"cart_ids": this.state.cart_ids,
  			"consignee": consignee,
  			"phone_num": phone_num,
  			"address": address
  		});
  		window.location.replace(TakeawayConstants.WEB_URI+"#/orders");
  	},
	render: function() {
		

		return (
			<div className="col-sm-12">

				<div className="col-sm-7 cart-main">
					<div className="cart cart-thead">
						<div className="column t-checkbox">选择</div>
						<div className="column t-goods">商品</div>
						<div className="column t-price">单价(元)</div>
						<div className="column t-quantity">数量</div>
					</div>
					{this.state.carts.map(function(result) {
						return <Cart
							onSelect={this.onSelect.bind(this, result.id)} 
							onUnSelect={this.onUnSelect.bind(this, result.id)} 
						 	key={'cid_' + result.id } 
						 	data={result} /> 
					}, this)}
				</div>

				<div className="col-sm-5 cart-detail">
					<div className="">
						送餐详情
					</div>
					<div className="cart-user-info">

						<div className="cart-consignee">
							<label labelFor="consignee">
							 <span>收货人：</span>	
							</label>
							<input ref="consignee"/>
						</div>
						<div className="cart-phone-num">
							<label labelFor="phone_num">
							 <span>手机号：</span>	
							</label>
							<input ref="phone_num"/>
						</div>

						<br/>
						<div className="cart-address">
							<label labelFor="address">
							<span>地址：</span> 
							</label>
							<input  ref="address"/>
						</div>
					</div>
					<div className="col-sm-5 save-button">
						<button
	                    	onClick={this._save}>
	                    	提交订单 
	            		</button>
					</div>
				</div>	
			</div>
		);
	}
});

module.exports = CartList;