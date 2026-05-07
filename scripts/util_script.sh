export PATH=~/micromamba/envs/cudf_dev/NVIDIA-Nsight-Compute-2026.1:$PATH

# Define the metrics variable
NCU_METRICS="smsp__average_thread_inst_executed_per_inst_executed.ratio,smsp__issue_active.avg.pct_of_peak_sustained_active,smsp__warps_issue_stalled_long_scoreboard.sum,smsp__warps_issue_stalled_wait.sum,l1tex__t_sectors_pipe_lsu_mem_global_op_ld.sum,l1tex__t_requests_pipe_lsu_mem_global_op_ld.sum,l1tex__t_sector_hit_rate.pct"

ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu skew_32.csv thread > ../profiles/thread/thread_skew_32.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu skew_16.csv thread > ../profiles/thread/thread_skew_16.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu skew_64.csv thread > ../profiles/thread/thread_skew_64.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu uniform_dist_16_128.csv thread > ../profiles/thread/thread_uniform.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu normal_16_128.csv thread > ../profiles/thread/thread_normal.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu bimodal_16_5_512_100.csv thread > ../profiles/thread/thread_bimodal_16_5_512_100.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu bimodal_32_10_512_100.csv thread > ../profiles/thread/thread_bimodal_32_10_512_100.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu bimodal_64_20_512_100.csv thread > ../profiles/thread/thread_bimodal_64_20_512_100.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu bimodal_16_5_8192_500.csv thread > ../profiles/thread/thread_bimodal_16_5_8192_500.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu bimodal_32_10_8192_500.csv thread > ../profiles/thread/thread_bimodal_32_10_8192_500.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu bimodal_64_20_8192_500.csv thread > ../profiles/thread/thread_bimodal_64_20_8192_500.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu bimodal_16_5_65536_2000.csv thread > ../profiles/thread/thread_bimodal_16_5_65536_2000.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu bimodal_32_10_65536_2000.csv thread > ../profiles/thread/thread_bimodal_32_10_65536_2000.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu bimodal_64_20_65536_2000.csv thread > ../profiles/thread/thread_bimodal_64_20_65536_2000.txt