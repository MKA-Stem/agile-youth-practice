var webpack = require("webpack");

var resolve = require("path").resolve;

module.exports = {
	entry: resolve("./app/index.jsx"),

	output:{
		filename: "bundle.js",
		path: resolve("./dist"),
		publicPath: "/",
	},

	devtool: "source-map",

}
