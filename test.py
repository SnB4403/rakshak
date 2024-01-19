target_value = 19.6
Thrust_l = 14.786
Thrust_u = 25.63
rpm_l = 5000
rpm_u = 6000
Tor_u = 0.677
Tor_l = 1.047
ratio = (target_value - Thrust_l)/(Thrust_u-Thrust_l)
Tor = (Tor_u-Tor_l)*ratio+Tor_l
rpm = (rpm_u-rpm_l)*ratio+rpm_l
I = 6.5

power = 1.1*Tor*rpm/9.55+I*I*0.024+22
print(power, Tor, rpm)