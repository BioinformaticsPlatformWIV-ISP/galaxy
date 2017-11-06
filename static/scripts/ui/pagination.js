define("ui/pagination",["jquery"],function(t){"use strict";function e(t,e){return this.numPages=null,this.currPage=0,this.init(t,e)}function i(t){return n(['<li><a href="javascript:void(0);">',t,"</a></li>"].join(""))}var a=function(t){return t&&t.__esModule?t:{default:t}}(t),n=a.default;e.prototype.DATA_KEY="pagination",e.prototype.defaults={startingPage:0,perPage:20,totalDataSize:null,currDataSize:null},e.prototype.init=function(t,i){return i=i||{},this.$element=t,this.options=a.default.extend(!0,{},this.defaults,i),this.currPage=this.options.startingPage,null!==this.options.totalDataSize&&(this.numPages=Math.ceil(this.options.totalDataSize/this.options.perPage),this.currPage>=this.numPages&&(this.currPage=this.numPages-1)),this.$element.data(e.prototype.DATA_KEY,this),this._render(),this},e.prototype._render=function(){return 0===this.options.totalDataSize?this:1===this.numPages?this:(this.numPages>0?(this._renderPages(),this._scrollToActivePage()):this._renderPrevNext(),this)},e.prototype._renderPrevNext=function(){var t=this,e=i("Prev"),a=i("Next"),r=n("<ul/>").addClass("pagination pagination-prev-next");return 0===this.currPage?e.addClass("disabled"):e.click(function(){t.prevPage()}),this.numPages&&this.currPage===this.numPages-1||this.options.currDataSize&&this.options.currDataSize<this.options.perPage?a.addClass("disabled"):a.click(function(){t.nextPage()}),this.$element.html(r.append([e,a])),this.$element},e.prototype._renderPages=function(){for(var t=this,e=n("<div>").addClass("pagination-scroll-container"),a=n("<ul/>").addClass("pagination pagination-page-list"),r=0;r<this.numPages;r+=1){var s=i(r+1).attr("data-page",r).click(function(e){t.goToPage(n(this).data("page"))});r===this.currPage&&s.addClass("active"),a.append(s)}return this.$element.html(e.html(a))},e.prototype._scrollToActivePage=function(){var t=this.$element.find(".pagination-scroll-container");if(!t.length)return this;var e=this.$element.find("li.active"),i=t.width()/2;return t.scrollLeft(t.scrollLeft()+e.position().left-i),this},e.prototype.goToPage=function(t){return t<=0&&(t=0),this.numPages&&t>=this.numPages&&(t=this.numPages-1),t===this.currPage?this:(this.currPage=t,this.$element.trigger("pagination.page-change",this.currPage),this._render(),this)},e.prototype.prevPage=function(){return this.goToPage(this.currPage-1)},e.prototype.nextPage=function(){return this.goToPage(this.currPage+1)},e.prototype.page=function(){return this.currPage},e.create=function(t,i){return new e(t,i)},a.default.fn.extend({pagination:function(t){var i=a.default.makeArray(arguments).slice(1);if("object"===a.default.type(t))return this.map(function(){return e.create(n(this),t),this});var r=n(this[0]).data(e.prototype.DATA_KEY);if(r){if("string"!==a.default.type(t))return r;var s=r[t];if("function"===a.default.type(s))return s.apply(r,i)}}})});
//# sourceMappingURL=../../maps/ui/pagination.js.map
