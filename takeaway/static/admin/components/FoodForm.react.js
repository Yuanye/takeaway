var React = require('react');

var CategoryStore = require('../stores/CategoryStore');
var ImageActions = require('../actions/ImageActions');
var ImageStore = require('../stores/ImageStore');
var TakeawayConstants = require('../constants/TakeawayConstants')
var FoodForm = React.createClass({

	propTypes: {
			value: React.PropTypes.string,
			placeholder: React.PropTypes.string
		},

		getInitialState: function() {
			return {
				cover: null,
				categories: CategoryStore.getAll(),
			};
		},

		render: function() {
			return (
				<form>

				<div>
					<label labelFor="category_id">分类</label>
					<select name="category_id" ref="category_id">
						{this.state.categories.map(function(result) {
							return <option key={"cid"+ result.id} value={result.id}>{result.name}</option>
						})}
					</select>
					<br/>
					<label labelFor="name">食品名称</label>
					<input ref="name"/> 
					<br/>
					<label labelFor="price">价格</label>
					<input ref="price"/>份/元
					<br/>
					<label labelFor="cover">封面</label>
					<input 
						onChange={this.onChange}
						className="labelForm-control" 
						ref="cover" 
						type="file" 
						accept="image/*" 
						name="cover" />
					<img src={this.state.cover} alt="" />
					<a onClick={this.uploadImage} className="btn btn-default">上传</a>
 
					<button className="btn btn-default"
		                    onClick={this._save}>
		                   添加食品
		            </button>

	            </div>
	            </form>
			);
		},
		uploadImage: function(){
			var cover = this.refs.cover.getDOMNode().files[0];
			var uptoken = ImageStore.getUploadToken();
			ImageActions.create({
				token: uptoken.uptoken, 
				key: uptoken.key, 
				file: cover
			});
			this.setState({cover: TakeawayConstants.QINIU_IMAGE_URI + uptoken.key})
		},

		onChange: function() {
			var cover = this.refs.cover.getDOMNode().files[0];
			this.setState({cover: window.URL.createObjectURL(cover)});
		},

		_save: function() {
			var name = this.refs.name.getDOMNode().value;
			var price = this.refs.price.getDOMNode().value;
			var	category_id = this.refs.category_id.getDOMNode().value;
			var cover = this.state.cover;
			var cover = "http://tardisimg.qiniudn.com/2015-03-26-ef24f40b26c7d037f8f41af366d15b51";

			this.props.onSave({
				"name": name,
				"price": price,
				"category_id": category_id,
				"cover": cover,
			}); 
			this.setState({
	      		cover: ''
	    	});
	  	},

});

module.exports = FoodForm;