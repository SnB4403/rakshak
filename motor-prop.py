import sys
import glob
import matplotlib.pyplot as plt

# Check if the user provided the glob pattern as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python your_script.py 'PERFILES_WEB-202308/*.dat'")
    sys.exit(1)

# Get the glob pattern from the command-line argument
glob_pattern = sys.argv[1]

# Use glob to find all matching .dat files
dat_files = glob.glob(glob_pattern)
# Define the output file name
output_file = "output.txt"
# Create a list to store the data
data_list = []
I = 6.5
target_vel = 2.237*14 # [m/s] to [mph]
target_thrust = 9.81*1 # [kg] to [N]

for file_path in dat_files:
    rpm_dict = {}
    output_arr = []
    # Open and read the .dat file line by line
    with open(file_path, 'r') as file:
        line_count = 0
        cnt_rpm = ''
        rpm_array = []
        for line in file:
            line_count += 1
            target_line = 25
            # Process each line here
            if(line_count>19):
                data = line.strip().split()
                if(len(data)==4):
                    try:
                        rpm = float(cnt_rpm)
                    except:
                        pass
                    cnt_rpm = data[-1]
                    target_line = line_count+4
                    rpm_best = ''
                    #print(cnt_rpm)
                if (line_count>=target_line) and (len(data)>0):
                    try:
                        float(data[9])
                    except:
                        continue

                    cnt_best_data = rpm_best.strip().split()
                    torque = float(data[9])
                    thrust = float(data[10])
                    if(target_vel+2>float(data[0])>target_vel-2):
                        if (len(rpm_best)<2):
                            rpm_best=line
                            rpm_dict[float(cnt_rpm)] = rpm_best
                            # print(f'In file {file_path} at RPM {cnt_rpm} we have the following:')
                            # print(line)
                        elif(abs(float(cnt_best_data[10])-target_thrust)>abs(thrust-target_thrust)): 
                            rpm_best=line
                            rpm_dict[float(cnt_rpm)] = rpm_best
                            # print(f'In file {file_path} at RPM {cnt_rpm} we have the following:')
                            # print(line)
                        #else:
                            #print(float(data[0]))
                    # except:
                    #     pass


                #if (line_count<25): print(data)  # This example just prints each line, but you can do any processing you need
    #print(rpm_dict)
    # print(f'RPM Velocity Torque Thrust')
    # for key in rpm_dict:
    #     line = rpm_dict[key].strip().split()
    #     print(f'{key} {line[0]} {line[9]} {line[10]}')

    thrusts = []
    torques = []
    rpm = []
    vel = []
    for key in rpm_dict:
        line = rpm_dict[key].strip().split()
        thrusts.append(float(line[10]))
        torques.append(float(line[9]))
        vel.append(float(line[0]))
        rpm.append(key)
    # Find the index of the target value
    target_value = target_thrust
    # print()
    try:
        index = thrusts.index(target_value)
        print(f"The index of {target_value} is: {index}")
    except ValueError:
        pass
        #print(f"{target_value} is not in the list.")
    # Find the index of the lower bound
    lower_bound_index = None
    for i in range(len(thrusts)):
        if (thrusts[i] < target_value):
            lower_bound_index = i

    # Find the index of the upper bound
    upper_bound_index = lower_bound_index
    for i in range(len(thrusts)):
        if thrusts[i] > target_value:
            upper_bound_index = i
            break
    if(lower_bound_index==None): lower_bound_index = upper_bound_index
    if(lower_bound_index==None): continue
    rpm_u = rpm[upper_bound_index]
    rpm_l = rpm[lower_bound_index]
    vel_u = vel[upper_bound_index]
    vel_l = vel[lower_bound_index]
    Tor_u = torques[upper_bound_index]
    Tor_l = torques[lower_bound_index]
    Thrust_u = thrusts[upper_bound_index]
    Thrust_l = thrusts[lower_bound_index]

    # print((Thrust_l,Thrust_u))

    # Print the upper bound line
    upper_bound_line = f"Upper bound at rpm {rpm_u} with torque {Tor_u} and thrust {Thrust_u}"
    # print(upper_bound_line)

    # Print the lower bound line
    lower_bound_line = f"Lower bound at rpm {rpm_l} with torque {Tor_l} and thrust {Thrust_l}"
    # print(lower_bound_line)
    # print()

    try:
        ratio = (target_value - Thrust_l)/(Thrust_u-Thrust_l)
        vel = (vel_u-vel_l)*ratio+vel_l
        Tor = (Tor_u-Tor_l)*ratio+Tor_l
        rpm = (rpm_u-rpm_l)*ratio+rpm_l
    except:
        vel = vel_l
        Tor = Tor_l
        rpm = rpm_l

    # Calculate the Power
    # power = 1.1*Tor*rpm/9.55+I*I*0.024+22
    power = Tor*(rpm/9.55)
        # Append the data to the list
    data_list.append((file_path[20:], vel, Tor,rpm,power))

# Sort the data list based on the Power column
data_list.sort(key=lambda x: x[4])

# Open the output file for writing
with open(output_file, 'w') as output:
    # Write the header with proper alignment
    output.write("{:<25}{:<20}{:<20}{:<20}{:<20}\n".format("Filename", "Velocity", "Torque", "RPM", "Power"))
    
    # Iterate over the sorted data and write to the output file
    for data in data_list:
        output.write("{:<25}{:<20}{:<20}{:<20}{:<20}\n".format(data[0], "{:.2f}".format(data[1]), "{:.2f}".format(data[2]), "{:.2f}".format(data[3]), "{:.2f}".format(data[4])))



# Extract torque and RPM data from data_list
torque_data = [data[2] for data in data_list]
rpm_data = [data[3] for data in data_list]
# Create a scatter plot of torque vs. RPM
plt.figure(figsize=(8, 6))
plt.scatter(rpm_data, torque_data, c='blue', marker='o', alpha=0.5)
plt.title('Torque vs. RPM')
plt.xlabel('RPM')
plt.ylabel('Torque')
plt.plot([0, 4404], [0, 0.48], c='red')
plt.grid(True)
plt.show()