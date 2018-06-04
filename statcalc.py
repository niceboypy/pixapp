import os
import time


directory = '/home/normalman/project_folder/pythonprjs/pixabayapp'

x = os.listdir(directory)

List =[]
for i in x:
	if i.endswith('.py') or i.endswith('.kv'):
		List += [i]


filelist = [os.path.join(directory, x) for x in List]
print("FILES READ: ")
for x in filelist:
	print("--- {} ".format(x.split('/')[-1]))

total_written_lines=total_comments=total_lines=num_lines=0


for File in filelist:
	with open(File, 'r') as cur_file:
		for line in cur_file:
			line = line.strip()
			total_lines += 1
			if line:
				total_written_lines += 1
				if not line.startswith('#'):
					num_lines += 1
				elif line.startswith('#'):
					total_comments += 1

total_spaces = total_lines-total_written_lines
				
				
print("The total lines are: ", total_lines)
print("The total written lines are: ", total_written_lines)
print("The total comments are: ", total_comments)
print("The total non_comments are: ", num_lines)
print("The total spaces are: ", total_spaces)
			
