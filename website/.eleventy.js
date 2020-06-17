module.exports = function(eleventyConfig) {
  eleventyConfig.templateFormats = ["liquid", "md", "png"];
  
  eleventyConfig.addPassthroughCopy("src/assets/");
  eleventyConfig.addPassthroughCopy("src/demos/");
};