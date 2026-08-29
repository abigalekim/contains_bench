export PATH=~/micromamba/envs/cudf_dev/NVIDIA-Nsight-Compute-2026.1:$PATH

# Define the metrics variable
NCU_METRICS="smsp__average_thread_inst_executed_per_inst_executed.ratio,smsp__issue_active.avg.pct_of_peak_sustained_active,smsp__warps_issue_stalled_long_scoreboard.sum,smsp__warps_issue_stalled_wait.sum,l1tex__t_sectors_pipe_lsu_mem_global_op_ld.sum,l1tex__t_requests_pipe_lsu_mem_global_op_ld.sum,l1tex__t_sector_hit_rate.pct"

ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu skew_32.csv het > ../profiles/het/het_skew_32.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu skew_16.csv het > ../profiles/het/het_skew_16.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu skew_64.csv het > ../profiles/het/het_skew_64.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu uniform_dist_16_128.csv het > ../profiles/het/het_uniform.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu normal_16_128.csv het > ../profiles/het/het_normal.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu bimodal_16_5_512_100.csv het > ../profiles/het/het_bimodal_16_5_512_100.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu bimodal_32_10_512_100.csv het > ../profiles/het/het_bimodal_32_10_512_100.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu bimodal_64_20_512_100.csv het > ../profiles/het/het_bimodal_64_20_512_100.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu bimodal_16_5_8192_500.csv het > ../profiles/het/het_bimodal_16_5_8192_500.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu bimodal_32_10_8192_500.csv het > ../profiles/het/het_bimodal_32_10_8192_500.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu bimodal_64_20_8192_500.csv het > ../profiles/het/het_bimodal_64_20_8192_500.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu bimodal_16_5_65536_2000.csv het > ../profiles/het/het_bimodal_16_5_65536_2000.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu bimodal_32_10_65536_2000.csv het > ../profiles/het/het_bimodal_32_10_65536_2000.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu bimodal_64_20_65536_2000.csv het > ../profiles/het/het_bimodal_64_20_65536_2000.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu fb_comments.csv het > ../profiles/het/het_fb_comments.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu fb_posts.csv het > ../profiles/het/het_fb_posts.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu reddit_utf8.csv het > ../profiles/het/het_reddit.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu twitter_utf8.csv het > ../profiles/het/het_twitter.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu amazon_arts_and_crafts.csv het > ../profiles/het/het_amazon.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu yelp_reviews.csv het > ../profiles/het/het_yelp.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu github_commits.csv het > ../profiles/het/het_github.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu common_crawl_urls.csv het > ../profiles/het/het_urls.txt

ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu skew_32.csv cudf > ../profiles/cudf/cudf_skew_32.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu skew_16.csv cudf > ../profiles/cudf/cudf_skew_16.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu skew_64.csv cudf > ../profiles/cudf/cudf_skew_64.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu uniform_dist_16_128.csv cudf > ../profiles/cudf/cudf_uniform.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu normal_16_128.csv cudf > ../profiles/cudf/cudf_normal.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu bimodal_16_5_512_100.csv cudf > ../profiles/cudf/cudf_bimodal_16_5_512_100.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu bimodal_32_10_512_100.csv cudf > ../profiles/cudf/cudf_bimodal_32_10_512_100.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu bimodal_64_20_512_100.csv cudf > ../profiles/cudf/cudf_bimodal_64_20_512_100.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu bimodal_16_5_8192_500.csv cudf > ../profiles/cudf/cudf_bimodal_16_5_8192_500.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu bimodal_32_10_8192_500.csv cudf > ../profiles/cudf/cudf_bimodal_32_10_8192_500.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu bimodal_64_20_8192_500.csv cudf > ../profiles/cudf/cudf_bimodal_64_20_8192_500.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu bimodal_16_5_65536_2000.csv cudf > ../profiles/cudf/cudf_bimodal_16_5_65536_2000.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu bimodal_32_10_65536_2000.csv cudf > ../profiles/cudf/cudf_bimodal_32_10_65536_2000.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu bimodal_64_20_65536_2000.csv cudf > ../profiles/cudf/cudf_bimodal_64_20_65536_2000.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu fb_comments.csv cudf > ../profiles/cudf/cudf_fb_comments.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu fb_posts.csv cudf > ../profiles/cudf/cudf_fb_posts.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu reddit_utf8.csv cudf > ../profiles/cudf/cudf_reddit.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu twitter_utf8.csv cudf > ../profiles/cudf/cudf_twitter.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu amazon_arts_and_crafts.csv cudf > ../profiles/cudf/cudf_amazon.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu yelp_reviews.csv cudf > ../profiles/cudf/cudf_yelp.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu github_commits.csv cudf > ../profiles/cudf/cudf_github.txt
ncu --section SpeedOfLight --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu common_crawl_urls.csv cudf > ../profiles/cudf/cudf_urls.txt

ncu --section SpeedOfLight  --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu skew_16_pct_0.1.csv cudf > ../profiles/exp5/cudf_pct_0.1.txt
ncu --section SpeedOfLight  --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu skew_16_pct_0.5.csv cudf > ../profiles/exp5/cudf_pct_0.5.txt
ncu --section SpeedOfLight  --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu skew_16_pct_1.0.csv cudf > ../profiles/exp5/cudf_pct_1.0.txt
ncu --section SpeedOfLight  --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu skew_16_pct_5.0.csv cudf > ../profiles/exp5/cudf_pct_5.0.txt
ncu --section SpeedOfLight  --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu skew_16_pct_10.0.csv cudf > ../profiles/exp5/cudf_pct_10.0.txt
ncu --section SpeedOfLight  --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu skew_16_pct_25.0.csv cudf > ../profiles/exp5/cudf_pct_25.0.txt
ncu --section SpeedOfLight  --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu skew_16_pct_50.0.csv cudf > ../profiles/exp5/cudf_pct_50.0.txt
ncu --section SpeedOfLight  --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu skew_16_pct_75.0.csv cudf > ../profiles/exp5/cudf_pct_75.0.txt
ncu --section SpeedOfLight  --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu skew_16_pct_90.0.csv cudf > ../profiles/exp5/cudf_pct_90.0.txt
ncu --section SpeedOfLight  --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu skew_16_pct_95.0.csv cudf > ../profiles/exp5/cudf_pct_95.0.txt
ncu --section SpeedOfLight  --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu skew_16_pct_99.0.csv cudf > ../profiles/exp5/cudf_pct_99.0.txt
ncu --section SpeedOfLight  --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu skew_16_pct_99.5.csv cudf > ../profiles/exp5/cudf_pct_99.5.txt
ncu --section SpeedOfLight  --metrics $NCU_METRICS --kernel-name 'regex:transform_kernel|contains_warp_parallel_fn' ../build/contains_ncu skew_16_pct_99.9.csv cudf > ../profiles/exp5/cudf_pct_99.9.txt