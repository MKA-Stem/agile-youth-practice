var webpack = require("webpack");
var path = require("path");
var ExtractTextPlugin = require("extract-text-webpack-plugin");

var DEV = process.env.NODE_ENV != "production";
process.env.NODE_ENV = DEV ? "development" : "production";

module.exports = {
    devtool: "source-map",

    devServer: {
        hot: true,
		port:8080,
		stats:{ chunks: false },
		proxy:{
			"/api":{target: "http://localhost:8081"}
		},
		historyApiFallback: {index: "app/index.html"},
		
    },

	entry: {app: path.resolve("./app/index.jsx")},

    output:{
        path: path.resolve('./dist'),
        filename:'[name].js',
        libraryTarget: "umd"
    },

    plugins: [
        new webpack.EnvironmentPlugin(["NODE_ENV"]),
		new webpack.ProvidePlugin({"fetch": "imports-loader?this=>global!exports-loader?global.fetch!whatwg-fetch"}), // fetch polyfill

		...(DEV?[
			new webpack.HotModuleReplacementPlugin(),
			new webpack.NamedModulesPlugin()
		]:[
			new ExtractTextPlugin("style.css"),
			new webpack.LoaderOptionsPlugin({
				minimize: true,
				debug: false
			}),
		  	new webpack.optimize.UglifyJsPlugin({
				compress: {
					warnings: false,
					screw_ie8: true,
				  	conditionals: true,
				  	unused: true,
				  	comparisons: true,
				  	sequences: true,
				  	dead_code: true,
				  	evaluate: true,
				  	if_return: true,
				  	join_vars: true,
				},
				output: {
				  comments: false,
				},
				sourceMap: true
		  	})
		])
    ],

    resolve: {
		modules: [path.resolve("./app"), "node_modules"]
	},

	module: {
		rules:[
			{
				test:/\.s?css$/,
				use:DEV?
					[
						{loader:"style-loader", options:{sourceMap:true}},
						{loader:"css-loader", options:{sourceMap:true, importLoaders:1}},
						{loader:"sass-loader", options:{sourceMap:true}}
					] :
					ExtractTextPlugin.extract({ use:["css-loader", {loader:"sass-loader", options:{sourceMap:true}}]})
			},
			{
				test:/\.jsx?$/,
				exclude:/node_modules/,
				use:[
					"react-hot-loader",
					{loader:"babel-loader", options:{presets:[["es2015", /*{modules:false}*/], "react"]}}
				],
			},
			{
				test:/\.svg$/,
				use: "file-loader"
			}
		]
    },
}
