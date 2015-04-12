module.exports = {
	entry: "./app.js",
	output: {
    	path: __dirname,
    	filename: "bundle.js"
    },
    module: {
  		loaders: [
    		{ test: /\.jsx?$/, loaders: ['jsx-loader', 'jsx?harmony'] },
        { test: /\.css$/, loader: "style!css" },
        { test: /\.less$/, loader: 'style-loader!css-loader!less-loader' },
        { test: /\.woff(\?v=\d+\.\d+\.\d+)?$/, loader: "url?limit=10000&minetype=application/font-woff" },
        { test: /\.woff2(\?v=\d+\.\d+\.\d+)?$/, loader: "url?limit=10000&minetype=application/font-woff" },
        { test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/, loader: "url?limit=10000&minetype=application/octet-stream" },
        { test: /\.eot(\?v=\d+\.\d+\.\d+)?$/, loader: "file" },
        { test: /\.svg(\?v=\d+\.\d+\.\d+)?$/, loader: "url?limit=10000&minetype=image/svg+xml" }
  		]		
	}
};