from generateotp import generateOTP
import smtplib


def SendOtp(Email):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("cbnits159@gmail.com", "anupam129")
    otp = generateOTP()
    message = "your otp is"+otp
    print(message)
    s.sendmail("cbnits159@gmail.com", Email, message)
    s.quit()
    return otp
