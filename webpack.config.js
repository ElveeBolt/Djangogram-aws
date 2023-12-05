const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");


module.exports = {
    mode: 'development',
    entry: {
        app: path.resolve(__dirname, './djangogram/static/js/index.js')
    },
    output: {
        path: path.resolve(__dirname, "./djangogram/static/dist"),
        publicPath: "/static/dist/",
        filename: "js/[name].js",
    },
    module: {
        rules: [
            {
                test: /\.css$/,
                use: [MiniCssExtractPlugin.loader, "css-loader", ],
            },
            {
                test: /\.(woff|woff2|eot|ttf)$/,
                type: 'asset/resource',
                generator: {
                  filename: 'fonts/[hash][ext][query]'
                }
            },
            {
                test: /\.(?:ico|gif|png|jpg|jpeg|svg)$/i,
                type: 'asset/resource',
                generator: {
                  filename: 'images/[hash][ext][query]'
                }
            },
            {
                test: require.resolve("jquery"),
                loader: "expose-loader",
                options: {
                    exposes: ["$", "jQuery"],
                },
            }]
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: "css/[name].css",
        })
    ],
};