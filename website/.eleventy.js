module.exports = function(eleventyConfig) {
  eleventyConfig.templateFormats = ["html", "liquid", "md", "png"];
  
  eleventyConfig.addPassthroughCopy("src/assets/");
};