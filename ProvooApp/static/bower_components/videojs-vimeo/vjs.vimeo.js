!function(){var a={UNSTARTED:-1,ENDED:0,PLAYING:1,PAUSED:2,BUFFERING:3};videojs.Vimeo=videojs.MediaTechController.extend({init:function(a,b,c){if(videojs.MediaTechController.call(this,a,b,c),"undefined"!=typeof b.source)for(var d in b.source)a.options()[d]=b.source[d];this.player_=a,this.player_el_=document.getElementById(this.player_.id()),this.player_.controls(!1),this.id_=this.player_.id()+"_vimeo_api",this.el_=videojs.Component.prototype.createEl("iframe",{id:this.id_,className:"vjs-tech",scrolling:"no",marginWidth:0,marginHeight:0,frameBorder:0}),this.el_.setAttribute("webkitAllowFullScreen",""),this.el_.setAttribute("mozallowfullscreen",""),this.el_.setAttribute("allowFullScreen",""),this.player_el_.insertBefore(this.el_,this.player_el_.firstChild);var e="file:"===document.location.protocol?"http:":document.location.protocol;this.baseUrl=e+"//player.vimeo.com/video/",this.vimeo={},this.vimeoInfo={};var f=this;this.el_.attachEvent?this.el_.attachEvent("onload",vjs.bind(f,f.onLoad)):this.el_.onload=function(){f.onLoad()},this.startMuted=a.options().muted,this.src(a.options().src)}}),videojs.Vimeo.prototype.dispose=function(){this.vimeo.removeEvent("ready"),this.vimeo.api("unload"),delete this.vimeo,this.el_.parentNode.removeChild(this.el_),videojs.MediaTechController.prototype.dispose.call(this)},videojs.Vimeo.prototype.src=function(a){this.isReady_=!1;var b=/^.*(vimeo\.com\/)((channels\/[A-z]+\/)|(groups\/[A-z]+\/videos\/))?([0-9]+)/,c=a.match(b);c&&(this.videoId=c[5]);var d={api:1,byline:0,portrait:0,show_title:0,show_byline:0,show_portait:0,fullscreen:1,player_id:this.id_,autoplay:this.player_.options().autoplay?1:0,loop:this.player_.options().loop?1:0,color:this.player_.options().color||""};"#"===d.color.substring(0,1)&&(d.color=d.color.substring(1)),this.el_.src=this.baseUrl+this.videoId+"?"+videojs.Vimeo.makeQueryString(d)},videojs.Vimeo.prototype.load=function(){},videojs.Vimeo.prototype.play=function(){this.vimeo.api("play")},videojs.Vimeo.prototype.pause=function(){this.vimeo.api("pause")},videojs.Vimeo.prototype.paused=function(){return this.vimeoInfo.state!==a.PLAYING&&this.vimeoInfo.state!==a.BUFFERING},videojs.Vimeo.prototype.currentTime=function(){return this.vimeoInfo.time||0},videojs.Vimeo.prototype.setCurrentTime=function(a){this.vimeo.api("seekTo",a),this.player_.trigger("timeupdate")},videojs.Vimeo.prototype.duration=function(){return this.vimeoInfo.duration||0},videojs.Vimeo.prototype.buffered=function(){return videojs.createTimeRange(0,this.vimeoInfo.buffered*this.vimeoInfo.duration||0)},videojs.Vimeo.prototype.volume=function(){return this.vimeoInfo.muted?this.vimeoInfo.muteVolume:this.vimeoInfo.volume},videojs.Vimeo.prototype.setVolume=function(a){this.vimeo.api("setvolume",a),this.vimeoInfo.volume=a,this.player_.trigger("volumechange")},videojs.Vimeo.prototype.currentSrc=function(){return this.el_.src},videojs.Vimeo.prototype.muted=function(){return this.vimeoInfo.muted||!1},videojs.Vimeo.prototype.setMuted=function(a){a?(this.vimeoInfo.muteVolume=this.vimeoInfo.volume,this.setVolume(0)):this.setVolume(this.vimeoInfo.muteVolume),this.vimeoInfo.muted=a,this.player_.trigger("volumechange")},videojs.Vimeo.prototype.onReady=function(){this.isReady_=!0,this.triggerReady(),this.player_.trigger("loadedmetadata"),this.startMuted&&(this.setMuted(!0),this.startMuted=!1)},videojs.Vimeo.prototype.onLoad=function(){this.vimeo&&this.vimeo.api&&(this.vimeo.api("unload"),delete this.vimeo),this.vimeo=$f(this.el_),this.vimeoInfo={state:a.UNSTARTED,volume:1,muted:!1,muteVolume:1,time:0,duration:0,buffered:0,url:this.baseUrl+this.videoId,error:null};var b=this;this.vimeo.addEvent("ready",function(a){b.onReady(),b.vimeo.addEvent("loadProgress",function(a,c){b.onLoadProgress(a)}),b.vimeo.addEvent("playProgress",function(a,c){b.onPlayProgress(a)}),b.vimeo.addEvent("play",function(a){b.onPlay()}),b.vimeo.addEvent("pause",function(a){b.onPause()}),b.vimeo.addEvent("finish",function(a){b.onFinish()}),b.vimeo.addEvent("seek",function(a,c){b.onSeek(a)})})},videojs.Vimeo.prototype.onLoadProgress=function(a){var b=!this.vimeoInfo.duration;this.vimeoInfo.duration=a.duration,this.vimeoInfo.buffered=a.percent,this.player_.trigger("progress"),b&&this.player_.trigger("durationchange")},videojs.Vimeo.prototype.onPlayProgress=function(a){this.vimeoInfo.time=a.seconds,this.player_.trigger("timeupdate")},videojs.Vimeo.prototype.onPlay=function(){this.vimeoInfo.state=a.PLAYING,this.player_.trigger("play")},videojs.Vimeo.prototype.onPause=function(){this.vimeoInfo.state=a.PAUSED,this.player_.trigger("pause")},videojs.Vimeo.prototype.onFinish=function(){this.vimeoInfo.state=a.ENDED,this.player_.trigger("ended")},videojs.Vimeo.prototype.onSeek=function(a){this.player_.trigger("seeking"),this.vimeoInfo.time=a.seconds,this.player_.trigger("timeupdate"),this.player_.trigger("seeked")},videojs.Vimeo.prototype.onError=function(a){this.player_.error=a,this.player_.trigger("error")},videojs.Vimeo.isSupported=function(){var a=videojs.Flash.version()[0]>=10;if(!a){var b=-1!=navigator.userAgent.indexOf("Opera");if(b)return!1;var c=-1!=navigator.userAgent.indexOf("Mac OS X"),d=navigator.userAgent.toLowerCase().indexOf("firefox")>-1;if(c&&d)return!1;var e=/Trident\/([\d\.]+)/;if(e.test(navigator.userAgent)){var f;if(null!=e.exec(navigator.userAgent)&&(f=parseFloat(RegExp.$1)),f&&7>f)return!1}}return!0},videojs.Vimeo.prototype.supportsFullScreen=function(){return!1},videojs.Vimeo.canPlaySource=function(a){return"video/vimeo"==a.type},videojs.Vimeo.makeQueryString=function(a){var b=[];for(var c in a)a.hasOwnProperty(c)&&b.push(encodeURIComponent(c)+"="+encodeURIComponent(a[c]));return b.join("&")};(function(){function a(b){return new a.fn.init(b)}function g(a,b,c){if(!c.contentWindow.postMessage)return!1;var d=JSON.stringify({method:a,value:b});c.contentWindow.postMessage(d,f)}function h(a){var b,c;try{b=JSON.parse(a.data),c=b.event||b.method}catch(e){}if("ready"!=c||d||(d=!0),!/^https?:\/\/player.vimeo.com/.test(a.origin))return!1;"*"===f&&(f=a.origin);var g=b.value,h=b.data,i=""===i?null:b.player_id,k=j(c,i),l=[];return k?(void 0!==g&&l.push(g),h&&l.push(h),i&&l.push(i),l.length>0?k.apply(null,l):k.call()):!1}function i(a,c,d){d?(b[d]||(b[d]={}),b[d][a]=c):b[a]=c}function j(a,c){return c&&b[c]?b[c][a]:b[a]}function k(a,c){if(c&&b[c]){if(!b[c][a])return!1;b[c][a]=null}else{if(!b[a])return!1;b[a]=null}return!0}function l(a){return!!(a&&a.constructor&&a.call&&a.apply)}var b={},d=!1,f=(Array.prototype.slice,"*");return a.fn=a.prototype={element:null,init:function(a){return"string"==typeof a&&(a=document.getElementById(a)),this.element=a,this},api:function(a,b){if(!this.element||!a)return!1;var c=this,d=c.element,e=""!==d.id?d.id:null,f=l(b)?null:b,h=l(b)?b:null;return h&&i(a,h,e),g(a,f,d),c},addEvent:function(a,b){if(!this.element)return!1;var c=this,e=c.element,f=""!==e.id?e.id:null;return i(a,b,f),"ready"!=a?g("addEventListener",a,e):"ready"==a&&d&&b.call(null,f),c},removeEvent:function(a){if(!this.element)return!1;var b=this,c=b.element,d=""!==c.id?c.id:null,e=k(a,d);"ready"!=a&&e&&g("removeEventListener",a,c)}},a.fn.init.prototype=a.fn,window.addEventListener?window.addEventListener("message",h,!1):window.attachEvent("onmessage",h),window.Froogaloop=window.$f=a})()}();
