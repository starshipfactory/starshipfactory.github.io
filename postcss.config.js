module.exports = {
  plugins: [
    require("autoprefixer")({
      overrideBrowserslist: ["> 0.5% in CH", "last 2 versions"],
    }),
  ],
};
