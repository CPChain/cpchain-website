function formatTS(mss) {
	var hours = parseInt((mss % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
	var minutes = parseInt((mss % (1000 * 60 * 60)) / (1000 * 60));
	var seconds = parseInt((mss % (1000 * 60)) / 1000);
	var res = ''
	if (hours > 0) {
		res = `${hours} hr${hours>1? 's': ''} ${minutes} min${minutes>1? 's': ''} ${seconds} sec${seconds>1? 's': ''}`
	} else if (minutes > 0) {
		res = ` ${minutes} min${minutes>1? 's': ''} ${seconds} sec${seconds>1? 's': ''}`
	} else {
		res = `${seconds} second${seconds>1? 's': ''}`
	}
	return res
}