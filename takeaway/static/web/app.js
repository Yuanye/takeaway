var React = require('react');

var FoodList = require('./components/FoodList.react');
var CartList = require('./components/CartList.react');
var OrderList = require('./components/OrderList.react');
var UserLogin = require('./components/UserLogin.react');
var UserSignUp = require('./components/UserSignUp.react');
var UserStore = require('./stores/UserStore');

var TakeawayConstants = require('./constants/TakeawayConstants');


require("bootstrap/less/bootstrap.less");
require("./styles/nav.css");
require("./styles/cart.css");
require("./styles/order.css");
require("./styles/account.css");

var Router = require('react-router');
var DefaultRoute = Router.DefaultRoute;
var Link = Router.Link;
var Route = Router.Route;
var RouteHandler = Router.RouteHandler;

function isEmptyObject(obj){
    for (var n in obj) {
        return false
    }
    return true; 
} 


var Dashboard = React.createClass({

  render: function () {
    return (
      <div>首页</div>
    );
  }
});

var App = React.createClass({
  getInitialState: function(){
    return {
      user: UserStore.account()
    };
  },
  render: function () {
    var LoginSignUpStyle = {}
    var AccountStyle = {display: "none"}
    if (!isEmptyObject(this.state.user)) {
      LoginSignUpStyle = {display: "none"}
      AccountStyle = {}
    };
    var LOGOUT_URI = "/logout?next="+TakeawayConstants.WEB_URI;
    return (
      <div className="container">
      <nav className="navbar navbar-default">
        <header className="container-fluid">
          <div className="navbar-header">
            <a className="navbar-brand" href="#">有个外卖</a>
          </div>
          <ul className="nav navbar-nav">
            <li>
              <Link to="app">首页</Link>
            </li>
            <li>
              <Link to="orders" >我的订单</Link>
            </li>

            <li><Link to="carts" > 购物车</Link></li>
          </ul>
          <ul className="nav navbar-nav navbar-right">
            <a className="navbar-brand" style={AccountStyle} href="">{this.state.user.name}</a>
            <a className="navbar-brand" style={AccountStyle} href={LOGOUT_URI}>退出</a>
            <Link to="user-login" className="navbar-brand" style={LoginSignUpStyle} >登录</Link>
            <Link to="user-signup" className="navbar-brand" style={LoginSignUpStyle} >注册</Link>
          </ul>
          
        </header>
      </nav>

      <RouteHandler {...this.props} />
      </div>
    );
  }
});

var routes = (
  <Route name="app" path="/"  handler={App}>
    <Route name="carts" path="carts" handler={CartList}/>
    <Route name="orders" path="orders" handler={OrderList}/>
    <Route name="user-login" path="account/login" handler={UserLogin}/>
    <Route name="user-signup" path="account/signup" handler={UserSignUp}/>
    <Route name="categories" path="/categories/?:categoryId?" handler={FoodList}/>
    <DefaultRoute handler={FoodList }/>
  </Route>
);

Router.run(routes, function (Handler, state) {
  var params = state.params;
  React.render(<Handler params={params}/>, document.body);
});


