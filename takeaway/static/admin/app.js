var React = require('react');

var Router = require('react-router'); // or var Router = ReactRouter; in browsers

var DefaultRoute = Router.DefaultRoute;
var Link = Router.Link;
var Route = Router.Route;
var RouteHandler = Router.RouteHandler;

var CategoryAdmin = require("./components/CategoryAdmin.react");
var FoodAdmin = require("./components/FoodAdmin.react");
var OrderAdmin = require("./components/OrderAdmin.react");
var UserStore = require('./stores/UserStore');

var TakeawayConstants = require('./constants/TakeawayConstants');

require("bootstrap/less/bootstrap.less");
require("./styles/nav.css");
require("./styles/order.css");

var Dashboard = React.createClass({
  render: function () {
    return (
      <div>首页</div>
    );
  }
});

var App = React.createClass({
  getInitialState: function(){
    var user = UserStore.account();
    return {
      user: user,
    };
  },
  render: function () {
    var LoginSignUpStyle = {}
    var AccountStyle = {display: "none"}
    if (this.state.user) {
      LoginSignUpStyle = {display: "none"}
      AccountStyle = {}
    };
    var LOGOUT_URI = "/logout?next="+TakeawayConstants.WEB_URI;
    return (
      <div className="container">
        <div className="nav col-sm-2 sidebar"> 
          <ul>
            <li>
              <a style={AccountStyle} href="">{this.state.user.name}</a>
              <a style={AccountStyle} href={LOGOUT_URI}>退出</a>
            </li>
            <li><Link to="app">首页</Link></li>
            <li><Link to="orders" >订单管理</Link></li>
            <li><Link to="categories" >分类管理</Link></li>
            <li><Link to="foods" >食品管理</Link></li>
          </ul>
        </div>
        <RouteHandler/>
      </div>
    );
  }
});

var routes = (
  <Route name="app" path="/" handler={App}>
    <Route name="orders" handler={OrderAdmin}/>
    <Route name="categories" handler={CategoryAdmin}/>
    <Route name="foods" handler={FoodAdmin}/>
    <DefaultRoute handler={OrderAdmin}/>
  </Route>
);

Router.run(routes, function (Handler) {
  React.render(<Handler/>, document.body);
});


