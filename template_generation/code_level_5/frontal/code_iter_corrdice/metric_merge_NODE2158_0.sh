while getopts 'n:' flag; do
  case "${flag}" in
    n) iter_num="${OPTARG}" ;;
    *)
      echo "Usage: $0 [-n iter_num]"
      exit 1
      ;;
  esac
done
iter_num_last=$((${iter_num} - 1))
wb_command -metric-math '(x0+x1+x2+x3+x4+x5+x6+x7+x8+x9+x10+x11+x12+x13+x14+x15+x16+x17+x18+x19+x20+x21+x22+x23+x24+x25+x26+x27+x28+x29+x30+x31+x32+x33+x34+x35+x36+x37+x38+x39+x40+x41+x42+x43+x44+x45+x46+x47+x48+x49+x50+x51+x52+x53+x54+x55+x56+x57+x58+x59+x60+x61+x62+x63+x64+x65+x66+x67+x68+x69+x70+x71+x72+x73+x74+x75+x76+x77+x78+x79+x80+x81+x82+x83+x84+x85+x86+x87+x88+x89)/90' /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/NODE2158_${iter_num}.curv.affine.ico6.shape.gii -var x0 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/131217.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x1 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/179952.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x2 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/553344.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x3 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/107725.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x4 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/107725.R.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x5 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/204521.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x6 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/953764.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x7 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/713239.R.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x8 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/339847.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x9 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/205725.R.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x10 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/765864.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x11 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/195445.R.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x12 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/111211.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x13 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/171734.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x14 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/178243.R.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x15 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/937160.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x16 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/804646.R.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x17 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/102513.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x18 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/965771.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x19 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/558657.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x20 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/176542.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x21 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/929464.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x22 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/143224.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x23 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/767464.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x24 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/810439.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x25 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/715950.R.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x26 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/199655.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x27 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/251833.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x28 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/169343.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x29 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/627549.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x30 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/530635.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x31 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/571144.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x32 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/132017.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x33 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/202113.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x34 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/336841.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x35 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/559457.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x36 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/843151.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x37 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/186848.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x38 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/727553.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x39 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/183337.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x40 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/211619.R.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x41 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/355239.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x42 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/852455.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x43 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/644044.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x44 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/105216.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x45 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/672756.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x46 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/131419.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x47 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/208125.R.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x48 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/191235.R.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x49 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/783462.R.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x50 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/147030.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x51 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/151728.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x52 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/128329.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x53 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/146331.R.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x54 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/102614.R.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x55 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/173536.R.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x56 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/191336.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x57 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/197449.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x58 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/536647.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x59 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/204319.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x60 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/355845.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x61 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/185139.R.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x62 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/228434.R.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x63 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/185341.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x64 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/135932.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x65 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/163331.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x66 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/729254.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x67 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/729254.R.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x68 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/107018.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x69 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/118023.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x70 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/163331.R.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x71 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/171734.R.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x72 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/182032.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x73 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/182032.R.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x74 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/586460.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x75 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/355542.R.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x76 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/118124.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x77 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/148840.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x78 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/314225.R.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x79 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/192237.R.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x80 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/475855.R.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x81 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/185947.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x82 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/387959.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x83 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/880157.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x84 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/211114.R.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x85 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/382242.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x86 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/500222.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x87 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/248238.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x88 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/734247.L.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii -var x89 /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/107321.R.MSM.NODE2158_${iter_num}.transformed_and_reprojected.func.gii;
wb_command -metric-merge /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/NODE2158_frontal_merged.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/131217.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/179952.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/553344.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/107725.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/107725.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/204521.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/953764.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/713239.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/339847.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/205725.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/765864.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/195445.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/111211.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/171734.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/178243.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/937160.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/804646.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/102513.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/965771.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/558657.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/176542.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/929464.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/143224.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/767464.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/810439.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/715950.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/199655.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/251833.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/169343.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/627549.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/530635.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/571144.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/132017.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/202113.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/336841.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/559457.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/843151.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/186848.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/727553.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/183337.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/211619.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/355239.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/852455.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/644044.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/105216.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/672756.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/131419.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/208125.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/191235.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/783462.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/147030.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/151728.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/128329.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/146331.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/102614.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/173536.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/191336.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/197449.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/536647.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/204319.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/355845.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/185139.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/228434.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/185341.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/135932.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/163331.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/729254.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/729254.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/107018.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/118023.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/163331.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/171734.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/182032.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/182032.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/586460.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/355542.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/118124.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/148840.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/314225.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/192237.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/475855.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/185947.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/387959.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/880157.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/211114.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/382242.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/500222.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/248238.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/734247.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/107321.R.frontal.ico6.shape.gii;
wb_command -metric-reduce /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/NODE2158_frontal_merged.shape.gii MAX /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/NODE2158_frontal_mask.shape.gii;

cp /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/NODE2158_${iter_num}.curv.affine.ico6.shape.gii /HPC_work_dir/corrdice_affine_mask/checkNODE2158_msmrefine/NODE2158.final.curv.affine.ico6.shape.gii
