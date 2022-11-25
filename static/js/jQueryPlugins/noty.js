(function ($) {
	$.fn.noty = function (options) {
		return {
			settings: $.extend({
				'maxMessage': 5,
				'timeToHide': 10000,
				'timerDelay': 500
			},
			options),
			noty: $(this),
			notysObjects: [],
			queue: [],
			curPos: 1,
			init: function () {
				let timerId = setTimeout(function tick() {
					this.getFromQueue();
					this.timerTick();
					timerId = setTimeout(tick.bind(this), this.settings.timerDelay);
				}.bind(this), this.settings.timerDelay);
			},
			getFromQueue: function () {
				if (this.queue.length > 0) {
					this.create(this.queue.shift());
				}
			},
			new: function (notysContent) {
				this.queue.push(notysContent);
			},
			timerTick: function () {
				let flag = -1;
				for (let i = 0; i < this.notysObjects.length; i++) {
					this.notysObjects[i].time += this.settings.timerDelay;
					if (this.notysObjects[i].time >= this.settings.timeToHide) {
						flag = i;
					}
				}

				if (flag !== -1) {
					let $elem = $('div[data-func=' + this.notysObjects[flag].pos + ']');

					this.notysObjects.splice(flag, 1);
					$elem.children('.noty-btn').css('display', 'none');
					$elem.hide('fast').delay(1).queue(function () {
						$(this).remove();
					})
				}
			},
			notysHTML: function (notysContent, notysId) {
				return `<div class="noty" data-func="${notysId}">
				<div class="noty-btn">
				<i class="fa fa-times" aria-hidden="true"></i>
				</div>
				<div class="noty-message">
				${notysContent}
				</div>
				</div>`
			},
			create: function (notysContent) {
				if (this.notysObjects.length >= this.settings.maxMessage) {
					this.notysObjects = [];
					this.noty.html('');
				}
				this.notysObjects.push({
					time: 0,
					msg: notysContent,
					pos: this.curPos
				});
				let newNotyHTML = this.notysHTML(notysContent, this.curPos);
				this.noty.html(this.noty.html() + newNotyHTML);

				let $elem = $('div[data-func=' + this.curPos + ']');
				$elem.show('fast');

				let that = this;
				$('div[data-func] .noty-btn').on('click', function () {
					let flag = -1;

					let num = $(this).parent().data('func');

					for (let i = 0; i < that.notysObjects.length; i++) {
						if (that.notysObjects[i].pos === num) {
							flag = i;
							break
						}
					}

					if (flag !== -1) {
						let $elem = $('div[data-func=' + that.notysObjects[flag].pos + ']');

						that.notysObjects.splice(flag, 1);
						$elem.children('.noty-btn').css('display', 'none');
						$elem.hide('fast').delay(1).queue(function () {
							$(this).remove();
						})
					}
				});
				this.curPos += 1;
			}


		}
	}
})(jQuery)