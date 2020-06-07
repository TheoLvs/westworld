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
"use strict";function BaseTexture(a,b){if(EventTarget.call(this),this.width=100,this.height=100,this.scaleMode=b||BaseTexture.SCALE_MODE.DEFAULT,this.hasLoaded=!1,this.source=a,a){if("complete"in this.source)if(this.source.complete)this.hasLoaded=!0,this.width=this.source.width,this.height=this.source.height,globals.texturesToUpdate.push(this);else{var c=this;this.source.onload=function(){c.hasLoaded=!0,c.width=c.source.width,c.height=c.source.height,globals.texturesToUpdate.push(c),c.dispatchEvent({type:"loaded",content:c})}}else this.hasLoaded=!0,this.width=this.source.width,this.height=this.source.height,globals.texturesToUpdate.push(this);this.imageUrl=null,this._powerOf2=!1}}var platform=require("../platform"),globals=require("../core/globals"),EventTarget=require("../events/EventTarget"),baseTextureCache={},proto=BaseTexture.prototype;proto.destroy=function(){this.source.src&&(this.imageUrl in baseTextureCache&&delete baseTextureCache[this.imageUrl],this.imageUrl=null,this.source.src=null),this.source=null,globals.texturesToDestroy.push(this)},proto.updateSourceImage=function(a){this.hasLoaded=!1,this.source.src=null,this.source.src=a},BaseTexture.fromImage=function(a,b,c){var d=baseTextureCache[a];if(!d){var e=new platform.createImage;b&&(e.crossOrigin=""),e.src=a,d=new BaseTexture(e,c),d.imageUrl=a,baseTextureCache[a]=d}return d},BaseTexture.SCALE_MODE={DEFAULT:0,LINEAR:0,NEAREST:1},module.exports=BaseTexture;