var React = require('react');

var Food = require('./Food.react');
var FoodStore = require('../stores/FoodStore');

var FoodList = React.createClass({
	getInitialState: function(){
		return {
			foods: FoodStore.getAll()
		};
	},

	componentDidMount: function() {
		FoodStore.addChangeListener(this._onChange);
  	},
  	componentWillUnmount: function() {
        FoodStore.removeChangeListener(this._onChange);
    },

	render: function() {
		return (
			<div className="col-sm-11 foods">
				<ul>
					{this.state.foods.map(function(result){
						return <li > <Food key={'fid_' + result.id} data={result} /></li>
					})}
				</ul>
			</div>
		);
	},
	_onChange: function() {
		this.setState({
			foods: Food.getAll()
		});	
	}

});

module.exports = FoodList;