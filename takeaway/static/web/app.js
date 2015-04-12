var React = require('react');

var FoodList = require('./components/FoodList.react');
var CartList = require('./components/CartList.react');
var OrderList = require('./components/OrderList.react');
var Router = require('react-router');

var DefaultRoute = Router.DefaultRoute;
var Link = Router.Link;
var Route = Router.Route;
var RouteHandler = Router.RouteHandler;


var Dashboard = React.createClass({
  render: function () {
    return (
      <div>首页</div>
    );
  }
});

var App = React.createClass({
  render: function () {
    return (
      <div>
        <header>
          <ul>
            <li><Link to="app">首页</Link></li>
            <li><Link to="orders" >我的订单</Link></li>
            <li><Link to="carts" >购物车</Link></li>
          </ul>
          Logged in as Jane
        </header>
        <RouteHandler {...this.props} />
      </div>
    );
  }
});

var routes = (
  <Route name="app" path="/"  handler={App}>
    <Route name="carts" path="carts" handler={CartList}/>
    <Route name="orders" path="orders" handler={OrderList}/>
    <Route name="categories" path="/categories/?:categoryId?" handler={FoodList}/>
    <DefaultRoute handler={FoodList }/>
  </Route>
);

Router.run(routes, function (Handler, state) {
  var params = state.params;
  React.render(<Handler params={params}/>, document.body);
});


