import numpy
import nibabel

regularisation = [ 0.025, 0.05, 0.1, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7 ]

#group = 2182
#subjects = [ 101309, 101410, 103010, 130417, 131823, 136833, 140319, 144226, 150625, 155938, 157942, 164030, 166640, 167238, 169141, 186545, 191336, 196346, 203418, 214423, 257542, 316835, 376247, 380036, 421226, 506234, 512835, 518746, 531536, 541640, 548250, 579665, 588565, 597869, 627549, 702133, 705341, 783462, 792867, 886674, 995174 ]

#group = 1910
#subjects = [ 130619, 136732, 144731, 144732, 145127, 146836, 166438, 189349, 228434, 391748, 512835, 565452, 572045, 590047, 644246, 769064, 814649 ]

#group = 1951
#subjects = [ 124220, 138332, 146533, 153227, 187345, 188751, 237334, 281135, 303119, 378857, 381038, 387959, 465852, 513736, 529549, 672756, 694362, 828862, 865363, 872158 ]

#group = 2142
#subjects = [ 101915, 108828, 118932, 128026, 128027, 138130, 144832, 154835, 154836, 157336, 161731, 164939, 183741, 185442, 187850, 192843, 192844, 195950, 199150, 248339, 287248, 299760, 351938, 368551, 422632, 552241, 558960, 576255, 583858, 598568, 654350, 660951, 695768, 751348, 763557, 820745, 917558, 917559, 989987, 995174 ]

#group = 2078
#subjects = [ 119025, 124220, 156233, 156536, 165032, 206929, 208327, 208328, 214726, 237334, 351938, 365343, 381543, 386250, 727654, 815247, 973770 ]

#group = 2126
#subjects = [ 104820, 116221, 127226, 194645, 207628, 284646, 394956, 647858 ]

#group = 2133
#subjects = [ 117122, 117123, 128026, 139637, 561444, 660951, 677968 ]

group = 2143
subjects = [ 112920, 122822, 125424, 137532, 140117, 140824, 146937, 162935, 165638, 168745, 170934, 180533, 183034, 186949, 188448, 193845, 195445, 196750, 206525, 213522, 214221, 349244, 371843, 448347, 465852, 492754, 523032, 529953, 597869, 683256, 690152, 704238, 704239, 724446, 725751, 742549, 782157, 784565, 786569, 788674, 792867, 810843, 894067, 910241, 910443, 947668, 994273, 994274 ]

percentile = 75
num_pairs = (len(subjects)*(len(subjects)-1))/2

corrsum = 0.0
dice_sum = 0.0

for i in range(len(subjects)):
	for j in range(i+1, len(subjects)):
		subject1 = nibabel.load("/home/rb22/fsldev/studies/groupwise/data/" + str(group) + "/" + str(subjects[i]) + ".L.sulc.affine.ico6.shape.gii").darrays[0].data
		subject2 = nibabel.load("/home/rb22/fsldev/studies/groupwise/data/" + str(group) + "/" + str(subjects[j]) + ".L.sulc.affine.ico6.shape.gii").darrays[0].data

		corrsum += numpy.corrcoef(subject1, subject2)[0,1]
		
		sub1perc = numpy.where((subject1 > numpy.percentile(subject1, percentile)), 1, 0)
		sub2perc = numpy.where((subject2 > numpy.percentile(subject2, percentile)), 1, 0)
		dice_sum += (2 * numpy.sum(sub1perc * sub2perc)) / (numpy.sum(sub1perc) + numpy.sum(sub2perc))

print("After rigid alignment, group {}'s CC similarity: {:.4}; Dice overlap: {:0,.2f}%".format(group, corrsum/num_pairs, (dice_sum/num_pairs)*100))

corrsum = 0.0
dice_sum = 0.0

for reg in regularisation:
	for i in range(len(subjects)):
		for j in range(i+1, len(subjects)):
			subject1 = nibabel.load("/home/rb22/fsldev/studies/groupwise/hpc_results/output/" + str(group) + "/" + str(reg) + "/groupwise." + str(group) + "." + str(reg) + ".transformed_and_reprojected.dedrift-" + str(subjects[i]) + ".func.gii").darrays[0].data
			subject2 = nibabel.load("/home/rb22/fsldev/studies/groupwise/hpc_results/output/" + str(group) + "/" + str(reg) + "/groupwise." + str(group) + "." + str(reg) + ".transformed_and_reprojected.dedrift-" + str(subjects[j]) + ".func.gii").darrays[0].data
			
			corrsum += numpy.corrcoef(subject1, subject2)[0,1]
			
			sub1perc = numpy.where((subject1 > numpy.percentile(subject1, percentile)), 1, 0)
			sub2perc = numpy.where((subject2 > numpy.percentile(subject2, percentile)), 1, 0)
			dice_sum += (2 * numpy.sum(sub1perc * sub2perc)) / (numpy.sum(sub1perc) + numpy.sum(sub2perc))

	areal = numpy.abs(numpy.asarray(nibabel.load("/home/rb22/fsldev/studies/groupwise/hpc_results/results/" + str(group) + "/" + str(reg) + "/groupwise." + str(group) + "." + str(reg) + ".areal.distortion.merge.L.sulc.affine.dedrifted.ico6.shape.gii").agg_data()).flatten())
	shape = numpy.abs(numpy.asarray(nibabel.load("/home/rb22/fsldev/studies/groupwise/hpc_results/results/" + str(group) + "/" + str(reg) + "/groupwise." + str(group) + "." + str(reg) + ".shape.distortion.merge.L.sulc.affine.dedrifted.ico6.shape.gii").agg_data()).flatten())

	print("Lambda: {}; CC similarity: {:.4}; Dice overlap: {:0,.2f}%; Areal mean: {:.4}; Areal Max: {:.4}; Areal 95%: {:.4}; Areal 98%: {:.4}; Shape mean: {:.4}; Shape Max: {:.4}".format(reg, corrsum/num_pairs, (dice_sum/num_pairs)*100, numpy.mean(areal), numpy.max(areal), numpy.percentile(areal, 95), numpy.percentile(areal, 98), numpy.mean(shape), numpy.max(shape)))
	
	#This is for a CSV like output
	#print("{} ({}),{},{:.4},{:.4},{:.4},{:.4},{:.4},{:.4},{:.4},{:.4}".format(group, len(subjects), reg, corrsum/num_pairs, dice_sum/num_pairs, numpy.mean(areal), numpy.max(areal), numpy.percentile(areal, 95), numpy.percentile(areal, 98), numpy.mean(shape), numpy.max(shape)))
	
	corrsum = 0.0
	dice_sum = 0.0
