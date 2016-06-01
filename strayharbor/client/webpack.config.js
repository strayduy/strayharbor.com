var path = require('path');
var webpack = require('webpack');

var NODE_ENV = process.env.NODE_ENV;

var config = {
    entry: ['./src/index.js'],
    output: {
        path: path.join(__dirname, 'static/app/js'),
        filename: 'index.bundle.js',
    },
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
        ],
    },
};

if (NODE_ENV && NODE_ENV.toLowerCase() === 'production') {
    config.output.filename = 'index.bundle.min.js';
    config.plugins = [
        new webpack.optimize.UglifyJsPlugin({
            compressor: {
                warnings: false,
            },
        }),
        new webpack.optimize.OccurenceOrderPlugin(),
    ];
}
else {
    config.output.publicPath = 'http://localhost:8080/static/app/js/';
}

module.exports = config;
