var React = require('react');

require("bootstrap/less/bootstrap.less");

var Router = require('react-router'); // or var Router = ReactRouter; in browsers

var DefaultRoute = Router.DefaultRoute;
var Link = Router.Link;
var Route = Router.Route;
var RouteHandler = Router.RouteHandler;

var CategoryAdmin = require("./components/CategoryAdmin.react");
var FoodAdmin = require("./components/FoodAdmin.react");

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
            <li><Link to="categories" >分类管理</Link></li>
            <li><Link to="foods" >食品管理</Link></li>
          </ul>
          Logged in as Jane
        </header>

        <RouteHandler/>
      </div>
    );
  }
});

var routes = (
  <Route name="app" path="/" handler={App}>
    <Route name="categories" handler={CategoryAdmin}/>
    <Route name="foods" handler={FoodAdmin}/>
    <DefaultRoute handler={Dashboard}/>
  </Route>
);

Router.run(routes, function (Handler) {
  React.render(<Handler/>, document.body);
});


