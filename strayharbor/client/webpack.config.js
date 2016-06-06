var path = require('path');
var webpack = require('webpack');

var NODE_ENV = process.env.NODE_ENV;

var config = {
    entry: ['./src/index.js'],
    output: {
        path: path.join(__dirname, 'static/app/js'),
        publicPath: '/static/app/js/',
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
                include: [
                    path.resolve(__dirname, 'src'),
                ],
                query: {
                    cacheDirectory: true,
                },
            },
            {
                test: /\.vue$/,
                loader: 'vue',
            },
            {
                test: /\.css$/,
                loader: 'style-loader!css-loader'
            },
            {
                test: /\.(ttf|eot|svg|woff(2)?)(\?[a-z0-9=&.]+)?$/,
                loader: 'file?name=./[name].[ext]',
            },
        ],
    },
};

if (!NODE_ENV || NODE_ENV.toLowerCase() !== 'production') {
    config.output.publicPath = 'http://localhost:8080/static/app/js/';
    config.output.filename = 'index.bundle.js';
    config.plugins = [];
}

module.exports = config;
