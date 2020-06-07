## Deprecated! This repository is now deprecated, please use the upstream project Pixi.JS v3+. It has now been migrated to a modular architecture.

[![Build Status](https://secure.travis-ci.org/drkibitz/node-pixi.svg?branch=master)](http://travis-ci.org/drkibitz/node-pixi?branch=master)
[![Coverage Status](https://coveralls.io/repos/drkibitz/node-pixi/badge.svg?branch=master)](https://coveralls.io/r/drkibitz/node-pixi?branch=master)
[![NPM version](https://badge.fury.io/js/pixi.svg)](http://badge.fury.io/js/pixi)
[![devDependency Status](https://david-dm.org/drkibitz/node-pixi/dev-status.svg)](https://david-dm.org/drkibitz/node-pixi#info=devDependencies)

# Node Pixi Renderer

This is a fork of [Pixi.JS](https://github.com/GoodBoyDigital/pixi.js) mainly for use with [browserify](http://browserify.org/), but has also went in a slightly different direction in terms of programming style.

**node-pixi matches the public Pixi.JS API, but now modular with browserify.** In a later major version, the public API and architecture may change to no longer match Pixi.JS. If/when such a split occurs the project's major version and branching will be updated occordingly, and the latest major version with full compatibility with Pixi.JS will containue to be maintained.

*Basically I am open to MAJOR refactors if appropriate. In the future, the goals may differ from Pixi.JS, and I may streamline things to only on WebGL, and maybe sooner rather than later (Saying goodbye to context 2d). This is all a maybe, as the web is moving fast, and Pixi.JS may actually make this move before this project.*

### Pixi.JS JavaScript 2D Renderer

The aim of this project is to provide a fast lightweight 2D library that works across all devices. The Pixi renderer allows everyone to enjoy the power of hardware acceleration without prior knowledge of [WebGL](http://en.wikipedia.org/wiki/WebGL). Also its fast.

- [Pixi.JS README](https://github.com/GoodBoyDigital/pixi.js/blob/master/README.md)
- [Pixi.JS Documentation](http://www.goodboydigital.com/pixijs/docs/)
- [Pixi.JS forum](http://www.html5gamedevs.com/forum/15-pixijs/)
- [Pixi.JS Tutorials and other helpful bits](https://github.com/GoodBoyDigital/pixi.js/wiki/Resources)

This content is released under the (http://opensource.org/licenses/MIT) MIT License.

## Examples

- [Basics](http://drkibitz.github.io/node-pixi/example/1-basics/)
- [SpriteSheet](http://drkibitz.github.io/node-pixi/example/2-sprite-sheet/)
- [MovieClip](http://drkibitz.github.io/node-pixi/example/3-movie-clip/)
- [Balls](http://drkibitz.github.io/node-pixi/example/4-balls/)
- [Morph](http://drkibitz.github.io/node-pixi/example/5-morph/)
- [Interactivity](http://drkibitz.github.io/node-pixi/example/6-interactivity/)
- [Transparent Background](http://drkibitz.github.io/node-pixi/example/7-transparent-background/)
- [Dragging](http://drkibitz.github.io/node-pixi/example/8-dragging/)
- [Tiling Texture](http://drkibitz.github.io/node-pixi/example/9-tiling-texture/)
- [Text](http://drkibitz.github.io/node-pixi/example/10-text/)
- [RenderTexture](http://drkibitz.github.io/node-pixi/example/11-render-texture/)
- [Spine](http://drkibitz.github.io/node-pixi/example/12-spine/)
- [Graphics](http://drkibitz.github.io/node-pixi/example/13-graphics/)
- [Masking](http://drkibitz.github.io/node-pixi/example/14-masking/)
- [Filters](http://drkibitz.github.io/node-pixi/example/15-filters/)

## Install

node-pixi can be installed with [Node](http://nodejs.org/) and [NPM](https://npmjs.org/).

```shell
npm install pixi
```

## Usage

### Basic

Once installed as a `node_module`, it can now be used in node and with browserify.

Example main.js:
```javascript
// Require pixi module
var pixi = require('pixi');

// You can use either WebGLRenderer or CanvasRenderer
var renderer = pixi.WebGLRenderer(800, 600);
document.body.appendChild(renderer.view);

var stage = new pixi.Stage();
var bunnyTexture = pixi.Texture.fromImage("bunny.png");
var bunny = new pixi.Sprite(bunnyTexture);

bunny.position.x = 400;
bunny.position.y = 300;
bunny.scale.x = 2;
bunny.scale.y = 2;

stage.addChild(bunny);

requestAnimationFrame(animate);

function animate() {
	bunny.rotation += 0.01;

	renderer.render(stage);

	requestAnimationFrame(animate);
}
```

### Alternative

You can completely bypass requiring the main `pixi` module, and go directly for the submodules. Doing this makes sure you only require what you need when you need it.

Example main.js:
```javascript
// Require modules
var Sprite = require('pixi/display/Sprite');
var Stage = require('pixi/display/Stage');
var Texture = require('pixi/textures/Texture');
var WebGLRenderer = require('pixi/renderers/webgl/WebGLRenderer');

var renderer = WebGLRenderer(800, 600);
document.body.appendChild(renderer.view);

var stage = new Stage();
// ... etc ...
```

## Build

node-pixi can be compiled with [Grunt](http://gruntjs.com/). If you don't already have this, go install [Node](http://nodejs.org/) and [NPM](https://npmjs.org/) then install the [Grunt Command Line](http://gruntjs.com/getting-started).
```shell
npm install -g grunt-cli
```

Get the source:
```shell
git clone https://github.com/drkibitz/node-pixi.git
```

Within your clone repository, install the `devDependencies` using NPM:
```shell
cd path/to/clone/
npm install
```

You should now be able to build node-pixi with Grunt:
```
grunt
```

Look in the `Gruntfile.js` for task configuration.

### Important Notes

**It's important to clone the source, and not assume that the source is the same is what is published to NPM.** The package on NPM is and should be considered a distributed release only, and is not compatible with the build process outlined here. To avoid any confusion about this, the published package.json has NO `devDependencies`, while the `devDependencies` of the source `package.json` remain.

The source may still be installed via NPM directly from Github. There are a few ways to define a URL to do this, just read [npm-faq](https://npmjs.org/doc/faq.html). If meant as a package dependency, I prefer using Github tarballs rather than the Git protocol to avoiding transferring the history. This is a *significantly faster* installation:
```shell
npm install https://github.com/drkibitz/node-pixi/archive/master.tar.gz
```

The default task is only slightly different from the task meant for continious integration. Both tasks build and test the bundles for debug and release, and copy the bundles to the dist directory, which are meant to be committed only by a repository maintainer. The difference is the default task creates project analysis reports using [plato](https://github.com/es-analysis/plato), and the ci task submits code coverage.

## Contribute

Want to contribute to node-pixi? Just make a pull request or a suggestion on [Github](https://github.com/drkibitz/node-pixi/issues). Please make sure you write tests, and run them before committing changes.

If you followed the steps in the **Build** section, then you can now run the tests locally:
```
grunt test
```

- The test suite uses the [karma-runner](http://karma-runner.github.io/0.10/index.html)
- The test suite expects Chrome to be installed (Configured in `Gruntfile.js`)
- Tests run for every [Travis CI](https://travis-ci.org/) build
- Code coverage is submitted to [coveralls](https://coveralls.io/) when running `grunt travis`

## Coming Soon

- **node-pixi goals**
- **node-pixi roadmap**
- **node-pixi documentation**
- **either update wiki, or remove it**
- **complete unit tests, and working functional tests**


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/drkibitz/node-pixi/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

