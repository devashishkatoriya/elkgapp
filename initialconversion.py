import msgpack
import time
import json
from tqdm import tqdm
def main(filename):

	# List of input files
	fileNames = [filename]

	STR_DONE = 'Done.'

	# For every input file
	for in_filename in fileNames:

		# Read input data
		print('\nReading input file...', in_filename)
		total_lines = []
		with open(in_filename, 'r') as in_file:
			total_lines = in_file.readlines()
		print(STR_DONE)
		time1 = time.process_time()

		# Initialise Predicate dictionary
		predicates = dict()

		print('Converting...')
		pbar = tqdm(total=len(total_lines))
		i = 0
		while i < len(total_lines):
			# Iterate over every triple

			line1 = total_lines[i].strip()
			#print(i)

			if line1.startswith('_:') and  total_lines[i+3].strip().split(' ')[1].endswith('#hasVT>'):
				# Current line is part of group of lines containing metaknowledge of TYPE 1 - hasVT

				line1 = line1.split(' ')
				line2 = total_lines[i+1].strip().split(' ')
				line3 = total_lines[i+2].strip().split(' ')
				line4 = total_lines[i+3].strip().split(' ')

				i = i + 4
				pbar.update(4)

				s1 = line1[2]
				p1 = line2[2]
				o1 = line3[2]
				u1 = line1[0]
				t2 = str(int(line4[2][1:-1]))

				if p1 in predicates:
					predicates[p1].append([s1, o1, u1, "-1", t2, "-1", "-1", "0"])
				else:
					predicates[p1] = [[s1, o1, u1, "-1", t2, "-1", "-1", "0"]]
			
			elif line1.startswith('_:') and  total_lines[i+4].strip().split(' ')[1].endswith('#subject>'):
			
				# Current line is part of group of lines containing metaknowledge of TYPE 3 - hascertainty nmk

				line1 = line1.split(' ')
				line2 = total_lines[i+1].strip().split(' ')
				line3 = total_lines[i+2].strip().split(' ')
				line4 = total_lines[i+3].strip().split(' ')
				line5 = total_lines[i+4].strip().split(' ')
				line8 = total_lines[i+7].strip().split(' ')
				

				i = i + 8
				pbar.update(8)

				s1 = line1[2]
				p1 = line2[2]
				o1 = line3[2]
				t1 = str(line4[3])
				u1 = line1[0]
				u2 = line5[0]
				
				mk2 = line8[3]
				mk1 = line8[1]
				#print("pre: ",p1)
				#print("u1: ", u1)
				#print("sub: ", s1)
				#print("obj: ", o1)
				#print("certainty: ", u2)
				#print("meta-knowledge predicate: ", mk2)
				#t31 = str(int(line4[2][1:-1]))
				#t32 = str(int(line5[2][1:-1]))

				if p1 in predicates:
					predicates[p1].append([s1, o1, u1, t1, "-1", "-1", "-1", u2])
				else:
					predicates[p1] = [[s1, o1, u1, t1, "-1", "-1", "-1", u2]]
				if mk1 in predicates:
						predicates[mk1].append([u2, mk2, "0", "-1","-1","-1","-1","0"])
				else:
						predicates[mk1] = [[u2, mk2, "0", "-1","-1","-1","-1","0"]]
			elif line1.startswith('_:') and total_lines[i+3].strip().split(' ')[1].endswith('#hasBegining>'):
				# Current line is part of group of lines containing metaknowledge of TYPE 2 - hasBegining

				line1 = line1.split(' ')
				line2 = total_lines[i+1].strip().split(' ')
				line3 = total_lines[i+2].strip().split(' ')
				line4 = total_lines[i+3].strip().split(' ')
				line5 = total_lines[i+4].strip().split(' ')

				i = i + 5
				pbar.update(5)

				s1 = line1[2]
				p1 = line2[2]
				o1 = line3[2]
				u1 = line1[0]
				t31 = str(int(line4[2][1:-1]))
				t32 = str(int(line5[2][1:-1]))

				if p1 in predicates:
					predicates[p1].append([s1, o1, u1, "-1", "-1", t31, t32, "0"])
				else:
					predicates[p1] = [[s1, o1, u1, "-1", "-1", t31, t32, "0"]]
			elif line1.startswith('_:') and total_lines[i].strip().split(' ')[1].endswith('derives_from>'):
				# Current line is part of group of lines containing metaknowledge of TYPE 3 - derives_from

				line1 = line1.split(' ')
				line2 = total_lines[i+1].strip().split(' ')
				line3 = total_lines[i+2].strip().split(' ')
				line4 = total_lines[i+3].strip().split(' ')
				#line5 = total_lines[i+4].strip().split(' ')

				i = i + 5
				pbar.update(5)

				mk2 = line1[2]
				mk1 = line1[1]
				o1 = line2[2]
				p1 = line3[2]
				s1 = line4[2]
				u1 = line1[0]
				'''print("pre: ",p1)
				print("u1: ", u1)
				print("sub: ", s1)
				print("obj: ", o1)
				print("meta-knowledge predicate: ", mk1)'''
				#t31 = str(int(line4[2][1:-1]))
				#t32 = str(int(line5[2][1:-1]))

				if p1 in predicates:
					predicates[p1].append([s1, o1, u1, "-1", "-1", "-1", "-1", "0"])
				else:
					predicates[p1] = [[s1, o1, u1, "-1", "-1", "-1", "-1", "0"]]
				if mk1 in predicates:
						predicates[mk1].append([u1, mk2, "0", "-1","-1","-1","-1","0"])
				else:
						predicates[mk1] = [[u1, mk2, "0", "-1","-1","-1","-1","0"]]
			
			elif line1.startswith('<http'):
				# Current line does not contain metaknowledge

				line1 = line1.split('> ')

				i = i + 1
				pbar.update(1)

				s1 = line1[0] + '>'
				p1 = line1[1] + '>'
				o1 = line1[2][:-2]

				if p1 in predicates:
					predicates[p1].append([s1, o1, "-1", "-1", "-1", "-1", "-1", "0"])
				else:
					predicates[p1] = [[s1, o1, "-1", "-1", "-1", "-1", "-1", "0"]]
			'''elif total_lines[i].strip().split(' ')[1].endswith('#subject>'):
				# Current line is part of group of lines containing metaknowledge of TYPE 1 - subject

				line1 = line1.split(' ')
				line2 = total_lines[i+1].strip().split(' ')
				line3 = total_lines[i+2].strip().split(' ')
				#line4 = total_lines[i+3].strip().split(' ')

				i = i + 3
				pbar.update(4)

				s1 = line1[2]
				p1 = line2[2]
				o1 = line3[2]
				u1 = line1[0]
				#t2 = str(int(line4[2][1:-1]))

				if p1 in predicates:
					predicates[p1].append([s1, o1, u1, "-1", "-1", "-1", "-1", "0"])
				else:
					predicates[p1] = [[s1, o1, u1, "-1", "-1", "-1", "-1", "0"]]'''
			'''elif line1.startswith('_:'):
			
				# Current line is part of group of lines containing metaknowledge of TYPE 3 - hscertainty

				line1 = line1.split(' ')
				line2 = total_lines[i+1].strip().split(' ')
				line3 = total_lines[i+2].strip().split(' ')
				line4 = total_lines[i+3].strip().split(' ')
				line5 = total_lines[i+4].strip().split(' ')
				line6 = total_lines[i+5].strip().split(' ')
				line7 = total_lines[i+6].strip().split(' ')
				

				i = i + 7
				pbar.update(7)

				s1 = line1[2]
				p1 = line2[2]
				o1 = line3[2]
				t1 = line4[2]
				u1 = line1[0]
				t31 = str(int(line5[2][1:-1]))
				t32 = str(int(line6[2][1:-1]))
				mk2 = line7[2]
				mk1 = line7[1]
				#print("pre: ",p1)
				#print("u1: ", u1)
				#print("sub: ", s1)
				#print("obj: ", o1)
				#print("meta-knowledge predicate: ", mk1)
				#t31 = str(int(line4[2][1:-1]))
				#t32 = str(int(line5[2][1:-1]))

				if p1 in predicates:
					predicates[p1].append([s1, o1, u1, t1, "-1", t31, t32, "0"])
				else:
					predicates[p1] = [[s1, o1, u1, t1, "-1", t31, t32, "0"]]
				if mk1 in predicates:
						predicates[mk1].append([u1, mk2, "0", "-1","-1","-1","-1","0"])
				else:
						predicates[mk1] = [[u1, mk2, "0", "-1","-1","-1","-1","0"]]'''

			

		pbar.close()
		print(STR_DONE)
		time2 = time.process_time()
		print('Time taken for conversion:', (time2 - time1))
		return predicates
		

#-------------------------------

if __name__ == "__main__":
    main('./input_files/generated_Rmk.nt')
