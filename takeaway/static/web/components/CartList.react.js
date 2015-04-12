var React = require('react');

var CartStore = require('../stores/CartStore');
var Cart = require('./Cart.react');
var CartList = React.createClass({
	getInitialState: function(){
		var categoryId = this.props.params.categoryId;
		return {
			carts: CartStore.getAll(),
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


	render: function() {
		return (
			<div>
					{this.state.carts.map(function(result) {
						return <Cart key={'cid_' + result.id} data={result} /> 
						})
					} 
			</div>
		);
	},
	_onChange:function(){
		
	}

});

module.exports = CartList;