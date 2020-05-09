#!/usr/bin/env python
# -*- encoding: utf8-*-
import weather
import os
import smtplib


def check():
	district = "新北市"
	arg = ["./weather.py", "-d", district, "-t", "1" ]
	rr = weather.weather(arg)
	if rr > 50:
		smtp=smtplib.SMTP('smtp.gmail.com', 587)
		#smtp.ehlo()
		smtp.starttls()
		smtp.login('weathersnail@gmail.com','hiimsnail')
		from_addr='weathersnail@gmail.com'
		to_addr="jeff0118252718@gmail.com"
		msg="Subject:降雨提醒 WeaterSnail天氣蝸牛 關心您\n你好，\n你所在的區域 {} 降雨機率為 {}% (>50%)，出門建議攜帶雨具，在此通知您。\
		\n\n如有疑問請聯絡此信箱，謝謝！\n祝 身體健康\n\n天氣蝸牛WeatherSnail"\
		.format( district, rr )
		status=smtp.sendmail(from_addr, to_addr, msg)
		if status=={}:
		    print("Successfully send!")
		else:
		    print("Fail in sending!")
		smtp.quit()
	else:
		print "<50% rain rate!!"


if __name__ == '__main__':
	check()