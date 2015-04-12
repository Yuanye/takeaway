var React = require('react');

var Food = React.createClass({
	propTypes: {
    	data: React.PropTypes.object,
    	id: React.PropTypes.number,
    	name: React.PropTypes.string,
    	category: React.PropTypes.object,
    	price: React.PropTypes.number,
    	cover: React.PropTypes.string,
    	records: React.PropTypes.number,
    	created_at: React.PropTypes.string,
    	updated_at: React.PropTypes.string
	},

	render: function() {
		var food = this.props.data;
		return (
			<div className="food">
				{food.id}/
				{food.name}	/	
				{food.price}/元		
				{food.updated_at}/	
				<img src={food.cover} alt="" />		
			</div>
		);
	}

});

module.exports = Food;