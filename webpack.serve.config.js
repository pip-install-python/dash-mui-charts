const config = require('./webpack.config.js');
const path = require('path');

const options = {
    mode: 'development',
    entry: './src/demo/index.js',
    output: {
        filename: './output.js',
        path: path.resolve(__dirname),
    },
};

module.exports = (env, argv) => {
    const baseConfig = config(env, argv);
    return {
        ...baseConfig,
        ...options,
        devServer: {
            static: {
                directory: path.join(__dirname),
            },
        },
    };
};
