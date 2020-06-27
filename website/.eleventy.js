const markdownIt = require("markdown-it");
const markdownItRenderer = new markdownIt();

module.exports = function(eleventyConfig) {
  eleventyConfig.templateFormats = ["liquid", "md", "png"];
  
  eleventyConfig.addFilter('markdownify', (str) => {
    return markdownItRenderer.renderInline(str);
  })

  eleventyConfig.addPassthroughCopy("src/assets/");
  eleventyConfig.addPassthroughCopy("src/demos/");
};