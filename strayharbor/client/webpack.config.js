var path = require('path');
var webpack = require('webpack');

module.exports = {
    entry: ['./src/index.js'],
    output: {
        path: path.join(__dirname, 'static/app/js'),
        filename: 'index.bundle.min.js',
    },
    plugins: [
        new webpack.optimize.UglifyJsPlugin({
            compressor: {
                warnings: false,
            },
        }),
        new webpack.optimize.OccurenceOrderPlugin(),
    ],
    module: {
        loaders: [
            {
                test: /\.js$/,
                loader: 'babel',
                exclude: /node_modules/,
            },
            {
                test: /\.vue$/,
                loader: 'vue',
            },
        ],
    },
    vue: {
        loaders: {
            js: 'babel',
        },
    },
};
