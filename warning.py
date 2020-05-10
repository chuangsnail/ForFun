#!/usr/bin/env python
# -*- encoding: utf8-*-
import weather
import os
import smtplib


def check1( to_addr="jeff0118252718@gmail.com", people = "Snail", district="新北市", an_time = 1 ):
	
	to_addr="jeff0118252718@gmail.com"
	people = "Snail"
	district = "新北市"
	an_time = 1

	str_an_time = ""
	if an_time == 0:
		str_an_time = "半夜"
	elif an_time == 1:
		str_an_time = "白天"
	elif an_time == 2:
		str_an_time = "晚上"

	arg = ["./weather.py", "-d", district, "-t", str(an_time) ]
	rr = weather.weather(arg)
	if rr >= 50:
		smtp=smtplib.SMTP('smtp.gmail.com', 587)
		#smtp.ehlo()
		smtp.starttls()
		smtp.login('weathersnail@gmail.com','hiimsnail')
		from_addr='weathersnail@gmail.com'
		
		msg="Subject:降雨提醒 WeaterSnail天氣蝸牛 關心您\n{} 你好，\n你所在的區域 {} {}降雨機率為 {}% (>=50%)，出門建議攜帶雨具，在此通知您。\
		\n\n如有疑問請聯絡此信箱，謝謝！\n祝 身體健康\n\n天氣蝸牛WeatherSnail"\
		.format( people, district, str_an_time, rr )
		status=smtp.sendmail(from_addr, to_addr, msg)
		if status=={}:
		    print("Successfully send!")
		else:
		    print("Fail in sending to {}!".format(to_addr))
		smtp.quit()
	else:
		print "<50% rain rate!!"


if __name__ == '__main__':
	check1()