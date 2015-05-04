var React = require('react');

var Food = require('./Food.react');
var Category = require('./Category.react');
var FoodStore = require('../stores/FoodStore');
var CategoryStore = require('../stores/CategoryStore');

var FoodList = React.createClass({
	getInitialState: function(){
		var categoryId = this.props.params.categoryId;
		return {
			foods: FoodStore.getAllByCategoryId(categoryId),
			categories: CategoryStore.getAll()
		};
	},

	componentDidMount: function() {
		FoodStore.addChangeListener(this._onChange);
  	},
  	componentWillUnmount: function() {
        FoodStore.removeChangeListener(this._onChange);
    },
    componentWillReceiveProps: function(){
    },

	render: function() {
		return (

			<div className="wrap ">
				<div className="col-sm-1 sidebar">
				  <ul className="nav nav-sidebar">
				  	<li>
					 	<a href="#/categories/latest">最新</a>
					</li>
					<li>
					 	<a href="#/categories/hot">最热</a>
					</li>
					{this.state.categories.map(function(result) {
						return <Category key={'cid_' + result.id} data={result} /> 
						})
					} 
				  </ul>
					
				</div>
				<div className="col-sm-11 foods">
					<ul>
						{this.state.foods.map(function(result){
							return <li > <Food key={'fid_' + result.id} data={result} /></li>
						})}
					</ul>
				</div>
			</div>

		);
	},
	_onChange: function(){
		
	}

});

module.exports = FoodList;