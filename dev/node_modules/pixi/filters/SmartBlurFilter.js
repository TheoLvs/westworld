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
"use strict";function SmartBlurFilter(){AbstractFilter.call(this),this.passes=[this],this.uniforms={blur:{type:"1f",value:1/512}},this.fragmentSrc=["precision mediump float;","varying vec2 vTextureCoord;","uniform sampler2D uSampler;","const vec2 delta = vec2(1.0/10.0, 0.0);","float random(vec3 scale, float seed) {","   return fract(sin(dot(gl_FragCoord.xyz + seed, scale)) * 43758.5453 + seed);","}","void main(void) {","   vec4 color = vec4(0.0);","   float total = 0.0;","   float offset = random(vec3(12.9898, 78.233, 151.7182), 0.0);","   for (float t = -30.0; t <= 30.0; t++) {","       float percent = (t + offset - 0.5) / 30.0;","       float weight = 1.0 - abs(percent);","       vec4 sample = texture2D(uSampler, vTextureCoord + delta * percent);","       sample.rgb *= sample.a;","       color += sample * weight;","       total += weight;","   }","   gl_FragColor = color / total;","   gl_FragColor.rgb /= gl_FragColor.a + 0.00001;","}"]}var AbstractFilter=require("./AbstractFilter"),proto=SmartBlurFilter.prototype=Object.create(AbstractFilter.prototype,{constructor:{value:SmartBlurFilter}});Object.defineProperty(proto,"blur",{get:function(){return this.uniforms.blur.value},set:function(a){this.uniforms.blur.value=a}}),module.exports=SmartBlurFilter;