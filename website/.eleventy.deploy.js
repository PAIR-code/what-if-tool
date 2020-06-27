const markdownIt = require("markdown-it");
const markdownItRenderer = new markdownIt();
const rootPrefix = "/what-if-tool";

module.exports = function(eleventyConfig) {
  eleventyConfig.templateFormats = ["liquid", "md", "png"];

  eleventyConfig.addFilter('markdownify', (str) => {
    return markdownItRenderer.renderInline(str);
  })

  eleventyConfig.addShortcode("root", () => {
    return rootPrefix;
  });

  eleventyConfig.addPassthroughCopy("src/assets/");
  eleventyConfig.addPassthroughCopy("src/demos/");
};
