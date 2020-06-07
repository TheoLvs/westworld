/**
 * pixi 0.3.1 (a1e2d46)
 * http://drkibitz.github.io/node-pixi/
 * Copyright (c) 2013-2015 Dr. Kibitz, http://drkibitz.com
 * Super fast 2D rendering engine for browserify, that uses WebGL with a context 2d fallback.
 * built: Fri May 22 2015 20:31:02 GMT-0700 (PDT)
 *
 * Pixi.js - v1.3.0
 * Copyright (c) 2012, Mat Groves
 */
"use strict";var platform=require("../platform"),CanvasRenderer=require("../renderers/canvas/CanvasRenderer"),WebGLRenderer=require("../renderers/webgl/WebGLRenderer");module.exports=function(a,b,c,d,e){a||(a=800),b||(b=600);var f=function(){try{var a=platform.createCanvas();return!!platform.window.WebGLRenderingContext&&(a.getContext("webgl")||a.getContext("experimental-webgl"))}catch(b){return!1}}();if(f&&platform.navigator){var g=-1!==platform.navigator.userAgent.toLowerCase().indexOf("trident");f=!g}return f?new WebGLRenderer(a,b,c,d,e):new CanvasRenderer(a,b,c,d)};