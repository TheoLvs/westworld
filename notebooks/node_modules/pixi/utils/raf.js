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
"use strict";for(var platformGlobal=require("../platform").global,lastTime=0,vendors=["ms","moz","webkit","o"],i=0;i<vendors.length&&!platformGlobal.requestAnimationFrame;++i)platformGlobal.requestAnimationFrame=platformGlobal[vendors[i]+"RequestAnimationFrame"],platformGlobal.cancelAnimationFrame=platformGlobal[vendors[i]+"CancelAnimationFrame"]||platformGlobal[vendors[i]+"CancelRequestAnimationFrame"];platformGlobal.requestAnimationFrame||(platformGlobal.requestAnimationFrame=function(a){var b=(new Date).getTime(),c=Math.max(0,16-(b-lastTime)),d=platformGlobal.setTimeout(function(){a(b+c)},c);return lastTime=b+c,d}),platformGlobal.cancelAnimationFrame||(platformGlobal.cancelAnimationFrame=function(a){platformGlobal.clearTimeout(a)}),module.exports=platformGlobal.requestAnimationFrame;