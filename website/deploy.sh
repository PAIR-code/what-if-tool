
rm -rf www && rm -rf ../docs && mkdir ../docs && eleventy --input=src --output=www --config=.eleventy.js && cp -r www/. ../docs
