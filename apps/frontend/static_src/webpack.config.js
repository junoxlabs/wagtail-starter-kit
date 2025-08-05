const Webpack = require("webpack");
const path = require("path");
const glob = require("glob");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const { WebpackAssetsManifest } = require("webpack-assets-manifest");

const getEntryObject = () => {
  const entries = {};
  // for javascript/typescript entry file
  glob.sync(path.join(__dirname, "./src/app/*.{js,ts}")).forEach((filePath) => {
    const name = path.basename(filePath);
    const extension = path.extname(filePath);
    const entryName = name.replace(extension, "");
    if (entryName in entries) {
      throw new Error(`Entry file conflict: ${entryName}`);
    }
    entries[entryName] = filePath;
  });
  return entries;
};

module.exports = {
  entry: getEntryObject(),
  output: {
    path: path.resolve(__dirname, "../build"),
    filename: "js/[chunkhash:8].js",
    chunkFilename: "js/[id].[chunkhash:8].chunk.js",
    publicPath: "/static/",
  },
  optimization: {
    splitChunks: {
      chunks: "all",
    },

    runtimeChunk: "single",
  },
  plugins: [
    new CleanWebpackPlugin(),
    new MiniCssExtractPlugin({
      filename: "css/[name].[contenthash:8].css",
      chunkFilename: "css/[id].[contenthash:8].css",
    }),
    new WebpackAssetsManifest({
      entrypoints: true,
      output: "manifest.json",
      writeToDisk: true,
      publicPath: true,
    }),
  ],
  module: {
    rules: [
      {
        test: /\.s?css$/,
        use: [MiniCssExtractPlugin.loader, "css-loader", "postcss-loader"],
      },
      {
        test: /\.m?js$/,
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: "swc-loader",
        },
      },
    ],
  },
};
