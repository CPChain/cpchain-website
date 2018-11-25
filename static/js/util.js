function formatTS(mss) {
	var days = parseInt((mss / (1 * 60 * 60 * 24)))
	var hours = parseInt((mss % (1 * 60 * 60 * 24)) / (1 * 60 * 60));
	var minutes = parseInt((mss % (1 * 60 * 60)) / (1 * 60));
	var seconds = parseInt((mss % (1 * 60)) / 1);
	var res = ''
	if (days > 0) {
		res = `${days} days`
	} else if (hours > 0) {
		res = `${hours} hr${hours>1? 's': ''} ${minutes} min${minutes>1? 's': ''}`
	} else if (minutes > 0) {
		res = ` ${minutes} min${minutes>1? 's': ''} ${seconds} sec${seconds>1? 's': ''}`
	} else {
		res = `${seconds} second${seconds>1? 's': ''}`
	}
	return res
}

function convertDate(mss) {
	const longmss = mss*1000
	const date = new Date(longmss)
	const month = date.getMonth() + 1
	const day = date.getDate()
	const year = date.getFullYear()
	const hr = date.getHours()
	const mn = date.getMinutes()

	return `${month}/${day}/${year} ${hr}:${mn}`
}